#!/bin/bash
# render.sh - Deployment script for Render
# This runs during the Render build process

set -eu

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🗄️  Initializing database..."
python manage.py init

echo "🌱 Seeding sample yoga poses..."
python manage.py seed

echo "✅ Build complete! Starting app..."
