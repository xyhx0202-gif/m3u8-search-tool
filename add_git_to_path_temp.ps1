# Temporarily add Git to current session environment variables
$gitPath = "C:\Program Files\Git\cmd"
Write-Output "Adding Git path $gitPath to current session environment variables..."

# Add to current session PATH
$env:PATH = "$env:PATH;$gitPath"
Write-Output "Successfully added Git path to current session"

# Test Git command
Write-Output "Testing Git command..."
$gitExe = "$gitPath\git.exe"
if (Test-Path $gitExe) {
    Write-Output "Found Git executable: $gitExe"
    # Run git.exe directly
    & "$gitExe" --version
    Write-Output "✓ Git command is now available!"
} else {
    Write-Output "✗ Cannot find Git executable, please check Git installation path"
}

# Show Git related paths in current environment variables
Write-Output ""
Write-Output "Git related paths in current environment variables:"
$env:PATH -split ';' | Where-Object { $_ -like '*git*' }