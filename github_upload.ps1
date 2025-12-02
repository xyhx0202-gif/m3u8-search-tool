#!/usr/bin/env powershell
# GitHub Upload Script - Using full Git path

# Configuration
$gitExe = "C:\Program Files\Git\cmd\git.exe"
$username = "xyhx0202-gif"
$repo_name = "m3u8-search-tool"
$remote_url = "https://github.com/$username/$repo_name.git"

Write-Output "=== GitHub Upload Tool ==="
Write-Output "Git path: $gitExe"
Write-Output "Repository: $remote_url"

# Check if Git executable exists
if (-not (Test-Path $gitExe)) {
    Write-Output "Error: Git executable not found"
    exit 1
}

# Function to execute Git commands
function Execute-Git($cmd) {
    Write-Output "\nExecuting: git $cmd"
    & $gitExe $cmd.Split(' ')
    return $LASTEXITCODE
}

# Initialize Git repository if needed
if (-not (Test-Path ".git")) {
    Write-Output "\nInitializing Git repository..."
    Execute-Git "init"
    Execute-Git "config user.name '$username'"
    Execute-Git "config user.email '$username@example.com'"
    Execute-Git "remote add origin $remote_url"
}

# Add all files
Write-Output "\nAdding files to staging..."
Execute-Git "add ."

# Commit changes
Write-Output "\nCommitting changes..."
Execute-Git "commit -m 'Upload m3u8-search-tool project'"

# Create and push branch
Write-Output "\nCreating main branch..."
Execute-Git "checkout -b main"

Write-Output "\nPushing to GitHub..."
Write-Output "Note: If authentication is required, please enter GitHub credentials when prompted"
Execute-Git "push -u origin main"

Write-Output "\n=== Operation completed ==="
Write-Output "If you encounter authentication issues, please run the Git push command manually"