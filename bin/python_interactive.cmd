
@echo off
set REL_PATH=..\
set ABS_PATH=

rem // Save current directory and change to target directory
pushd %REL_PATH%

rem // Save value of CD variable (current directory)
set ABS_PATH=%CD%

rem // Restore original directory
popd

set ZOOTOOLS_ROOT=F:\code\python\personal\zootoolspro
set ZOO_PACKAGE_VERSION_PATH=%ABS_PATH%\zoo\package_version.config
set PYTHONPATH=%PYTHONPATH%;%ABS_PATH%;%ZOOTOOLS_ROOT%\install\core\python
set SLITHER_PLUGIN_PATH=%ABS_PATH%\slither\plugins


call py %ABS_PATH%/slither/example.py
call py