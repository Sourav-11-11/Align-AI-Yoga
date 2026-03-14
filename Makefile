.PHONY: help install run-local run-prod test lint format clean db-reset deploy

help:
	@echo "🧘 Align AI Yoga — Makefile Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install        Install dependencies"
	@echo "  make run-local      Run Flask locally (dev mode)"
	@echo "  make test           Run test suite"
	@echo "  make lint           Run code linter (flake8)"
	@echo "  make format         Auto-format code (black)"
	@echo ""
	@echo "Database:"
	@echo "  make db-reset       Reset SQLite database"
	@echo ""
	@echo "Production:"
	@echo "  make run-prod       Run with Gunicorn (production)"
	@echo "  make deploy         Deploy to Render (requires git push)"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          Clean __pycache__, .pytest_cache, etc."

install:
	pip install -r requirements.txt

run-local:
	cd frontend && python run.py

run-prod:
	cd frontend && gunicorn -w 1 -b 0.0.0.0:8000 --timeout 60 wsgi:app

test:
	cd frontend && pytest tests/ -v

lint:
	flake8 frontend/app --max-line-length=100

format:
	black frontend/app --line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -name *.pyc -delete
	find . -name .DS_Store -delete

db-reset:
	rm -f frontend/align_yoga.db
	@echo "✓ SQLite database reset. It will be recreated on next app startup."

deploy:
	@echo "Push to GitHub and Render will auto-deploy:"
	@echo "  git add ."
	@echo "  git commit -m 'Deploy: [description]'"
	@echo "  git push origin main"
	@echo ""
	@echo "Monitor deployment: https://dashboard.render.com"
