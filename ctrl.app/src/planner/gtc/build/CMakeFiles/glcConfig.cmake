# - Config file for 'glc' package
# It defines the following variables
#  GLC_INCLUDE_DIRS - include directories
#  GLC_LIBRARIES    - libraries to link against

# Include directory
set(GLC_INCLUDE_DIRS "/usr/local/include")

# Import the exported targets
include("/usr/local/lib/cmake/glc/glcTargets.cmake")

# Set the expected library variable
set(GLC_LIBRARIES glc)
