
@echo off
set REL_PATH=..\
set ABS_PATH=

rem // Save current directory and change to target directory
pushd %REL_PATH%

rem // Save value of CD variable (current directory)
set ABS_PATH=%CD%

rem // Restore original directory
popd

set pluginBase=%ABS_PATH%\slither\plugins
set nodeLib=%pluginBase%\nodes\generic

set PYTHONPATH=%PYTHONPATH%;%ABS_PATH%;%ABS_PATH%\thirdparty\zoocore;%ABS_PATH%\thirdparty\zoocore\thirdparty
set SLITHER_NODE_LIB=%nodeLib%
set SLITHER_TYPE_LIB=%pluginBase%\datatypes\generic
set DISPATCHER_LIB=%pluginBase%\dispatchers

call python %ABS_PATH%/tests/graphtest.py
