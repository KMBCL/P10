# Lance le serveur de développement Django (API navigable DRF sur http://127.0.0.1:8000/).
# Usage depuis la racine P10 : .\run.ps1
# Si Windows bloque le script : powershell -ExecutionPolicy Bypass -File .\run.ps1

$ErrorActionPreference = 'Stop'

# Python du venv appelé directement : évite de dépendre de Activate.ps1 (politique d'exécution).
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$manage = Join-Path $PSScriptRoot 'p10\manage.py'

# migrate est sans effet si tout est déjà appliqué ; garantit une base à jour.
& $python $manage migrate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

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

& $python $manage runserver
