#!/usr/bin/env bash
# Start DeepSeek Harness behind the PRIVATE GitHub Codespaces port-forward.
# Do not paste the printed tokenized URL into logs or public issues.
set -euo pipefail
if [[ -z "${CODESPACE_NAME:-}" ]]; then
  echo "This launcher requires a GitHub Codespace (CODESPACE_NAME missing)." >&2
  exit 2
fi
cd "$(dirname "$0")/.."
host="${CODESPACE_NAME}-3080.app.github.dev"
url="https://${host}/"
echo "Starting DSH Web with Codespaces authority configured."
echo "Keep forwarded port 3080 PRIVATE in the Codespaces Ports panel."
exec pnpm dsh web --no-open --public-url "$url" --trusted-host "$host"
