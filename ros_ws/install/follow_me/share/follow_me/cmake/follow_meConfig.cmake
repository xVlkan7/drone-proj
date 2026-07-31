# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_follow_me_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED follow_me_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(follow_me_FOUND FALSE)
  elseif(NOT follow_me_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(follow_me_FOUND FALSE)
  endif()
  return()
endif()
set(_follow_me_CONFIG_INCLUDED TRUE)

# output package information
if(NOT follow_me_FIND_QUIETLY)
  message(STATUS "Found follow_me: 0.0.0 (${follow_me_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'follow_me' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT follow_me_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(follow_me_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${follow_me_DIR}/${_extra}")
endforeach()
