dir env:
Write-Output($PSScriptRoot)
$env:ZOO_PACKAGE_VERSION_PATH="$PSScriptRoot\..\..\zoo\package_version.config"
Write-Output("$PSScriptRoot\..\..\slither\cli\slithercli.py")
Write-Output("$env:ZOOTOOLS_PRO_ROOT\install\core\bin\zoo_cmd.bat")
Write-Output($env:ZOOTOOLS_PRO_ROOT)
Write-Output(">>>>>>")
& "$env:ZOOTOOLS_PRO_ROOT/install/core/bin/zoo_cmd.bat" env -- py $PSScriptRoot\..\slither\cli\slithercli.py "$argumentList" --test
exit $LASTEXITCODE