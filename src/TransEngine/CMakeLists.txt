cmake_minimum_required(VERSION 3.22)
project(engine)
set(CMAKE_CXX_STANDARD 17)
include_directories(${INCDIR}/TransEngine ${INCDIR})

file(GLOB HEADER_FILES ${INCDIR}/TransEngine/*.h)
file(GLOB SOURCE_FILES ${SRCDIR}/TransEngine/*.cpp)

add_library(TransEngine SHARED ${SOURCE_FILES})

add_executable(engine test/engine-main.cpp)
add_executable(md5-test md5.cpp ${INCDIR}/TransEngine/md5.h)
target_link_libraries(TransEngine ${CPR_DLL} utils)
target_link_libraries(engine TransEngine)

set(EXECUTABLE_OUTPUT_PATH ${EXEOUTPATH})
set(LIBRARY_OUTPUT_PATH  ${LIBOUTPATH})
