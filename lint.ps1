<#
.SYNOPSIS
    Python code quality checker with auto-fix capabilities using black, isort, flake8, and mypy.

.DESCRIPTION
    This script runs code quality tools on Python files. By default, it automatically fixes
    formatting issues with black and isort, then checks for style and type errors.
    Use -NoFix to only check without making changes.

.PARAMETER Paths
    Paths to files or directories to check (default: .\src). Accepts multiple paths.

.PARAMETER NoFix
    Disable auto-fixing. Tools will run in check-only mode.

.PARAMETER NoMypy
    Skip mypy type checking.

.PARAMETER NoFlake8
    Skip flake8 style checking.

.EXAMPLE
    .\lint.ps1
    Runs with default settings: fixes .\src with black/isort, then checks flake8 and mypy.

.EXAMPLE
    .\lint.ps1 .\src\main.py .\tests -NoFix
    Checks only specified paths without auto-fixing.

.EXAMPLE
    .\lint.ps1 -NoMypy -NoFlake8
    Only runs black and isort (with auto-fix enabled by default).
#>

param(
    [Parameter(Position = 0, ValueFromRemainingArguments = $true)]
    [string[]]$Paths = @(".\src"),

    [switch]$NoFix,
    [switch]$NoMypy,
    [switch]$NoFlake8
)

$ErrorActionPreference = "Continue"

# Set console encoding to UTF-8 for proper emoji display
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# ====================== Helper Functions ======================

function Write-Step
{
    param([string]$Message, [string]$Color = "Yellow")
    Write-Host "`n>>> $Message" -ForegroundColor $Color
}

function Write-Success
{
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-ErrorMsg
{
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Run-Black
{
    param(
        [string]$Name,
        [string]$CommandBase
    )

    Write-Step "$Name checking..." "Yellow"

    # Собираем все пути в одну строку (с пробелами)
    $pathList = $Paths -join " "

    # Команда
    $fullCommand = "poetry run $CommandBase $pathList"

    Write-Host "`n--- $Name Output ---" -ForegroundColor DarkGray

    # Black выводит в stderr, но мы просто выполняем команду и показываем вывод
    Invoke-Expression $fullCommand

    Write-Host "---------------------" -ForegroundColor DarkGray

    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0)
    {
        Write-Success "$Name passed"
        return $true
    }

    if ($CommandBase -and $NoFix)
    {
        Write-Host "Tip: Run without -NoFix to auto-fix" -ForegroundColor Yellow
    }

    return $false
}

function Run-Checker
{
    param(
        [string]$Name,
        [string]$CheckCommand,
        [string]$FixCommand = $null,
        [switch]$Skip
    )

    if ($Skip)
    {
        Write-Host "Skipping $Name..." -ForegroundColor DarkGray
        return $true
    }

    Write-Step "$Name checking..." "Yellow"

    $pathList = $Paths -join " "

    # ====================== AUTO-FIX MODE ======================
    if (-not $NoFix -and $FixCommand)
    {
        $fullFix = "poetry run $FixCommand $pathList"

        Write-Host "`n--- $Name Output ---" -ForegroundColor DarkGray

        # Для Isort в режиме автофикса: вывод в stdout, просто выполняем

        $output = Invoke-Expression $fullFix 2>&1
        # Показываем захваченный вывод
        if ($output)
        {
            $output | ForEach-Object {
                Write-Host $_.ToString()
            }
        }
        else
        {
            Write-Host "(no output)" -ForegroundColor DarkGray
        }


        Write-Host "---------------------" -ForegroundColor DarkGray

        $exitCode = $LASTEXITCODE

        if ($exitCode -ne 0)
        {
            Write-ErrorMsg "$Name fix failed"
            return $false
        }

        Write-Success "$Name fixed"
        return $true
    }

    # ====================== CHECK MODE ======================
    $fullCheck = "poetry run $CheckCommand $pathList"

    Write-Host "`n--- $Name Output ---" -ForegroundColor DarkGray

    # Для check mode нужно захватить вывод для анализа

    if ($Name -eq "Isort")
    {
        Invoke-Expression $fullCheck
    }
    else
    {
        $output = Invoke-Expression $fullCheck 2>&1
    }

    # Показываем захваченный вывод
    if ($output)
    {
        $output | ForEach-Object {
            Write-Host $_.ToString()
        }
    }
    else
    {
        Write-Host "(no output)" -ForegroundColor DarkGray
    }

    Write-Host "---------------------" -ForegroundColor DarkGray

    $exitCode = $LASTEXITCODE

    # Определяем наличие ошибок
    $hasIssues = $false

    if ($Name -eq "Mypy")
    {
        # Mypy: проверяем наличие паттернов ошибок в выводе
        $hasIssues = ($output | Where-Object {
            $_ -match "(?i)error:|no-untyped-def|undefined|incompatible"
        }).Count -gt 0
    }
    elseif ($Name -eq "Flake8")
    {
        # Flake8: ненулевой exit code означает ошибки
        $hasIssues = $exitCode -ne 0
    }
    elseif ($Name -eq "Isort")
    {
        # Isort в check mode: ненулевой exit code означает ошибки
        $hasIssues = $exitCode -ne 0
    }
    else
    {
        $hasIssues = $exitCode -ne 0
    }

    if (-not $hasIssues)
    {
        Write-Success "$Name passed"
        return $true
    }

    Write-ErrorMsg "$Name failed"

    if ($FixCommand -and $NoFix)
    {
        Write-Host "Tip: Run without -NoFix to auto-fix" -ForegroundColor Yellow
    }

    return $false
}

# ====================== Main Script ======================

# Header
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "Code Quality Checker" -ForegroundColor Cyan
Write-Host ("=" * 60) -ForegroundColor Cyan

# Show current mode
if (-not $NoFix)
{
    Write-Host "▶ AUTO-FIX включён" -ForegroundColor Magenta
}
if ($NoFix)
{
    Write-Host "▶ AUTO-FIX отключён (только проверка)" -ForegroundColor DarkGray
}
if ($NoMypy)
{
    Write-Host "▶ Mypy пропущен" -ForegroundColor DarkGray
}
if ($NoFlake8)
{
    Write-Host "▶ Flake8 пропущен" -ForegroundColor DarkGray
}

# Проверка существования всех переданных путей
$allPathsExist = $true
foreach ($p in $Paths)
{
    if (-not (Test-Path $p))
    {
        Write-ErrorMsg "Path not found: $p"
        $allPathsExist = $false
    }
}

if (-not $allPathsExist)
{
    Write-Host "Aborting due to missing paths." -ForegroundColor Red
    exit 1
}

Write-Host "Checking paths: $( $Paths -join ', ' )" -ForegroundColor Cyan

$BlackPassed = $true
$IsortPassed = $true
$Flake8Passed = $true
$MypyPassed = $true

# === Black ===
if ($NoFix)
{
    $BlackPassed = Run-Black -Name "Black" -CommandBase "black --check"
}
else
{
    $BlackPassed = Run-Black -Name "Black" -CommandBase "black"
}

# === Isort ===
$IsortPassed = Run-Checker -Name "Isort" -CheckCommand "isort --check-only" -FixCommand "isort"

# === Flake8 ===
if (-not $NoFlake8)
{
    $Flake8Passed = Run-Checker -Name "Flake8" -CheckCommand "flake8"
}
else
{
    Write-Host "Skipping Flake8..." -ForegroundColor DarkGray
}

# === Mypy ===
if (-not $NoMypy)
{
    $MypyPassed = Run-Checker -Name "Mypy" -CheckCommand "mypy"
}
else
{
    Write-Host "Skipping Mypy..." -ForegroundColor DarkGray
}

# ====================== Итог ======================
$allPassed = $BlackPassed -and $IsortPassed -and $Flake8Passed -and $MypyPassed
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
if ($allPassed)
{
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    exit 0
}
else
{
    Write-Host "❌ SOME CHECKS FAILED!" -ForegroundColor Red
    exit 1
}