
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
echo %ABS_PATH%\slither\cli\slithercli.py
echo "%ZOOTOOLS_PRO_ROOT%\install\core\bin\zoo_cmd.bat"

%ZOOTOOLS_PRO_ROOT%\install\core\bin\zoo_cmd.bat env -- py %ABS_PATH%\slither\cli\slithercli.py %*

exit /b 1