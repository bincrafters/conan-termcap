project(termcap C)
cmake_minimum_required(VERSION 3.1.2)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(${CMAKE_PROJECT_NAME} source_subfolder/termcap.c
                                  source_subfolder/termcap.h
                                  source_subfolder/tparam.c
                                  source_subfolder/version.c)
target_compile_definitions(${CMAKE_PROJECT_NAME} PRIVATE HAVE_STRING_H=1 STDC_HEADERS=1)
target_include_directories(${CMAKE_PROJECT_NAME} PRIVATE source_subfolder)

export(TARGETS ${CMAKE_PROJECT_NAME}
       NAMESPACE ${CMAKE_PROJECT_NAME}::
       FILE "${CMAKE_CURRENT_BINARY_DIR}/${CMAKE_PROJECT_NAME}Config.cmake")

install(TARGETS ${CMAKE_PROJECT_NAME}
        EXPORT ${CMAKE_PROJECT_NAME}Config
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(FILES source_subfolder/termcap.h DESTINATION include)

install(EXPORT ${CMAKE_PROJECT_NAME}Config
        DESTINATION "${CMAKE_INSTALL_LIBDIR}/${CMAKE_PROJECT_NAME}/cmake"
        NAMESPACE ${CMAKE_PROJECT_NAME}::)
