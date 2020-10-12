
@echo off
set REL_PATH=..\
set ABS_PATH=

rem // Save current directory and change to target directory
pushd %REL_PATH%

rem // Save value of CD variable (current directory)
set ABS_PATH=%CD%

rem // Restore original directory
popd

set SLITHER_PLUGIN_PATH=%ABS_PATH%\slither\plugins
set ZOOTOOLS_ROOT=F:\code\python\personal\zootoolspro
set ZOO_PACKAGE_VERSION_PATH=F:\code\python\personal\vortexUI\package_version.config
set PYTHONPATH=%PYTHONPATH%;%ABS_PATH%;F:\code\python\personal\zootoolspro\install\core\python

call py -m unittest discover -s %ABS_PATH%/tests

