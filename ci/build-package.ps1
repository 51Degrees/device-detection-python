param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
	[Parameter(Mandatory=$true)]
    [string]$Version
)

# GitVersion emits a SemVer string. For `main` this is a clean release (e.g.
# 4.6.0) and for `version/*` branches a recognised prerelease (e.g. 4.6.0-alpha.1)
# - both of which setuptools/PEP 440 accept. Any other branch produces an
# arbitrary prerelease label taken from the branch name (e.g.
# 4.6.0-fix-utm-parameters.1), which is NOT a valid PEP 440 version, so modern
# setuptools rejects it and `python -m build` fails. Convert such a label into a
# PEP 440 local-version segment so the package still builds on any branch.
if ($Version -match '^(\d+\.\d+\.\d+)-(?!(?:alpha|beta|rc)[.0-9]*$)(.+)$') {
    $local = ($Matches[2] -replace '[^0-9A-Za-z]+', '.').Trim('.')
    $Version = "$($Matches[1])+$local"
    Write-Output "Normalized non-PEP 440 branch version to '$Version'"
}

$packages = "fiftyone_devicedetection_shared", "fiftyone_devicedetection_cloud", "fiftyone_devicedetection_onpremise", "fiftyone_devicedetection"
./python/build-package-pypi.ps1 -RepoName $RepoName -Version $Version -Packages $packages

exit $LASTEXITCODE
