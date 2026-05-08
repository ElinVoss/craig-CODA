<#
.SYNOPSIS
    Clone D:\craig-CODA to a new drive for disk imaging.

.DESCRIPTION
    Uses robocopy to mirror the full craig-CODA client image to a new disk.
    Run this once the blank disk is attached and has a drive letter assigned.

    What is excluded from the clone:
      - .venv\         (Python venv — rebuild with: pip install -r requirements.txt)
      - agent\node_modules\ (Node deps — rebuild with: npm install)
      - __pycache__\   (Python bytecode — regenerated automatically)
      - .pytest_cache\ (test cache)
      - artifacts\checkpoints\ (large training checkpoints — copy separately if needed)

    What is always included:
      - All source code, scripts, configs, prompts, graphs
      - vault\ — authored corpus
      - .coda\ — state, manifests, pulse.log, checkpoints
      - models\ — local fallback models (if any)
      - All handoff and continuity docs

.PARAMETER Source
    Source directory. Defaults to D:\craig-CODA.

.PARAMETER Dest
    Destination root on the new disk. Example: E:\craig-CODA

.PARAMETER DryRun
    Print what would be copied without actually copying.

.EXAMPLE
    .\scripts\clone_to_disk.ps1 -Dest E:\craig-CODA
    .\scripts\clone_to_disk.ps1 -Dest E:\craig-CODA -DryRun
#>

param(
    [string]$Source = "D:\craig-CODA",
    [Parameter(Mandatory)]
    [string]$Dest,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $Source)) {
    Write-Error "Source not found: $Source"
    exit 1
}

$destDrive = Split-Path $Dest -Qualifier
if (-not (Test-Path $destDrive)) {
    Write-Error "Destination drive $destDrive not found. Attach the disk first."
    exit 1
}

Write-Host ""
Write-Host "Craig-CODA disk clone" -ForegroundColor Cyan
Write-Host "  Source : $Source"
Write-Host "  Dest   : $Dest"
if ($DryRun) { Write-Host "  Mode   : DRY RUN (no files will be written)" -ForegroundColor Yellow }
Write-Host ""

$robocopyFlags = @(
    "/E",           # copy subdirectories including empty ones
    "/COPYALL",     # copy all file attributes
    "/R:2",         # 2 retries on failure
    "/W:5",         # 5 second wait between retries
    "/NP",          # no progress percentage (cleaner terminal output)
    "/LOG+:$Source\.coda\clone.log"  # append to clone log
)

$excludeDirs = @(
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".git",
)

if ($DryRun) {
    $robocopyFlags += "/L"   # list only
}

$excludeArgs = $excludeDirs | ForEach-Object { "/XD"; $_ }

Write-Host "Starting robocopy..." -ForegroundColor Green
$exitCode = 0

try {
    & robocopy $Source $Dest @robocopyFlags @excludeArgs
    $exitCode = $LASTEXITCODE
} catch {
    Write-Error "robocopy failed: $_"
    exit 1
}

# Robocopy exit codes: 0-7 are success/informational, 8+ are errors
if ($exitCode -ge 8) {
    Write-Host ""
    Write-Host "ERROR: robocopy exit code $exitCode — check output above." -ForegroundColor Red
    exit $exitCode
}

Write-Host ""
Write-Host "Clone complete (robocopy exit code: $exitCode)." -ForegroundColor Green
Write-Host ""
Write-Host "Next steps on the new disk:"
Write-Host "  1. python -m venv .venv && .\.venv\Scripts\Activate.ps1"
Write-Host "  2. pip install -r requirements.txt"
Write-Host "  3. cd agent && npm install"
Write-Host "  4. .\startup.ps1"
