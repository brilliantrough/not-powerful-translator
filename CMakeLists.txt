cmake_minimum_required(VERSION 3.22)
project(not-powerful-translator)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# add include directory
include_directories(include)
set(CMAKE_PREFIX_PATH "D:/Qt/5.14.2/mingw73_64")
if (CMAKE_BUILD_TYPE MATCHES "Debug")
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)
    set(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)
else ()
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/release-bin)
    set(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/release-bin)
endif ()
if (MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
    message(STATUS "the cmake flags ${CMAKE_CXX_FLAGS}")
    message(STATUS "the msvc ${MSVC}")
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/release-bin-vs)
    set(LIBRARY_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/release-bin-vs)
    set(CPR_DLL "${LIBRARY_OUTPUT_PATH}/${CMAKE_BUILD_TYPE}/cpr.dll")
    add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
    add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
else ()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libstdc++")
    set(CPR_DLL "${LIBRARY_OUTPUT_PATH}/libcpr.dll")
    message(STATUS "the cmake flags ${CMAKE_CXX_FLAGS}")
endif ()

# set cpr dll

# set mouse selection files
set(ENCODE_CONVERT_FILES include/mouse_selection/EncodeConvert.h)
set(MOUSE_SELECTION_FILES src/mouse_selection/MouseSelection.cpp include/mouse_selection/MouseSelection.h ${ENCODE_CONVERT_FILES})

find_package(Qt5 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED
        )

# set library
add_library(utils SHARED src/mouse_selection/EncodeConvert.cpp)

add_executable(not-powerful-translator WIN32
        main.cpp mainwindow.cpp mainwindow.h mainwindow.ui
        ${MOUSE_SELECTION_FILES}
        resource.rc
        )

target_link_libraries(not-powerful-translator
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        TransEngine
        utils
        )


if (WIN32)
    set(DEBUG_SUFFIX)
    if (MSVC AND CMAKE_BUILD_TYPE MATCHES "Debug")
        set(DEBUG_SUFFIX "d")
    endif ()
    set(QT_INSTALL_PATH "${CMAKE_PREFIX_PATH}")
    if (NOT EXISTS "${QT_INSTALL_PATH}/bin")
        set(QT_INSTALL_PATH "${QT_INSTALL_PATH}/..")
        if (NOT EXISTS "${QT_INSTALL_PATH}/bin")
            set(QT_INSTALL_PATH "${QT_INSTALL_PATH}/..")
        endif ()
    endif ()
    if (EXISTS "${QT_INSTALL_PATH}/plugins/platforms/qwindows${DEBUG_SUFFIX}.dll")
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E make_directory
                "$<TARGET_FILE_DIR:${PROJECT_NAME}>/plugins/platforms/")
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                "${QT_INSTALL_PATH}/plugins/platforms/qwindows${DEBUG_SUFFIX}.dll"
                "$<TARGET_FILE_DIR:${PROJECT_NAME}>/plugins/platforms/")
    endif ()
    foreach (QT_LIB Core Gui Widgets)
        add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                "${QT_INSTALL_PATH}/bin/Qt5${QT_LIB}${DEBUG_SUFFIX}.dll"
                "$<TARGET_FILE_DIR:${PROJECT_NAME}>")
    endforeach (QT_LIB)
endif ()

# for sub directory variable
set(EXEOUTPATH ${EXECUTABLE_OUTPUT_PATH})
set(LIBOUTPATH ${LIBRARY_OUTPUT_PATH})
set(INCDIR ${CMAKE_SOURCE_DIR}/include)
set(SRCDIR ${CMAKE_SOURCE_DIR}/src)

# add subdirectory
add_subdirectory(src/mouse_selection)
add_subdirectory(src/TransEngine)
add_subdirectory(src/cpr)
