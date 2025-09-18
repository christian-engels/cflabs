# Commit and push repo changes if any exist.
# Usage: .\commit_push.ps1 [commit message]
param(
    [string]$Message = "Auto-save changes"
)

$ErrorActionPreference = 'Stop'

try {
    $repoRoot = (& git rev-parse --show-toplevel) 2>$null
} catch {
    Write-Error "Not inside a git repository."
    exit 1
}

Set-Location $repoRoot

# Check for changes
$status = (& git status --porcelain)
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Output "No changes to commit."
    exit 0
}

# Stage everything
& git add -A

# If nothing staged, exit quietly
try {
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Output "No staged changes to commit."
        exit 0
    }
} catch {
    # ignore, proceed
}

& git commit -m $Message

$branch = (& git rev-parse --abbrev-ref HEAD).Trim()

# Check if upstream exists
& git rev-parse --abbrev-ref --symbolic-full-name "@{u}" *> $null
if ($LASTEXITCODE -eq 0) {
    & git push
} else {
    & git push -u origin $branch
}

Write-Output "Committed and pushed to $branch."
