param(
    [string]$ProjectRoot = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'

$directories = @(
    'configs',
    'data/raw',
    'data/clean',
    'data/sft',
    'data/prefs',
    'data/pretrain',
    'data/eval',
    'scripts',
    'src',
    'notebooks',
    'logs',
    'checkpoints',
    'exports',
    '.github'
)

Write-Host "Bootstrapping repository at $ProjectRoot"

foreach ($relative in $directories) {
    $path = Join-Path $ProjectRoot $relative
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
        Write-Host "Created $relative"
    }
}

$venvPath = Join-Path $ProjectRoot '.venv'
if (-not (Test-Path -LiteralPath $venvPath)) {
    Write-Host "Creating Python virtual environment at .venv"
    python -m venv $venvPath
}

Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Activate the virtual environment: .\.venv\Scripts\Activate.ps1"
Write-Host "2. Install minimal requirements: pip install -r requirements.txt"
Write-Host "3. Validate sample data: python .\scripts\validate_data.py"
Write-Host "4. Print the tree: python .\scripts\print_tree.py"

