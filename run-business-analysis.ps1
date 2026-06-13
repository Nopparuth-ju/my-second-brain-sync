$ErrorActionPreference = "Stop"

$agentDir = ".agents\IndustryResearcher"
$queueFile = "$agentDir\industry_queue.json"
$completedFile = "$agentDir\industry_completed.json"
$outputDir = "02_SOURCE\BUSINESS_FEEDS"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  [*] DEEP LEARNING INDUSTRY RESEARCHER [*]" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

if (-not (Test-Path $queueFile)) {
    Write-Host "[x] Queue file not found: $queueFile" -ForegroundColor Red
    exit
}

$queue = Get-Content $queueFile -Raw | ConvertFrom-Json
if ($queue.Length -eq 0) {
    Write-Host "[v] The industry research queue is empty. Good job!" -ForegroundColor Green
    exit
}

$topic = $queue[0]
$remaining = $queue[1..($queue.Length-1)]
if ($null -eq $remaining) { $remaining = @() }

Write-Host "`n[>] Starting deep research on: " -NoNewline
Write-Host "$topic" -ForegroundColor Yellow

# Create output path
$today = Get-Date -Format "yyyy-MM-dd"
$safeTopic = $topic -replace '[\\/*?:"<>|]', '-'
$targetFile = "$outputDir\$today - $safeTopic.md"

# Ensure output dir exists
if (-not (Test-Path $outputDir)) { New-Item -ItemType Directory -Force -Path $outputDir | Out-Null }

$prompt = "You are the IndustryResearcher. I need you to deeply research the following business/industry topic: `"$topic`". `n"
$prompt += "Read .agents/IndustryResearcher/instruction.md and follow it strictly. `n"
$prompt += "Research the topic thoroughly, structure it using the 4 Pillars, and save the final Markdown report to: `"$targetFile`" `n"
$prompt += "Do not just print the report to the terminal. You MUST use your write_to_file tool to save it EXACTLY ONCE. Do NOT create any drafts or files with other names."

Write-Host "[...] Invoking AI Agent to perform web research and synthesis... (This may take a few minutes)" -ForegroundColor DarkGray

# Execute agy
$process = Start-Process -FilePath "agy" -ArgumentList "--dangerously-skip-permissions", "-p", "`"$prompt`"" -NoNewWindow -Wait -PassThru

if ($process.ExitCode -eq 0) {
    if (Test-Path $targetFile) {
        Write-Host "`n[v] Research complete! Report saved to: $targetFile" -ForegroundColor Green
        
        # Update Queue
        $remaining | ConvertTo-Json | Set-Content $queueFile -Encoding UTF8
        
        # Add to Completed
        $completed = @()
        if (Test-Path $completedFile) {
            $completed = Get-Content $completedFile -Raw | ConvertFrom-Json
        }
        $completed += $topic
        $completed | ConvertTo-Json | Set-Content $completedFile -Encoding UTF8
        
        Write-Host "[>] Moved `"$topic`" to completed list. $($remaining.Length) items left in queue.`n" -ForegroundColor Cyan
    } else {
        Write-Host "`n[x] AI Agent finished but failed to create the target file: $targetFile" -ForegroundColor Red
    }
} else {
    Write-Host "`n[x] AI Agent process failed with exit code $($process.ExitCode)" -ForegroundColor Red
}
