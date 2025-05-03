BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PY_MCRL2_TO_AUT="$BASE_DIR/../../source_code/model_translator_tool/adtmc-mcrl2_to_sdtmc-prism/mcrl2-aut_to_prism-pm.py"

INPUT_FILE="$1"

python3 "$PY_MCRL2_TO_AUT" "$INPUT_FILE"
