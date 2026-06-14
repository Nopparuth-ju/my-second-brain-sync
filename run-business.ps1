$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$baseOutputDir = "02_SOURCE\BUSINESS_FEEDS"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  [*] DEEP LEARNING BUSINESS ANALYST [*]" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

Write-Host "Please select the domain you want to research:" -ForegroundColor Yellow
Write-Host "[1] Business Models & Economics"
Write-Host "[2] Behavioral Psychology & Consumer Behavior"
Write-Host "[3] Systems Thinking & Operations"
Write-Host "[4] Leadership & Culture"
Write-Host "[5] Risk Management & Antifragility"

$selection = Read-Host "`nEnter category number (1-5)"

$agentName = ""
$categoryFolder = ""

switch ($selection) {
    "1" { $agentName = "BusinessModelAnalyst"; $categoryFolder = "Business Models" }
    "2" { $agentName = "BehavioralAnalyst"; $categoryFolder = "Behavioral Psychology" }
    "3" { $agentName = "SystemsAnalyst"; $categoryFolder = "Systems & Operations" }
    "4" { $agentName = "CultureAnalyst"; $categoryFolder = "Culture & Leadership" }
    "5" { $agentName = "RiskAnalyst"; $categoryFolder = "Risk & Antifragility" }
    default {
        Write-Host "[x] Invalid selection. Exiting." -ForegroundColor Red
        exit
    }
}

$agentDir = ".agents\$agentName"
$instructionFile = "$agentDir\instruction.md"
$outputDir = "$baseOutputDir\$categoryFolder"

if (-not (Test-Path $instructionFile)) {
    Write-Host "[x] Instruction file not found: $instructionFile" -ForegroundColor Red
    exit
}

Write-Host "`n[>] You selected: $categoryFolder" -ForegroundColor Green
$topicsInput = Read-Host "`nEnter the topics/companies to research (comma separated, e.g., 'Apple, Tesla, Jobs-to-be-Done')"

if ([string]::IsNullOrWhiteSpace($topicsInput)) {
    Write-Host "[x] No topics entered. Exiting." -ForegroundColor Red
    exit
}

$topics = $topicsInput -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }

if (-not (Test-Path $outputDir)) { 
    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null 
}

$today = Get-Date -Format "yyyy-MM-dd"

foreach ($topic in $topics) {
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host "[>] Starting deep research on: " -NoNewline
    Write-Host "$topic" -ForegroundColor Yellow
    Write-Host "    Domain: $categoryFolder" -ForegroundColor DarkGray
    
    $safeTopic = $topic -replace '[\\/*?:"<>|]', '-'
    $targetFile = "$outputDir\$today - $safeTopic.md"

    $prompt = "You are the $agentName. I need you to deeply research the following topic: `"$topic`". `n"
    $prompt += "Read .agents/$agentName/instruction.md and follow it strictly. `n"
    $prompt += "Research the topic thoroughly using your tools, structure it exactly as requested in the instruction, and save the final Markdown report to: `"$targetFile`" `n"
    $prompt += "Do not just print the report to the terminal. You MUST use your write_to_file tool to save it EXACTLY ONCE."

    Write-Host "[...] Invoking AI Agent... (This may take a few minutes)" -ForegroundColor DarkGray

    # Execute agy
    $process = Start-Process -FilePath "agy" -ArgumentList "--dangerously-skip-permissions", "-p", "`"$prompt`"" -NoNewWindow -Wait -PassThru

    if ($process.ExitCode -eq 0) {
        if (Test-Path $targetFile) {
            Write-Host "`n[v] Research complete! Report saved to: $targetFile" -ForegroundColor Green
        } else {
            Write-Host "`n[x] AI Agent finished but failed to create the target file: $targetFile" -ForegroundColor Red
        }
    } else {
        Write-Host "`n[x] AI Agent process failed with exit code $($process.ExitCode)" -ForegroundColor Red
    }
}

Write-Host "`n[v] All research tasks completed!" -ForegroundColor Green
