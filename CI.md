# CI / CD

- **CI:** GitHub Actions workflow `CI Pipeline` runs on pull requests and pushes to `main`. It runs `ruff` (lint) and tests with coverage via `bash scripts/run-tests.sh`.
- **CD:** GitHub Actions workflow `CD Pipeline` runs on pushes to `main` and after `CI Pipeline` completes successfully. It builds a Docker image and uploads a deployment package artifact.
- **Required repository secrets:** `DOCKER_USERNAME`, `DOCKER_PASSWORD` (for pushing images to Docker Hub).

## Badges

Add these badge links near the top of the `README.md` (replace `<owner>/<repo>`):

[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml) [![CD](https://github.com/<owner>/<repo>/actions/workflows/cd.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/cd.yml)
