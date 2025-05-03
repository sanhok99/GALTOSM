BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

EXC_LOC="$BASE_DIR/../../source_code/model_translator_tool/adtmc_to_sdtmc-dev/build"

INPUT_FILE="$1"

MODEL_TYPE="$2"

"$EXC_LOC/ADTMC_TO_SDTMC" "$BASE_DIR/$INPUT_FILE" "$MODEL_TYPE"

