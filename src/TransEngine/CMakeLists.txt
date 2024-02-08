cmake_minimum_required(VERSION 3.22)
project(engine)
set(CMAKE_CXX_STANDARD 17)
message(STATUS "in subdirectory CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
include_directories(${INCDIR}/TransEngine)

file(GLOB HEADER_FILES ${INCDIR}/TransEngine/*.h)
file(GLOB SOURCE_FILES ${SRCDIR}/TransEngine/*.cpp)

add_library(TransEngine SHARED ${SOURCE_FILES})

add_executable(engine test/engine-main.cpp)
target_link_libraries(TransEngine ${CPR_DLL})
target_link_libraries(engine TransEngine)

set(EXECUTABLE_OUTPUT_PATH ${EXEOUTPATH})
set(LIBRARY_OUTPUT_PATH  ${LIBOUTPATH})
