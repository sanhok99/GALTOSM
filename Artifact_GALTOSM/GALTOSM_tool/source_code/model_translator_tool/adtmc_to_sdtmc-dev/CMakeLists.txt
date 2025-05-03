cmake_minimum_required(VERSION 3.10)

# Set the project
project(ADTMC_TO_SDTMC)

# Add the executable
add_executable(
    ${PROJECT_NAME}
    src/main.cpp
    src/aut.cpp
    src/aut_read.cpp
    src/aut_convert.cpp
)

target_include_directories(
    ${PROJECT_NAME}
    PUBLIC
    ${PROJECT_SOURCE_DIR}/include
    ${PROJECT_SOURCE_DIR}/thirdparty
)

# Specify the c++17 standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set the generator to Ninja
set(CMAKE_GENERATOR "Ninja")