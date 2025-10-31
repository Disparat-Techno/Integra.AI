param(
    [string]$WheelPath
)

# PowerShell installer for Integra.AI on Windows.
# Tries pipx first; falls back to user-level pip install.

if (-not $WheelPath) {
  $wheel = Get-ChildItem -Path "dist" -Filter "*.whl" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
} else {
  $wheel = (Resolve-Path $WheelPath).Path
}

if (-not (Test-Path $wheel)) {
  Write-Error "Wheel não encontrado. Gere com: python -m build"
  exit 1
}

if (Get-Command pipx -ErrorAction SilentlyContinue) {
  Write-Host "Instalando via pipx..."
  pipx install $wheel
} else {
  Write-Host "pipx não encontrado. Instalando no usuário via pip..."
  python -m pip install --user $wheel
}

Write-Host "Integra.AI instalado. Tente executar: integra --help"
