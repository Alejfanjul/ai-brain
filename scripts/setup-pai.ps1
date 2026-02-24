# Setup PAI (Personal AI Infrastructure) from ai-brain repo
# Run this ONCE on each new Windows machine after cloning ai-brain
#
# Creates directory junctions (preferred) or copies so that git pull updates everything.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\setup-pai.ps1

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $ScriptDir
$ClaudeDir = Join-Path $env:USERPROFILE ".claude"
$ConfigSrc = Join-Path $RepoDir ".claude-config"
$PaiSrc = Join-Path $RepoDir "pai"

Write-Host "Setting up PAI..." -ForegroundColor Cyan
Write-Host "   Repo: $RepoDir"
Write-Host ""

# Check if config exists in repo
if (-not (Test-Path $ConfigSrc)) {
    Write-Host ".claude-config not found in ai-brain repo" -ForegroundColor Red
    exit 1
}

# Ensure ~/.claude/ exists
if (-not (Test-Path $ClaudeDir)) {
    New-Item -ItemType Directory -Path $ClaudeDir | Out-Null
    Write-Host "   Created $ClaudeDir" -ForegroundColor Green
}

function Link-Item {
    param(
        [string]$Source,
        [string]$Target,
        [string]$Label,
        [bool]$IsDirectory = $true
    )

    if (-not (Test-Path $Source)) {
        Write-Host "   SKIP $Label (source not found)" -ForegroundColor Yellow
        return
    }

    # Backup existing non-junction target
    if (Test-Path $Target) {
        $item = Get-Item $Target -Force
        $isJunction = $item.Attributes -band [System.IO.FileAttributes]::ReparsePoint

        if (-not $isJunction) {
            $backup = "$Target.bak-$(Get-Date -Format 'yyyyMMdd')"
            Write-Host "   Backing up existing $Label to $backup" -ForegroundColor Yellow
            Move-Item $Target $backup -Force
        } else {
            # Remove existing junction to recreate
            if ($IsDirectory) {
                cmd /c "rmdir `"$Target`"" 2>$null
            } else {
                Remove-Item $Target -Force
            }
        }
    }

    if ($IsDirectory) {
        # Directory junction (no admin required)
        cmd /c "mklink /J `"$Target`" `"$Source`"" | Out-Null
        if ($LASTEXITCODE -eq 0 -or (Test-Path $Target)) {
            Write-Host "   OK $Label (junction)" -ForegroundColor Green
        } else {
            # Fallback: copy
            Copy-Item -Recurse $Source $Target
            Write-Host "   OK $Label (copied - junctions not available)" -ForegroundColor Yellow
        }
    } else {
        # File: try symlink, fallback to copy
        try {
            New-Item -ItemType SymbolicLink -Path $Target -Target $Source -ErrorAction Stop | Out-Null
            Write-Host "   OK $Label (symlink)" -ForegroundColor Green
        } catch {
            Copy-Item $Source $Target
            Write-Host "   OK $Label (copied - symlinks require developer mode)" -ForegroundColor Yellow
        }
    }
}

# Link hooks directory
Write-Host "Linking hooks..." -ForegroundColor White
$hooksSrc = Join-Path $ConfigSrc "hooks"
$hooksDst = Join-Path $ClaudeDir "hooks"
Link-Item -Source $hooksSrc -Target $hooksDst -Label "hooks/" -IsDirectory $true

# Link settings.json
Write-Host "Linking settings..." -ForegroundColor White
$settingsSrc = Join-Path $ConfigSrc "settings.json"
$settingsDst = Join-Path $ClaudeDir "settings.json"
Link-Item -Source $settingsSrc -Target $settingsDst -Label "settings.json" -IsDirectory $false

# Link global CLAUDE.md
$claudeMdSrc = Join-Path $ConfigSrc "CLAUDE.md"
if (Test-Path $claudeMdSrc) {
    Write-Host "Linking global CLAUDE.md..." -ForegroundColor White
    $claudeMdDst = Join-Path $ClaudeDir "CLAUDE.md"
    Link-Item -Source $claudeMdSrc -Target $claudeMdDst -Label "CLAUDE.md" -IsDirectory $false
}

# Link skills directory
Write-Host "Linking skills..." -ForegroundColor White
$skillsSrc = Join-Path $ConfigSrc "skills"
$skillsDst = Join-Path $ClaudeDir "skills"
if (Test-Path $skillsSrc) {
    Link-Item -Source $skillsSrc -Target $skillsDst -Label "skills/" -IsDirectory $true
}

# Link PAI context directory
Write-Host "Linking PAI context..." -ForegroundColor White
$paiDst = Join-Path $ClaudeDir "pai"
Link-Item -Source $PaiSrc -Target $paiDst -Label "pai/" -IsDirectory $true

# Check for bun
Write-Host ""
$bunPath = Join-Path $env:USERPROFILE ".bun\bin\bun.exe"
if (Test-Path $bunPath) {
    Write-Host "Bun found: $bunPath" -ForegroundColor Green
} elseif (Get-Command bun -ErrorAction SilentlyContinue) {
    Write-Host "Bun found: $(Get-Command bun | Select-Object -ExpandProperty Source)" -ForegroundColor Green
} else {
    Write-Host "Bun not found. Install with:" -ForegroundColor Yellow
    Write-Host '   powershell -c "irm bun.sh/install.ps1 | iex"'
}

Write-Host ""
Write-Host "PAI setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Links created:" -ForegroundColor White
@("hooks", "skills", "pai") | ForEach-Object {
    $p = Join-Path $ClaudeDir $_
    if (Test-Path $p) { Write-Host "   $p -> $(Get-Item $p -Force | Select-Object -ExpandProperty Target)" -ForegroundColor Gray }
}
@("settings.json", "CLAUDE.md") | ForEach-Object {
    $p = Join-Path $ClaudeDir $_
    if (Test-Path $p) { Write-Host "   $p" -ForegroundColor Gray }
}
Write-Host ""
Write-Host "Restart Claude Code and check if context loads." -ForegroundColor Cyan
