param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    [Parameter(Mandatory=$true)]
    [Hashtable]$Keys
)

if ($IsWindows) {
    # Shorten the temporary directory path to work around MSVC path lenght limit
    $env:TEMP = New-Item -ItemType Directory -Force -Path "C:\tmp"
    Write-Output $env:TEMP
}

$packages = "fiftyone_devicedetection_cloud", "fiftyone_devicedetection_examples"

if (!$Keys.TestResourceKey) {
    Write-Output "::warning file=$($MyInvocation.ScriptName),line=$($MyInvocation.ScriptLineNumber),title=No Resource Key::No resource key was provided, so integration tests will not run."
    return
} elseif (!(Test-Path $RepoName/fiftyone_devicedetection_cloud/tests/51Degrees.csv)) {
    Write-Output "::warning file=$($MyInvocation.ScriptName),line=$($MyInvocation.ScriptLineNumber),title=No CSV File::CSV file wasn't found, so cloud tests will not run."
    $packages = "fiftyone_devicedetection_examples"
}

# nightly-publish-main workflow doesn't create the examples package, so
# install-package.ps1 won't install it and its test dependencies won't get
# installed. That's why we install it here, as a special case.
if ($env:GITHUB_JOB -eq "Test") {
    Write-Output "Installing 'fiftyone_devicedetection_examples' package to install its dependencies"
    pip install $RepoName/fiftyone_devicedetection_examples || $(throw "pip install failed")
}

./python/run-integration-tests.ps1 -RepoName $RepoName -Packages $packages -Keys $Keys
$status = $LASTEXITCODE

Write-Host 'Running Selenium tests...'
try {
    # Start this repo's cloud example, pointed at the live cloud.
    Push-Location "$PSScriptRoot/../fiftyone_devicedetection_examples"
    try {
        python3 -m venv .venv
        $py = $IsWindows ? ".venv/Scripts/python.exe" : ".venv/bin/python"
        & $py -m pip install -e .
        $env:PORT = 8097
        $env:resource_key = $Keys.TestResourceKey
        $env:cloud_endpoint = "https://cloud.51degrees.com/api/v4/"
        $example = & $py -m fiftyone_devicedetection_examples.cloud.gettingstarted_web 2>&1 &
    } finally { Pop-Location }

    # Get the shared contract tests.
    if (-not (Test-Path selenium-api-tests)) {
        git clone --depth 1 https://github.com/51Degrees/selenium-api-tests.git
    }
    # Wait for the example to come up.
    curl -sS -o /dev/null --retry 5 --retry-connrefused "http://localhost:$env:PORT"

    $env:CLOUD_ROOT_URL = "https://cloud.51degrees.com/"
    $env:PAID_RESOURCE_KEY = $Keys.TestResourceKey
    $env:EXAMPLE_URL = "http://localhost:$env:PORT"
    $env:EXAMPLE_LANG = 'python'
    dotnet test selenium-api-tests -c Release --filter TestCategory=Contract
} catch {
    if ($example) { Write-Host '>>> example app output >>>'; Receive-Job $example | Out-Host; Write-Host '<<< app output <<<' }
    throw
} finally {
    if ($example) { Remove-Job -Force $example }
}
