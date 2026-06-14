$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$baseOutputDir = "02_SOURCE\BUSINESS_FEEDS"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  [*] DEEP LEARNING BUSINESS ANALYST [*]" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

Write-Host "Please select the domain(s) you want to research:" -ForegroundColor Yellow
Write-Host "[1] Business Models & Economics"
Write-Host "[2] Behavioral Psychology & Consumer Behavior"
Write-Host "[3] Systems Thinking & Operations"
Write-Host "[4] Leadership & Culture"
Write-Host "[5] Risk Management & Antifragility"

$selectionInput = Read-Host "`nEnter category number(s) (e.g., '1', '1,3', '1-5', or 'all')"

$selectedCategories = @()
if ($selectionInput -match "(?i)all") {
    $selectedCategories = 1..5
} else {
    $parts = $selectionInput -split ',' | ForEach-Object { $_.Trim() }
    foreach ($part in $parts) {
        if ($part -match "^(\d+)\s*-\s*(\d+)$") {
            $start = [int]$matches[1]
            $end = [int]$matches[2]
            if ($start -le $end) { $selectedCategories += $start..$end }
        } elseif ($part -match "^\d+$") {
            $selectedCategories += [int]$part
        }
    }
}

$selectedCategories = $selectedCategories | Where-Object { $_ -ge 1 -and $_ -le 5 } | Select-Object -Unique

if ($selectedCategories.Count -eq 0) {
    Write-Host "[x] Invalid selection. Exiting." -ForegroundColor Red
    exit
}

$topicsInput = Read-Host "`nEnter the topics/companies to research (comma separated, e.g., 'Apple, Tesla', or type 'suggest')"

if ([string]::IsNullOrWhiteSpace($topicsInput)) {
    Write-Host "[x] No topics entered. Exiting." -ForegroundColor Red
    exit
}

$topics = @()
if ($topicsInput -match "(?i)^suggest$") {
    Write-Host "[...] Reading your Business Curriculum to find the next best topic..." -ForegroundColor DarkGray
    $curriculumFile = "$baseOutputDir\00_Business_Curriculum.md"
    if (Test-Path $curriculumFile) {
        $lines = Get-Content $curriculumFile
        $foundSuggest = $false
        foreach ($line in $lines) {
            if ($line -match "^\d+\.\s+\*\*([^*]+)\*\*") {
                $candidate = $matches[1].Trim()
                $safeCandidate = $candidate -replace '[\\/*?:"<>|]', '-'
                $existing = Get-ChildItem -Path $baseOutputDir -Recurse -Filter "*$safeCandidate.md" -ErrorAction SilentlyContinue
                if ($null -eq $existing -or $existing.Count -eq 0) {
                    $topics += $candidate
                    Write-Host "[v] Suggestion selected: $candidate" -ForegroundColor Green
                    $foundSuggest = $true
                    break
                }
            }
        }
        if (-not $foundSuggest) {
            Write-Host "[x] Could not find any unresearched topics in the curriculum. Please enter manually." -ForegroundColor Red
            exit
        }
    } else {
        Write-Host "[x] Curriculum file not found at $curriculumFile" -ForegroundColor Red
        exit
    }
} else {
    $topics = $topicsInput -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
}

$today = Get-Date -Format "yyyy-MM-dd"

foreach ($topic in $topics) {
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host "[>] Starting deep research on: " -NoNewline
    Write-Host "$topic" -ForegroundColor Yellow

    foreach ($catNum in $selectedCategories) {
        $agentName = ""
        $categoryFolder = ""
        switch ($catNum) {
            1 { $agentName = "BusinessModelAnalyst"; $categoryFolder = "Business Models" }
            2 { $agentName = "BehavioralAnalyst"; $categoryFolder = "Behavioral Psychology" }
            3 { $agentName = "SystemsAnalyst"; $categoryFolder = "Systems & Operations" }
            4 { $agentName = "CultureAnalyst"; $categoryFolder = "Culture & Leadership" }
            5 { $agentName = "RiskAnalyst"; $categoryFolder = "Risk & Antifragility" }
        }

        $agentDir = ".agents\$agentName"
        $outputDir = "$baseOutputDir\$categoryFolder"
        
        if (-not (Test-Path $outputDir)) { 
            New-Item -ItemType Directory -Force -Path $outputDir | Out-Null 
        }

        $absOutputDir = (Resolve-Path $outputDir).Path
        $absInstruction = (Resolve-Path "$agentDir\instruction.md").Path

        Write-Host "    -> Domain: $categoryFolder" -ForegroundColor DarkGray
        
        $safeTopic = $topic -replace '[\\/*?:"<>|]', '-'
        $targetFile = "$outputDir\$today - $safeTopic.md"
        $absTargetFile = "$absOutputDir\$today - $safeTopic.md"

        $prompt = "You are the $agentName. I need you to deeply research the following topic: `"$topic`". `n"
        $prompt += "Read your instruction file at `"$absInstruction`" and follow it strictly. `n"
        $prompt += "Research the topic thoroughly using your tools, structure it exactly as requested in the instruction, and save the final Markdown report to: `"$absTargetFile`" `n"
        $prompt += "CRITICAL: You MUST use your write_to_file tool to save the report EXACTLY to the absolute path provided (`"$absTargetFile`"). DO NOT change the folder name, do not create new folders. DO NOT just print the report to the terminal."

        Write-Host "       [...] Invoking AI Agent..." -ForegroundColor DarkGray

        $process = Start-Process -FilePath "agy" -ArgumentList "--dangerously-skip-permissions", "-p", "`"$prompt`"" -NoNewWindow -Wait -PassThru

        if ($process.ExitCode -eq 0) {
            if (Test-Path $targetFile) {
                Write-Host "       [v] Saved to: $targetFile" -ForegroundColor Green
            } else {
                Write-Host "       [x] Failed to create file: $targetFile" -ForegroundColor Red
            }
        } else {
            Write-Host "       [x] Agent failed with exit code $($process.ExitCode)" -ForegroundColor Red
        }
    }
}

Write-Host "`n[v] All research tasks completed!" -ForegroundColor Green
