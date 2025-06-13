#!/bin/bash

# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create GitHub repository (requires gh CLI)
gh repo create photo-importer --public --confirm

git push -u origin main

echo "GitHub repository created at https://github.com/$(gh api user | jq -r '.login')/photo-importer"
