# Create a distributable zip containing the app and spells directories and README
param(
    [string]$OutDir = "dist"
)

$repo = (Get-Location).Path
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$timestamp = Get-Date -Format yyyyMMddHHmmss
$zip = Join-Path $OutDir "orb-dist-$timestamp.zip"

$paths = @()
if (Test-Path "$repo\app") { $paths += "$repo\app" }
if (Test-Path "$repo\spells") { $paths += "$repo\spells" }
if (Test-Path "$repo\README.md") { $paths += "$repo\README.md" }

if ($paths.Count -eq 0) { Write-Error "No content to package"; exit 1 }

Compress-Archive -Path $paths -DestinationPath $zip -Force
Write-Output "Created $zip"
exit 0
