# QuickerCleaner Elite Edition - Makefile
# Provides convenient commands for development, testing, and building

.PHONY: help install test lint format clean build release windows-exe docker-build docker-test

# Default target
help:
	@echo "QuickerCleaner Elite Edition - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     - Install package in development mode"
	@echo "  test        - Run tests with coverage"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with Black"
	@echo "  clean       - Clean build artifacts"
	@echo ""
	@echo "Building:"
	@echo "  build       - Build package distribution"
	@echo "  windows-exe - Build Windows executable"
	@echo "  release     - Prepare for release"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-test  - Run tests in Docker"
	@echo ""
	@echo "Utilities:"
	@echo "  help        - Show this help message"
	@echo "  version     - Show current version"
	@echo "  check       - Run all quality checks"

# Development commands
install:
	@echo "Installing QuickerCleaner in development mode..."
	pip install -e .
	pip install -r requirements.txt

test:
	@echo "Running tests with coverage..."
	pytest --cov=quickercleaner --cov-report=term-missing --cov-report=html

lint:
	@echo "Running linting checks..."
	flake8 quickercleaner/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 quickercleaner/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

format:
	@echo "Formatting code with Black..."
	black quickercleaner/

format-check:
	@echo "Checking code formatting..."
	black --check --diff quickercleaner/

type-check:
	@echo "Running type checking with mypy..."
	mypy quickercleaner/ --ignore-missing-imports

check: lint format-check type-check test
	@echo "All quality checks passed! ✅"

# Building commands
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

build: clean
	@echo "Building package distribution..."
	python -m build

windows-exe:
	@echo "Building Windows executable..."
	pip install pyinstaller
	pyinstaller --onefile --windowed --name QuickerCleaner_Elite quickercleaner/gui.py
	@echo "Executable created: dist/QuickerCleaner_Elite.exe"

release: check build
	@echo "Release preparation complete!"
	@echo "Next steps:"
	@echo "1. Update version in quickercleaner/__init__.py"
	@echo "2. Update CHANGELOG.md"
	@echo "3. Create and push git tag"
	@echo "4. GitHub Actions will handle the rest"

# Docker commands
docker-build:
	@echo "Building Docker image..."
	docker build -t quickercleaner:latest .

docker-test:
	@echo "Running tests in Docker..."
	docker run --rm quickercleaner:latest pytest

docker-run:
	@echo "Running QuickerCleaner in Docker..."
	docker run --rm -it quickercleaner:latest python -m quickercleaner.main --help

# Utility commands
version:
	@python -c "import quickercleaner; print(f'QuickerCleaner version: {quickercleaner.__version__}')"

# Development environment setup
setup-dev:
	@echo "Setting up development environment..."
	python -m venv venv
	@echo "Virtual environment created. Activate it with:"
	@echo "  venv\\Scripts\\activate  # Windows"
	@echo "  source venv/bin/activate  # Unix/Linux"
	@echo "Then run: make install"

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "Documentation is available in README.md and QUICK_START.md"

# Security checks
security:
	@echo "Running security checks..."
	pip install safety
	safety check

# Performance profiling
profile:
	@echo "Running performance profiling..."
	python -m cProfile -o profile.stats quickercleaner/main.py --scan C: --dry-run
	@echo "Profile data saved to profile.stats"

# Backup and restore
backup:
	@echo "Creating backup of current state..."
	git archive --format=zip --output=backup-$(shell date +%Y%m%d-%H%M%S).zip HEAD

# Environment setup
env-setup:
	@echo "Setting up environment configuration..."
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "Environment file created from template"; \
	else \
		echo "Environment file already exists"; \
	fi

# Quick start
quick-start: env-setup install
	@echo "Quick start setup complete!"
	@echo "Run the application with:"
	@echo "  python -m quickercleaner.main --help"
	@echo "  python -m quickercleaner.gui"

# Windows-specific commands
windows-setup:
	@echo "Setting up Windows-specific requirements..."
	pip install pywin32
	@echo "Windows setup complete"

# CI/CD helpers
ci-install:
	@echo "Installing dependencies for CI..."
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy build wheel twine

ci-test:
	@echo "Running CI tests..."
	pytest --cov=quickercleaner --cov-report=xml

ci-lint:
	@echo "Running CI linting..."
	flake8 quickercleaner/ --count --exit-zero --max-complexity=10 --max-line-length=88
	black --check quickercleaner/
	mypy quickercleaner/ --ignore-missing-imports

# Package management
update-deps:
	@echo "Updating dependencies..."
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

freeze-deps:
	@echo "Freezing current dependencies..."
	pip freeze > requirements-frozen.txt

# Git helpers
git-hooks:
	@echo "Setting up git hooks..."
	@if [ -d .git ]; then \
		mkdir -p .git/hooks; \
		echo '#!/bin/sh' > .git/hooks/pre-commit; \
		echo 'make check' >> .git/hooks/pre-commit; \
		chmod +x .git/hooks/pre-commit; \
		echo "Git hooks installed"; \
	else \
		echo "Not a git repository"; \
	fi 