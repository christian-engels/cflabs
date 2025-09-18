#!/usr/bin/env bash
set -euo pipefail

# Commit and push repo changes if any exist.
# Usage: commit_push.sh [commit message]

# Move to repo root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [[ -z "${REPO_ROOT}" ]]; then
  echo "Not inside a git repository." >&2
  exit 1
fi
cd "${REPO_ROOT}"

# Check for changes (tracked or untracked)
if [[ -z "$(git status --porcelain)" ]]; then
  echo "No changes to commit."
  exit 0
fi

# Stage everything
git add -A

# If nothing is staged (e.g., ignored), exit quietly
if git diff --cached --quiet; then
  echo "No staged changes to commit."
  exit 0
fi

MESSAGE="${1:-Auto-save changes}"
git commit -m "${MESSAGE}"

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push, setting upstream if needed
if git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
  git push
else
  git push -u origin "${BRANCH}"
fi

echo "Committed and pushed to ${BRANCH}."
