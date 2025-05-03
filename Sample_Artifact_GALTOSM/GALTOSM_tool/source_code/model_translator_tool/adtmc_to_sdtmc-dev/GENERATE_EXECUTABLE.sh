BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir build
cd build
cmake ..
cmake --build .
cd ..
cd ..
