
@echo off
set REL_PATH=..\
set ABS_PATH=

rem // Save current directory and change to target directory
pushd %REL_PATH%

rem // Save value of CD variable (current directory)
set ABS_PATH=%CD%

rem // Restore original directory
popd

set ZOO_PACKAGE_VERSION_PATH=%ABS_PATH%\zoo\package_version.config

call py -i %ZOOTOOLS_ROOT%\install\core\scripts\zoo_cmd.py env --apply
