# Lance le serveur de développement Django (API navigable DRF sur http://127.0.0.1:8000/).
# Usage depuis la racine P10 : .\run.ps1
# Si Windows bloque le script : powershell -ExecutionPolicy Bypass -File .\run.ps1

$ErrorActionPreference = 'Stop'

# Python du venv appelé directement : évite de dépendre de Activate.ps1 (politique d'exécution).
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$manage = Join-Path $PSScriptRoot 'p10\manage.py'

# Affiche l'erreur et garde la fenêtre ouverte (sinon elle se ferme avant qu'on puisse lire).
function Stop-OnError([string]$etape) {
    if ($LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host "ECHEC a l'etape '$etape' (code $LASTEXITCODE)." -ForegroundColor Red
        Write-Host "Lire la derniere ligne du traceback ci-dessus : c'est la cause." -ForegroundColor Yellow
        Read-Host 'Appuyer sur Entree pour fermer'
        exit $LASTEXITCODE
    }
}

# check : charge settings, apps et urls -> révèle imports cassés, include() vers un module absent, etc.
Write-Host '== manage.py check ==' -ForegroundColor Cyan
& $python $manage check
Stop-OnError 'check'

# migrate est sans effet si tout est déjà appliqué ; garantit une base à jour.
Write-Host '== manage.py migrate ==' -ForegroundColor Cyan
& $python $manage migrate
Stop-OnError 'migrate'

# runserver bloque le script : Firefox est ouvert en tâche de fond, une fois le port 8000 prêt.
$url = 'http://127.0.0.1:8000/api-auth/login/?next=/api/user/'
Start-Job -ArgumentList $url -ScriptBlock {
    param($url)
    for ($i = 0; $i -lt 20; $i++) {
        try { (New-Object Net.Sockets.TcpClient('127.0.0.1', 8000)).Close(); break }
        catch { Start-Sleep -Milliseconds 500 }
    }
    Start-Process firefox $url
} | Out-Null

Write-Host '== manage.py runserver ==' -ForegroundColor Cyan
& $python $manage runserver
Stop-OnError 'runserver'
