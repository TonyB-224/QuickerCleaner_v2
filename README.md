# QuickerCleaner Elite Edition 🧹

**The Fast, Safe, and Smart Windows Disk Cleanup Tool**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows)
[![CI](https://github.com/TonyB-224/QuickerCleaner/workflows/CI/badge.svg)](https://github.com/TonyB-224/QuickerCleaner/actions)
[![PyPI](https://img.shields.io/pypi/v/quicker-cleaner.svg)](https://pypi.org/project/quicker-cleaner/)

QuickerCleaner is the next-level, professional Windows disk cleanup tool. Designed for power users, IT professionals, and anyone who demands the best in speed, safety, and control.

## ✨ Features

- **Elite, modular, and extensible Python codebase**
- **CLI and GUI (Tkinter) interfaces** - Choose your preferred way to interact
- **Smart, aggressive, and safe cleaning logic** - Intelligent file detection and removal
- **Dry run, move, and delete modes** - Preview before making changes
- **Modern logging and configuration** - Comprehensive logging and flexible settings
- **Designed for Windows 10/11** - Optimized for modern Windows systems
- **100% local, privacy-respecting** - No cloud dependencies, no data collection
- **Protected paths system** - Never clean important directories
- **Rich CLI output** - Beautiful, informative command-line interface
- **Environment-based configuration** - Easy configuration management

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/TonyB-224/QuickerCleaner.git
cd QuickerCleaner

# Install in development mode
pip install -e .

# Or install from PyPI (when available)
pip install quicker-cleaner
```

### Basic Usage

```bash
# Scan drive for cleanup opportunities
quicker-cleaner --scan C:

# Clean drive with confirmation
quicker-cleaner --clean C: --confirm

# Dry run (preview only)
quicker-cleaner --clean C: --dry-run

# GUI mode
quicker-cleaner-gui
```

### Advanced Usage

```bash
# Clean with custom age filter
quicker-cleaner --clean C: --min-age 180

# Verbose output
quicker-cleaner --scan C: --verbose

# Move files to another drive
quicker-cleaner --clean C: --target D: --confirm
```

## ⚙️ Configuration

Copy `env.example` to `.env` and adjust settings:

```bash
# Copy configuration template
cp env.example .env

# Edit configuration
notepad .env
```

### Key Configuration Options

```ini
# Target drive for moving files
QUICK_CLEANER_TARGET_DRIVE=D:

# Maximum file size in GB
QUICK_CLEANER_MAX_FILE_SIZE_GB=10.0

# Dry run mode (preview only)
QUICK_CLEANER_DRY_RUN=false

# Protected paths (comma-separated)
QUICK_CLEANER_PROTECTED_PATHS=C:\Important,C:\Backup
```

## 🛠️ Development

### Prerequisites

- Python 3.8+
- Windows 10/11
- Git

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/TonyB-224/QuickerCleaner.git
cd QuickerCleaner

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install development tools
pip install pytest pytest-cov black flake8 mypy
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=quickercleaner

# Run specific test
pytest tests/test_cleaner.py
```

### Code Quality

```bash
# Format code
black quickercleaner/

# Lint code
flake8 quickercleaner/

# Type checking
mypy quickercleaner/
```

### Using Makefile

```bash
# Show all available commands
make help

# Install in development mode
make install

# Run tests
make test

# Build package
make build

# Full release preparation
make release
```

## 🐳 Docker Support

### Development with Docker

```bash
# Build and run tests
docker-compose --profile test up --build

# Run linting
docker-compose --profile lint up --build

# Development environment
docker-compose --profile dev up --build
```

### Build Docker Image

```bash
# Build image
docker build -t quickercleaner .

# Run container
docker run -it quickercleaner python -m quickercleaner.main --help
```

## 📦 Building Executables

### Using PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name QuickerCleaner quickercleaner/gui.py

# Or use Makefile
make windows-exe
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `make test`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📋 Requirements

- **OS**: Windows 10/11
- **Python**: 3.8 or higher
- **Dependencies**: See `requirements.txt`

## 🔧 Troubleshooting

### Common Issues

1. **Permission Denied**: Run as Administrator
2. **Import Errors**: Ensure all dependencies are installed
3. **GUI Not Working**: Check if tkinter is available

### Getting Help

- Check existing [Issues](https://github.com/TonyB-224/QuickerCleaner/issues)
- Create a new issue with detailed information
- Contact: tbullard224@gmail.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

## 🙏 Acknowledgments

- Built with ❤️ by Tony Technologies LLC
- Inspired by the need for better Windows disk management tools
- Thanks to all contributors and the open-source community

---

**QuickerCleaner: Elite cleaning, professional results.** 🚀

**By Tony Technologies LLC**  
**Contact**: tbullard224@gmail.com
