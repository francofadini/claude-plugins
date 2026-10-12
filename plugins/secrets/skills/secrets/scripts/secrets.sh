#!/usr/bin/env bash
# secrets.sh — secretos con dotenvx sin que el agente vea nunca un valor.
#
#   secrets.sh init  [archivo]          crea el archivo encriptado y suma su .env.keys al .gitignore
#   secrets.sh set   NOMBRE [archivo]   guarda el valor que está en el portapapeles (y lo vacía)
#   secrets.sh names [archivo]          lista solo los nombres
#   secrets.sh has   NOMBRE [archivo]   exit 0 si existe y no está vacío
#   secrets.sh run   [archivo] -- cmd   corre cmd con los secretos cargados
#
# Archivo por defecto: $CLAUDE_PROJECT_DIR/.claude/.env (o ./.claude/.env).

set -euo pipefail

default_file() { echo "${CLAUDE_PROJECT_DIR:-$PWD}/.claude/.env"; }
die() { echo "secrets: $*" >&2; exit 1; }
command -v dotenvx >/dev/null || die "falta dotenvx (brew install dotenvx/brew/dotenvx)"

ensure_gitignore() {
  local file="$1" dir root rel
  dir="$(cd "$(dirname "$file")" && pwd -P)"
  root="$(git -C "$dir" rev-parse --show-toplevel 2>/dev/null || echo "$dir")"
  rel="${dir#"$root"}"; rel="${rel#/}"
  local entry="${rel:+$rel/}.env.keys"
  touch "$root/.gitignore"
  grep -qxF "$entry" "$root/.gitignore" || grep -qxF ".env.keys" "$root/.gitignore" || echo "$entry" >> "$root/.gitignore"
}

cmd="${1:-}"; shift || true
case "$cmd" in
  init)
    file="${1:-$(default_file)}"
    mkdir -p "$(dirname "$file")"
    [[ -f "$file" ]] || printf '# Secretos encriptados con dotenvx. Se escriben con secrets.sh set.\n' > "$file"
    dotenvx encrypt -f "$file" >/dev/null
    ensure_gitignore "$file"
    echo "listo: $file (encriptado; la key en $(dirname "$file")/.env.keys, ignorada por git)"
    ;;
  set)
    name="${1:-}"; [[ "$name" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || die "uso: secrets.sh set NOMBRE [archivo]"
    file="${2:-$(default_file)}"
    value="$(pbpaste)"
    [[ -n "$value" ]] || die "el portapapeles está vacío: copiá el valor y volvé a correr"
    [[ -f "$file" ]] || "$0" init "$file" >/dev/null
    dotenvx set "$name" -f "$file" -- "$value" >/dev/null
    printf '' | pbcopy
    echo "$name guardado encriptado en $file (portapapeles vaciado)"
    ;;
  names)
    file="${1:-$(default_file)}"; [[ -f "$file" ]] || die "no existe $file"
    grep -oE '^[A-Za-z_][A-Za-z0-9_]*=' "$file" | tr -d '=' | grep -v '^DOTENV_PUBLIC_KEY' || true
    ;;
  has)
    name="${1:-}"; file="${2:-$(default_file)}"
    [[ -n "$(dotenvx get "$name" -f "$file" 2>/dev/null)" ]]
    ;;
  run)
    file="$(default_file)"
    if [[ "${1:-}" != "--" ]]; then file="$1"; shift; fi
    [[ "${1:-}" == "--" ]] && shift
    [[ $# -gt 0 ]] || die "uso: secrets.sh run [archivo] -- comando"
    exec dotenvx run -q -f "$file" -- "$@"
    ;;
  *) sed -n '2,10p' "$0"; exit 1 ;;
esac
