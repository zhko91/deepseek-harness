#!/usr/bin/env bash
# Launch the private Codespaces Web UI. Startup diagnostics never print tokenized URLs.
set -euo pipefail
if [[ -z "${CODESPACE_NAME:-}" ]]; then
  echo "Codespaces required: CODESPACE_NAME is not set." >&2
  exit 2
fi
cd "$(dirname "$0")/.."
host="${CODESPACE_NAME}-3080.app.github.dev"
url="https://${host}/"
echo "Starting DSH Web for the private Codespaces port 3080."
echo "Keep port 3080 PRIVATE. Open only the tokenized URL shown by DSH."
# Capture the latest startup diagnostics without guessing a timestamp or filename.
logdir="${DSH_HOME:-$HOME/.dsh}/logs"
before=""
if [[ -d "$logdir" ]]; then
  before="$(find "$logdir" -maxdepth 1 -type f -name 'startup-*.log' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2- || true)"
fi
set +e
pnpm dsh web --no-open --public-url "$url" --trusted-host "$host"
status=$?
set -e
if (( status != 0 )); then
  echo "DSH startup failed (exit $status)." >&2
  if [[ -d "$logdir" ]]; then
    latest="$(find "$logdir" -maxdepth 1 -type f -name 'startup-*.log' -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2- || true)"
    if [[ -n "$latest" && -f "$latest" ]]; then
      echo "Latest diagnostic log: $latest" >&2
      echo "To inspect it locally: tail -n 80 \"$latest\"" >&2
      # Never echo log contents automatically: they can contain secrets.
    else
      echo "No startup log found in $logdir" >&2
    fi
  fi
fi
exit "$status"
