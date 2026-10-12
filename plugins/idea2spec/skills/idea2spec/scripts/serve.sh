#!/usr/bin/env bash
# serve.sh: serve a folder over local HTTP and, optionally, expose it with a cloudflared quick tunnel.
#
# Usage:
#   serve.sh <folder> [--port N] [--tunnel] [--check file.html]
#   serve.sh --stop <folder>
#
#   <folder>        folder to serve (only this folder is exposed, e.g. idea2spec/docs)
#   --port N        preferred port (default 4570); if busy, the next free one is used
#   --tunnel        also open a cloudflared quick tunnel (if cloudflared is installed) and print its URL
#   --check FILE    file to verify with curl (default: the first .html in the folder, else the folder root)
#   --stop          stop the server and tunnel started for <folder>
#
# Idempotent: if a server (or tunnel) for the same folder is already running, it is reused.
# State lives in ${TMPDIR:-/tmp}/idea2spec-serve/. Every URL printed has been verified with curl (HTTP 200).
# Exit codes: 0 ok · 1 bad usage · 2 local server not responding 200 · 3 tunnel failed (local still up).

set -u

PORT_PREF=4570
TUNNEL=0
STOP=0
CHECK=""
DIR=""

while [ $# -gt 0 ]; do
  case "$1" in
    --port) PORT_PREF="${2:-}"; shift 2 ;;
    --tunnel) TUNNEL=1; shift ;;
    --check) CHECK="${2:-}"; shift 2 ;;
    --stop) STOP=1; shift ;;
    -h|--help) sed -n '2,17p' "$0"; exit 0 ;;
    *) if [ -z "$DIR" ]; then DIR="$1"; shift; else echo "Unknown argument: $1" >&2; exit 1; fi ;;
  esac
done

if [ -z "$DIR" ] || [ ! -d "$DIR" ]; then
  echo "Usage: serve.sh <folder> [--port N] [--tunnel] [--check file.html] | --stop <folder>" >&2
  [ -n "$DIR" ] && echo "Not a folder: $DIR" >&2
  exit 1
fi
DIR="$(cd "$DIR" && pwd)"
STATE_DIR="${TMPDIR:-/tmp}"; STATE_DIR="${STATE_DIR%/}/idea2spec-serve"
mkdir -p "$STATE_DIR"
KEY="$(python3 -c 'import hashlib,sys;print(hashlib.md5(sys.argv[1].encode()).hexdigest()[:10])' "$DIR")"
SRV_STATE="$STATE_DIR/$KEY.server"     # "pid port"
TUN_STATE="$STATE_DIR/$KEY.tunnel"     # "pid url"
SRV_LOG="$STATE_DIR/$KEY.server.log"
TUN_LOG="$STATE_DIR/$KEY.tunnel.log"

alive() { [ -n "${1:-}" ] && kill -0 "$1" 2>/dev/null; }
http_code() { curl -s -o /dev/null -m 10 -w '%{http_code}' "$1" 2>/dev/null; }

# ---------- stop ----------
if [ "$STOP" = 1 ]; then
  for f in "$TUN_STATE" "$SRV_STATE"; do
    if [ -f "$f" ]; then
      read -r pid _ < "$f"
      alive "$pid" && kill "$pid" 2>/dev/null && echo "Stopped PID $pid"
      rm -f "$f"
    fi
  done
  exit 0
fi

# ---------- file to check ----------
if [ -z "$CHECK" ]; then
  CHECK="$(cd "$DIR" && ls -1 *.html 2>/dev/null | head -1)"
fi
CHECK_PATH=""
[ -n "$CHECK" ] && CHECK_PATH="$(python3 -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' "$CHECK")"

# ---------- local server ----------
PORT=""
if [ -f "$SRV_STATE" ]; then
  read -r pid port < "$SRV_STATE"
  if alive "$pid" && [ "$(http_code "http://localhost:$port/")" = "200" ]; then
    PORT="$port"; echo "Reusing server (PID $pid) for $DIR"
  else
    rm -f "$SRV_STATE"
  fi
fi

if [ -z "$PORT" ]; then
  PORT="$(python3 - "$PORT_PREF" <<'PY'
import socket, sys
start = int(sys.argv[1])
for p in range(start, start + 200):
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", p)); s.close(); print(p); break
    except OSError:
        s.close()
PY
)"
  if [ -z "$PORT" ]; then echo "No free port found from $PORT_PREF" >&2; exit 2; fi
  nohup python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$DIR" >"$SRV_LOG" 2>&1 &
  pid=$!
  echo "$pid $PORT" > "$SRV_STATE"
  for _ in $(seq 1 30); do
    [ "$(http_code "http://localhost:$PORT/")" = "200" ] && break
    sleep 0.2
  done
fi

LOCAL="http://localhost:$PORT/$CHECK_PATH"
code="$(http_code "$LOCAL")"
if [ "$code" != "200" ]; then
  echo "Local server is NOT responding 200 at $LOCAL (got: ${code:-none}). Log: $SRV_LOG" >&2
  exit 2
fi
echo "Local:  $LOCAL  (200 OK)"
echo "Folder: $DIR"

# ---------- tunnel ----------
if [ "$TUNNEL" = 1 ]; then
  if ! command -v cloudflared >/dev/null 2>&1; then
    echo "cloudflared is not installed: no public link. Install it with 'brew install cloudflared' or share the local URL." >&2
    exit 3
  fi
  URL=""
  if [ -f "$TUN_STATE" ]; then
    read -r tpid turl < "$TUN_STATE"
    if alive "$tpid"; then URL="$turl"; echo "Reusing tunnel (PID $tpid)"; else rm -f "$TUN_STATE"; fi
  fi
  if [ -z "$URL" ]; then
    : > "$TUN_LOG"
    nohup cloudflared tunnel --no-autoupdate --url "http://127.0.0.1:$PORT" >"$TUN_LOG" 2>&1 &
    tpid=$!
    for _ in $(seq 1 60); do
      URL="$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUN_LOG" 2>/dev/null | head -1)"
      [ -n "$URL" ] && break
      alive "$tpid" || break
      sleep 0.5
    done
    if [ -z "$URL" ]; then
      echo "The tunnel did not start. Log: $TUN_LOG" >&2
      alive "$tpid" && kill "$tpid" 2>/dev/null
      exit 3
    fi
    echo "$tpid $URL" > "$TUN_STATE"
  fi
  # Wait until the tunnel has registered with Cloudflare before the first request: querying the
  # hostname too early makes the local resolver cache a "does not exist" answer for minutes.
  for _ in $(seq 1 40); do
    grep -q 'Registered tunnel connection' "$TUN_LOG" 2>/dev/null && break
    sleep 0.5
  done
  sleep 2
  PUBLIC="$URL/$CHECK_PATH"
  HOST="${URL#https://}"
  code=""; via=""
  for _ in $(seq 1 20); do
    code="$(http_code "$PUBLIC")"
    [ "$code" = "200" ] && break
    # Local DNS may still be stale: resolve through a public resolver and pin the address.
    if command -v dig >/dev/null 2>&1; then
      ip="$(dig +short @1.1.1.1 "$HOST" 2>/dev/null | grep -E '^[0-9.]+$' | head -1)"
      if [ -n "$ip" ]; then
        code="$(curl -s -o /dev/null -m 10 -w '%{http_code}' --resolve "$HOST:443:$ip" "$PUBLIC" 2>/dev/null)"
        [ "$code" = "200" ] && { via=" via 1.1.1.1; this computer's DNS may take a minute to catch up"; break; }
      fi
    fi
    sleep 2
  done
  if [ "$code" != "200" ]; then
    echo "Tunnel is up but $PUBLIC does not answer 200 yet (got: ${code:-none}). Retry the check in a few seconds. Log: $TUN_LOG" >&2
    exit 3
  fi
  echo "Public: $PUBLIC  (200 OK$via)"
fi

echo "Stop with: $0 --stop \"$DIR\""
