#!/bin/bash
# PreToolUse hook para Bash.
# Bloquea comandos que típicamente exponen credenciales al stdout (chat).
# Complementa a block-env-access.sh (bloquea leer .env).
# Los secretos viven encriptados con dotenvx (por defecto `.claude/.env`; la key en `.claude/.env.keys`).
#
# Input: JSON en stdin con .tool_input.command.
# Exit: 0 = permitir; 2 = bloquear con mensaje al stderr.

set -e

INPUT=$(cat)
CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')

[[ -z "$CMD" ]] && exit 0

# --- 1. source / export sobre .env (bypasea dotenvx) ---
# Con el .env encriptado, `source .claude/.env` carga valores encriptados inútiles
# Y si algún día no está encriptado, expone todo. Forzamos uso de dotenvx.
if echo "$CMD" | grep -qE '(^|[[:space:]]|;|&&|\|\|)(source|\.)[[:space:]]+[^|&;]*\.env($|[[:space:]]|;|&|\|)'; then
  echo "BLOQUEADO: no usar 'source .env' — usá 'dotenvx get NOMBRE_VAR -f .claude/.env' para leer variables individuales sin exponerlas." >&2
  exit 2
fi
if echo "$CMD" | grep -qE 'export[[:space:]]+\$\(.*\.env'; then
  echo "BLOQUEADO: 'export \$(... .env ...)' expone credenciales. Usá 'dotenvx get NOMBRE_VAR -f .claude/.env'." >&2
  exit 2
fi

# --- 2. dotenvx get sin nombre de variable ---
if echo "$CMD" | grep -qE 'dotenvx[[:space:]]+get([[:space:]]|$)'; then
  if ! echo "$CMD" | grep -qE 'dotenvx[[:space:]]+get([[:space:]]+-[a-zA-Z]+[[:space:]]+[^[:space:]]+)*[[:space:]]+[A-Z][A-Z0-9_]{2,}'; then
    echo "BLOQUEADO: 'dotenvx get' sin nombre de variable dumpea TODAS las credenciales al chat. Usá 'dotenvx get NOMBRE_VAR -f .claude/.env'." >&2
    exit 2
  fi
fi

# --- 3. dotenvx decrypt imprimiendo a stdout ---
if echo "$CMD" | grep -qE 'dotenvx[[:space:]]+decrypt[^|&;]*(--stdout|[[:space:]]-o[[:space:]]*-)'; then
  echo "BLOQUEADO: 'dotenvx decrypt --stdout' expone todas las credenciales al chat." >&2
  exit 2
fi

# --- 4. Pipes sospechosos tras dotenvx get / decrypt ---
if echo "$CMD" | grep -qE 'dotenvx[[:space:]]+(get|decrypt)[^|]*\|[[:space:]]*(head|cat|tail|less|more|tee|xxd|od|hexdump|awk|sed|grep)'; then
  echo "BLOQUEADO: no pipees la salida de 'dotenvx get/decrypt' a head/cat/tail/etc — imprime la credencial al chat. Asigná a variable shell: VAR=\$(dotenvx get NAME -f .claude/.env)." >&2
  exit 2
fi

# --- 5. dotenvx run -- env (dumpea todo el env expandido) ---
if echo "$CMD" | grep -qE 'dotenvx[[:space:]]+run[^|]*--[[:space:]]+env([[:space:]]|$|&|;|\|)'; then
  echo "BLOQUEADO: 'dotenvx run -- env' dumpea todas las credenciales al stdout." >&2
  exit 2
fi

# --- 6. cat/head/tail sobre .env* (templates y escrituras con `cat >` se permiten) ---
if echo "$CMD" | grep -qE '(cat|head|tail|less|more|awk|sed|grep)[[:space:]][^|&;]*\.env(\.[^[:space:]|&;]*)?(\.decrypt)?([[:space:]]|$|\||;|&)'; then
  READS_SECRET=0
  for tok in $(echo "$CMD" | grep -oE '[^[:space:]|&;<>"'"'"']*\.env(\.[A-Za-z0-9_.-]+)?'); do
    [[ "$tok" =~ \.env\.(example|sample|template|dist|defaults)$ ]] && continue
    # `cat > file` / `cat >> file` writes, it does not read.
    echo "$CMD" | grep -qE "cat[[:space:]]*>>?[[:space:]]*$tok" && continue
    READS_SECRET=1
  done
  if [[ $READS_SECRET -eq 1 ]]; then
    echo "BLOQUEADO: no leer archivos .env con cat/head/grep/etc — exponen credenciales al chat. Usá 'dotenvx get NOMBRE_VAR -f .claude/.env'." >&2
    exit 2
  fi
fi

# --- 7. echo/printf de variables que parecen credenciales ---
if echo "$CMD" | grep -qE '(echo|printf)[[:space:]][^|;&]*\$\{?[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD|PASS|PWD|URI|DSN|CREDENTIALS?|PRIVATE)[A-Z0-9_]*'; then
  echo "BLOQUEADO: imprimir una credencial la expone en el chat. Usá la variable directamente sin imprimirla." >&2
  exit 2
fi

# --- 8. printenv / env sin grep especifico ---
if echo "$CMD" | grep -qE '(^|[[:space:]]|;|&&|\|\|)(printenv|env)([[:space:]]*$|[[:space:]]*\||[[:space:]]*>|[[:space:]]*;)'; then
  echo "BLOQUEADO: 'printenv' / 'env' sin argumento dumpea todas las variables, incluidas credenciales." >&2
  exit 2
fi

exit 0
