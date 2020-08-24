
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
set ZOOTOOLS_ROOT=D:\dave\code\python\tools\personal\zootoolspro_install

set PYTHONPATH=%PYTHONPATH%;%ABS_PATH%;D:\dave\code\python\tools\personal\zootoolspro_install\install\core\python
set SLITHER_NODE_LIB=%nodeLib%
set SLITHER_TYPE_LIB=%pluginBase%\datatypes\generic
set DISPATCHER_LIB=%pluginBase%\dispatchers

call C:\Users\dave\AppData\Local\Programs\Python\Python37-32\python.exe %ABS_PATH%/tests/graphtest.py
