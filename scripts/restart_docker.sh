#!/usr/bin/env sh
set -e

echo "Rebuilding and restarting Docker services..."
docker-compose up -d --build

echo "Done. Use 'docker-compose logs -f' to follow logs."