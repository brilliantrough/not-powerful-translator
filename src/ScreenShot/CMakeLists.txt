cmake_minimum_required(VERSION 3.22)
project(ScreenShot)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_PREFIX_PATH "D:/Qt/5.14.2/mingw73_64")
include_directories(${INCDIR}/ScreenShot)
file(GLOB HEADER_FILES ${INCDIR}/ScreenShot/*.h)
file(GLOB SOURCE_FILES ${SRCDIR}/ScreenShot/*.cpp)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
find_package(Qt5 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED
)
add_library(ScreenShot SHARED ${SOURCE_FILES})

add_executable(ScreenShot_main WIN32 ScreenShot_main/ScreenShot_main.cpp ${INCDIR}/ScreenShot/ScreenShot.h)
#target_link_libraries(ScreenShot ${CPR_DLL})
target_link_libraries(ScreenShot_main
        ScreenShot
        Qt5::Core
        Qt5::Gui
        Qt5::Widgets
        )

set(EXECUTABLE_OUTPUT_PATH ${EXEOUTPATH})
set(LIBRARY_OUTPUT_PATH  ${LIBOUTPATH})
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
