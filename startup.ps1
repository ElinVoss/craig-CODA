<#
.SYNOPSIS
    Craig-CODA client startup script.

.DESCRIPTION
    Brings up the full client-side Craig-CODA runtime from a clean terminal:
      1. Loads environment from .env
      2. Activates the Python virtual environment
      3. Probes the LM Studio server at 192.168.4.25:1234
      4. Starts the heartbeat pulse loop as a background job
      5. Optionally starts the TypeScript agent server
      6. Prints a status summary

    Run from D:\craig-CODA or pass -Root to override.

.PARAMETER Root
    Project root directory. Defaults to the directory containing this script.

.PARAMETER Agent
    If specified, also start the Node.js agent server on port 8001.

.PARAMETER NoPulse
    Skip starting the heartbeat pulse loop.

.EXAMPLE
    .\startup.ps1
    .\startup.ps1 -Agent
    .\startup.ps1 -Root D:\craig-CODA -Agent
#>

param(
    [string]$Root    = $PSScriptRoot,
    [switch]$Agent,
    [switch]$NoPulse
)

$ErrorActionPreference = "Stop"
Set-Location $Root

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Craig-CODA client startup" -ForegroundColor Cyan
Write-Host "  Root: $Root" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# ── 1. Load .env ─────────────────────────────────────────────────────────────
$envFile = Join-Path $Root ".env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line.Split("=", 2)
            if ($parts.Count -eq 2) {
                [System.Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), "Process")
            }
        }
    }
    Write-Host "[env]  Loaded $envFile" -ForegroundColor Green
} else {
    Write-Warning "[env]  .env not found at $envFile — using existing environment"
}

# ── 2. Activate Python venv ──────────────────────────────────────────────────
$venvActivate = Join-Path $Root ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
    Write-Host "[venv] Activated $venvActivate" -ForegroundColor Green
} else {
    Write-Host "[venv] No .venv found — using system Python" -ForegroundColor Yellow
}

# ── 3. Probe LM Studio server ────────────────────────────────────────────────
$serverUrl  = $env:LMSTUDIO_SERVER ?? "http://192.168.4.25:1234"
$probeScript = Join-Path $Root "scripts\probe_server.py"

Write-Host "[probe] Checking $serverUrl ..." -NoNewline
try {
    $probeResult = python $probeScript --url $serverUrl 2>&1
    Write-Host " $probeResult" -ForegroundColor Green
    $serverOnline = $true
} catch {
    Write-Host " OFFLINE (will run in degraded mode)" -ForegroundColor Yellow
    $serverOnline = $false
}

# ── 4. Heartbeat pulse loop ───────────────────────────────────────────────────
if (-not $NoPulse) {
    $pulseScript = Join-Path $Root "scripts\pulse.py"
    $pulseJob = Start-Job -Name "coda-pulse" -ScriptBlock {
        param($py, $script, $root)
        & $py $script --interval 300
    } -ArgumentList (Get-Command python).Source, $pulseScript, $Root

    Write-Host "[pulse] Heartbeat started (Job ID: $($pulseJob.Id))" -ForegroundColor Green
    Write-Host "        Stop with: Stop-Job -Name coda-pulse" -ForegroundColor DarkGray
}

# ── 5. Agent server (optional) ────────────────────────────────────────────────
if ($Agent) {
    $agentDir = Join-Path $Root "agent"
    if (Test-Path $agentDir) {
        $agentJob = Start-Job -Name "coda-agent" -ScriptBlock {
            param($dir)
            Set-Location $dir
            npm run dev
        } -ArgumentList $agentDir

        Write-Host "[agent] Agent server started on port 8001 (Job ID: $($agentJob.Id))" -ForegroundColor Green
        Write-Host "        Stop with: Stop-Job -Name coda-agent" -ForegroundColor DarkGray
    } else {
        Write-Warning "[agent] agent/ directory not found at $agentDir"
    }
}

# ── 6. Status summary ────────────────────────────────────────────────────────
Write-Host ""
Write-Host "─────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  Status" -ForegroundColor White
Write-Host "─────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host "  Vault      : $env:CODA_TARGET"
Write-Host "  State      : $env:CODA_STATE_DIR"
Write-Host "  Server     : $serverUrl  $(if ($serverOnline) { '(ONLINE)' } else { '(OFFLINE)' })"
Write-Host "  CODA CLI   : $(Join-Path $Root 'craig-coda')"
Write-Host ""
Write-Host "  Commands:"
Write-Host "    coda audit          — scan vault and score artifacts"
Write-Host "    coda status         — show storage and graduation readiness"
Write-Host "    python scripts\pulse.py --once   — run one heartbeat cycle"
Write-Host "    python scripts\probe_server.py   — test server connectivity"
Write-Host ""
Write-Host "  Offline survival:"
Write-Host "    All coda commands work without the server."
Write-Host "    Server inference is skipped automatically when OFFLINE."
Write-Host ""
