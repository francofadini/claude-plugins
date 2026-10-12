#!/usr/bin/env bash
# Bloquea LECTURA de archivos .env con secretos (via Read y Bash: cat/grep/head/tail/less/more/sed/awk/strings/xxd/od/...).
# - Permite templates sin secretos: .env.example / .env.sample / .env.template / .env.dist / .env.defaults
# - No falsea con `grep "\.env" <dir>` (buscar el string, no leer el archivo): se sacan los segmentos entre comillas antes de matchear.
# - No bloquea `source .env.local` (boot de servers): `source` no es un comando de lectura de archivo.
# Usar como PreToolUse hook con matcher "Read|Bash".

set -euo pipefail

input="$(cat)"
tool_name="$(printf '%s' "$input" | jq -r '.tool_name // ""')"

deny() {
  local reason="$1"
  jq -cn --arg r "$reason" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $r
    }
  }'
  exit 0
}

# ¿El token es un archivo .env (cualquiera)?
is_env_file() { [[ "$1" =~ (^|/)\.env(\.[A-Za-z0-9_.-]+)?$ ]]; }

# ¿Es un template sin secretos (lectura OK)?
is_safe_env() { [[ "$1" =~ (^|/)\.env\.(example|sample|template|dist|defaults)$ ]]; }

case "$tool_name" in
  Read)
    file_path="$(printf '%s' "$input" | jq -r '.tool_input.file_path // ""')"
    if is_env_file "$file_path" && ! is_safe_env "$file_path"; then
      deny "Lectura de .env con secretos bloqueada (block-env-access). Ruta: $file_path. Los templates (.env.example/.sample/.template/.dist/.defaults) sí se pueden leer."
    fi
    ;;
  Bash)
    command="$(printf '%s' "$input" | jq -r '.tool_input.command // ""')"
    # Sacar segmentos entre comillas: `grep "\.env" dir` busca el string, no lee el archivo.
    stripped="$(printf '%s' "$command" | sed -E "s/'[^']*'//g; s/\"[^\"]*\"//g")"
    # Gate preciso: un comando de LECTURA apuntando directamente a un path .env (no matchea `source .env.local`).
    read_regex='(^|[[:space:];&|`$(])(cat|bat|less|more|head|tail|grep|egrep|fgrep|rg|ripgrep|sed|awk|strings|xxd|od|nl|tac|wc|cut|tr|dd)([[:space:]]+[^;&|`$()]*)*[[:space:]]+[^[:space:];&|`$()]*\.env([.[:alnum:]_-]*)?([[:space:];&|`$()]|$)'
    if printf '%s' "$stripped" | grep -Eq "$read_regex"; then
      # Hay lectura de algún .env; bloquear solo si el archivo NO es un template seguro.
      for tok in $stripped; do
        if is_env_file "$tok" && ! is_safe_env "$tok"; then
          deny "Lectura de .env con secretos via Bash bloqueada (block-env-access). Archivo: $tok. Los templates (.env.example/.sample/.template) sí se pueden leer."
        fi
      done
    fi
    ;;
esac

# Sin output = allow (default)
exit 0
