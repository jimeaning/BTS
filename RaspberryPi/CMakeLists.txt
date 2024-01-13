cmake_minimum_required(VERSION 3.11)

project(
   test
   VERSION 0.1
   DESCRIPTION "예제프로젝트"
   LANGUAGES CXX)

add_subdirectory(library)

add_executable (program main.cpp)

target_link_libraries(program weapon stage led pthread rt)

include_directories(./pigpio)
