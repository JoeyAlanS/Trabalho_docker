# Script PowerShell para Teste Rápido - Link Extractor
# Autor: Joey
# Uso: .\quick_test.ps1 -Scenario python-cache -NumUsers 10

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("python-cache", "python-no-cache", "ruby-cache", "ruby-no-cache")]
    [string]$Scenario,
    
    [int]$NumUsers = 10
)

$scenarioMap = @{
    "python-cache" = @{
        "compose" = "docker-compose.python-cache.yml"
        "name" = "Python com Cache"
        "port" = 5000
    }
    "python-no-cache" = @{
        "compose" = "docker-compose.python-no-cache.yml"
        "name" = "Python sem Cache"
        "port" = 5000
    }
    "ruby-cache" = @{
        "compose" = "docker-compose.ruby-cache.yml"
        "name" = "Ruby com Cache"
        "port" = 4567
    }
    "ruby-no-cache" = @{
        "compose" = "docker-compose.ruby-no-cache.yml"
        "name" = "Ruby sem Cache"
        "port" = 4567
    }
}

$config = $scenarioMap[$Scenario]

Write-Host "`n" -ForegroundColor Yellow
Write-Host "=========================================================================" -ForegroundColor Green
Write-Host "🧪 TESTE RÁPIDO - $($config.name)" -ForegroundColor Green
Write-Host "=========================================================================" -ForegroundColor Green
Write-Host "`n"

Write-Host "📊 Configuração:" -ForegroundColor Cyan
Write-Host "   Cenário: $($config.name)" -ForegroundColor White
Write-Host "   Usuários: $NumUsers" -ForegroundColor White
Write-Host "   Duração: 2 minutos (120 segundos)" -ForegroundColor White
Write-Host "`n=========================================================================" -ForegroundColor Green
Write-Host "`n"

# Step 1: Iniciar serviços
Write-Host "1️⃣  Iniciando containers Docker..." -ForegroundColor Yellow
& docker-compose -f $config.compose up -d --build

Write-Host "`n   ⏳ Aguardando 10 segundos para estabilizar..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Step 2: Executar teste
Write-Host "`n2️⃣  Executando teste Locust (2 minutos)..." -ForegroundColor Yellow
$apiUrl = "http://localhost:$($config.port)"
$rampUp = [math]::Max(1, [math]::Floor($NumUsers / 5))

$locustCmd = @(
    "locust -f locustfile.py --headless",
    "-u $NumUsers",
    "-r $rampUp",
    "-t 120",
    "-H $apiUrl"
) -join " "

Invoke-Expression $locustCmd

# Step 3: Parar serviços
Write-Host "`n3️⃣  Parando containers Docker..." -ForegroundColor Yellow
& docker-compose -f $config.compose down

Write-Host "`n=========================================================================" -ForegroundColor Green
Write-Host "✅ TESTE CONCLUÍDO!" -ForegroundColor Green
Write-Host "=========================================================================" -ForegroundColor Green
Write-Host "`n"
Write-Host ""
