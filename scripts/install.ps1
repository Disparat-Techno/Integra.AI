param(
    [string]$WheelPath
)

# PowerShell installer for Integra.AI on Windows.
# Tries pipx first; falls back to user-level pip install.

# Salva o diretório atual e muda para o diretório raiz do projeto
$currentDir = Get-Location
Set-Location (Split-Path $MyInvocation.MyCommand.Path -Parent | Split-Path -Parent)

try {
  if (-not $WheelPath) {
    $wheel = Get-ChildItem -Path "dist" -Filter "*.whl" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
  } else {
    $wheel = (Resolve-Path $WheelPath).Path
  }

  if (-not (Test-Path $wheel)) {
    Write-Host "Wheel não encontrado. Tentando construir o pacote..."

    # Verifica se o módulo 'build' está instalado
    try {
        python -c "import build" 2>$null
    } catch {
        Write-Warning "O módulo 'build' não está instalado. Instalando..."
        python -m pip install build
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Falha ao instalar o módulo 'build'. Por favor, instale-o manualmente com 'pip install build'."
            exit 1
        }
    }

    # Tenta construir o wheel
    Write-Host "Executando 'python -m build'..."
    python -m build
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha ao construir o wheel. Verifique se há erros no processo de build."
        exit 1
    }

    # Tenta encontrar o wheel novamente após a construção
    $wheel = Get-ChildItem -Path "dist" -Filter "*.whl" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { $_.FullName }
    if (-not (Test-Path $wheel)) {
      Write-Error "Wheel ainda não encontrado após a construção. Verifique a pasta 'dist'."
      exit 1
    }
    Write-Host "Wheel construído com sucesso: $wheel"
  }

  if (Get-Command pipx -ErrorAction SilentlyContinue) {
    Write-Host "Instalando via pipx..."
    pipx install $wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha na instalação via pipx."
        exit 1
    }
  } else {
    Write-Host "pipx não encontrado. Instalando no usuário via pip..."
    python -m pip install --user $wheel
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha na instalação via pip."
        exit 1
    }
  }

  Write-Host "Integra.AI instalado com sucesso. Tente executar: integra --help"
} finally {
  # Retorna ao diretório original
  Set-Location $currentDir
}
