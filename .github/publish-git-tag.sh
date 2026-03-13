#! /usr/bin/env bash

set -euo pipefail

current_version=$(python3 -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])")

git tag "$current_version"
git push --tags
