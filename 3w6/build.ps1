$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
python (Join-Path $PSScriptRoot "../generate.py") 3w6
if ($LASTEXITCODE -ne 0) { throw "Keymap generation failed" }

$firmwareDir = Join-Path -Path (Get-Location) -ChildPath "firmware"
if (-not (Test-Path -Path $firmwareDir)) {
    New-Item -Path $firmwareDir -ItemType Directory | Out-Null
}

docker build -t qmk-builder .
if ($LASTEXITCODE -ne 0) { throw "Docker build failed" }

$keyboardPath = Join-Path -Path (Get-Location) -ChildPath "3w6_rgb"
$firmwarePath = $firmwareDir

docker run --rm `
    -v "${keyboardPath}:/workspace/3w6_rgb:ro" `
    -v "${firmwarePath}:/workspace/firmware:rw" `
    qmk-builder `
    sh -c "cp -r /workspace/3w6_rgb /qmk_firmware/keyboards/ && qmk compile -kb 3w6_rgb -km default && cp /qmk_firmware/.build/*.uf2 /workspace/firmware/ 2>/dev/null"
if ($LASTEXITCODE -ne 0) { throw "Firmware build failed" }
