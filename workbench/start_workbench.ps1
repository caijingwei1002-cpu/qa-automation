param(
    [string]$CodexExe = $env:CODEX_EXE,
    [int]$Port = 8765
)

$ErrorActionPreference = "Stop"
$RepositoryRoot = Split-Path -Parent $PSScriptRoot
$VirtualPython = Join-Path $RepositoryRoot ".venv\Scripts\python.exe"
$Python = if (Test-Path -LiteralPath $VirtualPython) { $VirtualPython } else { "python" }
$Arguments = @(
    (Join-Path $PSScriptRoot "server.py"),
    "--root", $RepositoryRoot,
    "--port", $Port,
    "--open"
)

if ($CodexExe) {
    $Arguments += @("--codex-exe", $CodexExe)
}

& $Python @Arguments
