# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.7

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /var/opt/arc/ctrl.app/src/planner/gtc

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /var/opt/arc/ctrl.app/src/planner/gtc/build

# Include any dependencies generated for this target.
include test/CMakeFiles/test_glc_node.dir/depend.make

# Include the progress variables for this target.
include test/CMakeFiles/test_glc_node.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/test_glc_node.dir/flags.make

test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o: test/CMakeFiles/test_glc_node.dir/flags.make
test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o: ../test/test_glc_node.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/var/opt/arc/ctrl.app/src/planner/gtc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o"
	cd /var/opt/arc/ctrl.app/src/planner/gtc/build/test && /usr/bin/c++   $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o -c /var/opt/arc/ctrl.app/src/planner/gtc/test/test_glc_node.cpp

test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test_glc_node.dir/test_glc_node.cpp.i"
	cd /var/opt/arc/ctrl.app/src/planner/gtc/build/test && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /var/opt/arc/ctrl.app/src/planner/gtc/test/test_glc_node.cpp > CMakeFiles/test_glc_node.dir/test_glc_node.cpp.i

test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test_glc_node.dir/test_glc_node.cpp.s"
	cd /var/opt/arc/ctrl.app/src/planner/gtc/build/test && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /var/opt/arc/ctrl.app/src/planner/gtc/test/test_glc_node.cpp -o CMakeFiles/test_glc_node.dir/test_glc_node.cpp.s

test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.requires:

.PHONY : test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.requires

test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.provides: test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.requires
	$(MAKE) -f test/CMakeFiles/test_glc_node.dir/build.make test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.provides.build
.PHONY : test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.provides

test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.provides.build: test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o


# Object files for target test_glc_node
test_glc_node_OBJECTS = \
"CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o"

# External object files for target test_glc_node
test_glc_node_EXTERNAL_OBJECTS =

test/test_glc_node: test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o
test/test_glc_node: test/CMakeFiles/test_glc_node.dir/build.make
test/test_glc_node: glc/libglc_node.a
test/test_glc_node: /usr/local/lib/libgtest.a
test/test_glc_node: /usr/local/lib/libgtest_main.a
test/test_glc_node: glc/libglc_interpolation.a
test/test_glc_node: test/CMakeFiles/test_glc_node.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/var/opt/arc/ctrl.app/src/planner/gtc/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test_glc_node"
	cd /var/opt/arc/ctrl.app/src/planner/gtc/build/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_glc_node.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/test_glc_node.dir/build: test/test_glc_node

.PHONY : test/CMakeFiles/test_glc_node.dir/build

test/CMakeFiles/test_glc_node.dir/requires: test/CMakeFiles/test_glc_node.dir/test_glc_node.cpp.o.requires

.PHONY : test/CMakeFiles/test_glc_node.dir/requires

test/CMakeFiles/test_glc_node.dir/clean:
	cd /var/opt/arc/ctrl.app/src/planner/gtc/build/test && $(CMAKE_COMMAND) -P CMakeFiles/test_glc_node.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/test_glc_node.dir/clean

test/CMakeFiles/test_glc_node.dir/depend:
	cd /var/opt/arc/ctrl.app/src/planner/gtc/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /var/opt/arc/ctrl.app/src/planner/gtc /var/opt/arc/ctrl.app/src/planner/gtc/test /var/opt/arc/ctrl.app/src/planner/gtc/build /var/opt/arc/ctrl.app/src/planner/gtc/build/test /var/opt/arc/ctrl.app/src/planner/gtc/build/test/CMakeFiles/test_glc_node.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/test_glc_node.dir/depend
