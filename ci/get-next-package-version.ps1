param (
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    [Parameter(Mandatory=$true)]
    [string]$VariableName
)

./python/get-next-package-version.ps1 -RepoName $RepoName -VariableName $VariableName

exit $LASTEXITCODE
