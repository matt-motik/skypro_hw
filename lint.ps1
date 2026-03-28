# lint.ps1
param(
    [Parameter(Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Paths = @(".\src"),

    [switch]$Fix,
    [switch]$NoMypy,
    [switch]$NoFlake8,
    [switch]$Detailed
)

$ErrorActionPreference = "Continue"
$LASTEXITCODE = 0

function Write-Step {
    param([string]$Message, [string]$Color = "Yellow")
    Write-Host "`n>>> $Message" -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Run-Checker {
    param(
        [string]$Name,
        [string]$CheckCommand,
        [string]$FixCommand = $null,
        [switch]$Skip
    )

    if ($Skip) {
        Write-Host "Skipping $Name..." -ForegroundColor DarkGray
        return $true
    }

    Write-Step "$Name checking..." "Yellow"

    $pathList = $Paths -join " "

    # Автофикс
    if ($Fix -and $FixCommand) {
        $fullFix = "poetry run $FixCommand $pathList"
        if ($Detailed) { Write-Host "Running fix: $fullFix" -ForegroundColor DarkGray }

        $fixOutput = Invoke-Expression $fullFix 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$Name fixed successfully"
            return $true
        } else {
            Write-Fail "$Name fix failed"
            if ($fixOutput) { $fixOutput | Out-Host }
            return $false
        }
    }

    # Проверка
    $fullCheck = "poetry run $CheckCommand $pathList"
    if ($Detailed) {
        Write-Host "Running: $fullCheck" -ForegroundColor DarkGray
    }

    $output = Invoke-Expression $fullCheck 2>&1
    $exitCode = $LASTEXITCODE

    # Определяем наличие проблем
    $hasIssues = $false

    if ($Name -eq "Mypy") {
        $hasIssues = $output | Where-Object { $_ -match "(?i)error:|no-untyped-def|undefined|incompatible" }
    }
    elseif ($Name -eq "Flake8") {
        $hasIssues = $output | Where-Object { $_ -match "^.+\:\d+\:\d+\:\s+[A-Z]\d+" }
    }
    else {
        $hasIssues = $exitCode -ne 0
    }

    if ($exitCode -eq 0 -and -not $hasIssues) {
        Write-Success "$Name passed"
        return $true
    }

    # Показ ошибки
    Write-Fail "$Name failed"

    if ($output) {
        Write-Host "`n--- $Name output ---" -ForegroundColor DarkGray
        $output | Out-Host
        Write-Host "---------------------" -ForegroundColor DarkGray
    }

    if ($FixCommand -and (-not $Fix)) {
        Write-Host "Совет: Запусти с -Fix для автоисправления" -ForegroundColor Yellow
    }

    return $false
}

# ====================== Основная логика ======================
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "                Code Quality Checker" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan

if ($Fix) { Write-Host "▶ AUTO-FIX включён" -ForegroundColor Magenta }
if ($Detailed) { Write-Host "▶ Detailed режим включён" -ForegroundColor Magenta }

# Проверка путей
$pathsOk = $true
foreach ($p in $Paths) {
    if (-not (Test-Path $p)) {
        Write-Fail "Path not found: $p"
        $pathsOk = $false
    }
}
if (-not $pathsOk) { exit 1 }

Write-Host "Проверяемые пути: $($Paths -join ', ')" -ForegroundColor Cyan

# Запускаем ВСЕ проверки, даже если предыдущие упали
$allPassed = $true

$blackResult   = Run-Checker -Name "Black"   -CheckCommand "black --check" -FixCommand "black"
$isortResult   = Run-Checker -Name "Isort"   -CheckCommand "isort --check-only" -FixCommand "isort"
$flake8Result  = $true
$mypyResult    = $true

if (-not $NoFlake8) {
    $flake8Result = Run-Checker -Name "Flake8" -CheckCommand "flake8"
}

if (-not $NoMypy) {
    $mypyResult = Run-Checker -Name "Mypy" -CheckCommand "mypy"
}

$allPassed = $blackResult -and $isortResult -and $flake8Result -and $mypyResult

# Итог
Write-Host ("=" * 70) -ForegroundColor Cyan
if ($allPassed) {
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ SOME CHECKS FAILED!" -ForegroundColor Red
    exit 1
}