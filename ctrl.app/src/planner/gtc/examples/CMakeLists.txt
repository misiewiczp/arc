
include_directories(${PROJECT_SOURCE_DIR}/glc/include)

add_executable(nonholonomic-car-demo nonholonomic-car-demo.cpp)
target_link_libraries(nonholonomic-car-demo glc_planner_core glc_logging)

add_executable(gtc gtc.cpp)
target_link_libraries(gtc glc_planner_core glc_logging lcm)

include_directories(../../../lcm/cpp)


