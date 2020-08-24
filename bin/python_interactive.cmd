
@echo off
setlocal
set REL_PATH=..\
set ABS_PATH=

rem // Save current directory and change to target directory
pushd %REL_PATH%

rem // Save value of CD variable (current directory)
set ABS_PATH=%CD%

rem // Restore original directory
popd
echo %ABS_PATH%
set ZOOTOOLS_ROOT=F:\code\python\personal\zootoolspro
set pluginBase=%ABS_PATH%\slither\plugins
set nodeLib=%pluginBase%\nodes\generic
set PYTHONPATH=%PYTHONPATH%;%ABS_PATH%;%ZOOTOOLS_ROOT%\install\core\python
set SLITHER_NODE_LIB=%nodeLib%
set SLITHER_TYPE_LIB=%pluginBase%\datatypes\generic
set DISPATCHER_LIB=%pluginBase%\dispatchers

call %PYTHON_INTEPRETER% %ABS_PATH%/slither/example.py