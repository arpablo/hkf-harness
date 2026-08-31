#!/usr/bin/env bash
# Das Python des Harness. Baut die venv, wenn noetig, und startet sie.
#
#     ./py bin/hk-lint            wie bin/hk-lint, nur ausdruecklich
#     ./py -c "import yaml; ..."  ein Einzeiler in derselben Umgebung
#     ./py                        die Konsole
set -euo pipefail
WURZEL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$WURZEL/bootstrap-python.sh"
VENV="${HKF_VENV:-$HOME/.cache/hkf-harness/venv}"
export HKF_PY=1
exec "$VENV/bin/python" "$@"
