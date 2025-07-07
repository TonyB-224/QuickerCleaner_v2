# Changelog

All notable changes to QuickerCleaner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced GUI with modern Windows styling
- Improved error handling and logging
- Better configuration management
- Protected paths functionality
- Dry run mode for safe testing

### Changed
- Refactored codebase for better modularity
- Updated dependencies to latest versions
- Improved documentation and examples

### Fixed
- Various bug fixes and performance improvements

## [2.0.0] - 2025-01-XX

### Added
- Elite, modular, and extensible Python codebase
- CLI and GUI (Tkinter) interfaces
- Smart, aggressive, and safe cleaning logic
- Dry run, move, and delete modes
- Modern logging and configuration
- Designed for Windows 10/11
- 100% local, privacy-respecting
- Professional packaging with setuptools
- Comprehensive documentation
- Environment-based configuration
- Protected paths system
- Rich CLI output with progress indicators

### Changed
- Complete rewrite from v1.x
- Modern Python packaging standards
- Enhanced error handling
- Improved user experience

### Removed
- Legacy code and dependencies
- Outdated configuration methods

## [1.0.4] - 2024-XX-XX

### Added
- Basic disk cleanup functionality
- Simple GUI interface
- File scanning capabilities

### Changed
- Initial release structure

---

## Version History

- **v2.0.0**: Elite Edition - Complete rewrite with modern architecture
- **v1.0.4**: Initial release with basic functionality

## Migration Guide

### From v1.x to v2.0.0

1. **Installation**: Use `pip install .` instead of direct Python execution
2. **Configuration**: Copy `env.example` to `.env` and configure settings
3. **CLI Usage**: Use `quicker-cleaner` command instead of `python main.py`
4. **GUI Usage**: Use `quicker-cleaner-gui` command for GUI mode

### Breaking Changes

- Command line interface has changed
- Configuration file format is different
- Some function names and parameters have been updated

---

## Contributing

To add entries to this changelog:

1. Add your changes under the `[Unreleased]` section
2. Use the appropriate category: Added, Changed, Deprecated, Removed, Fixed, Security
3. Provide clear, concise descriptions
4. Reference issue numbers when applicable

## Release Process

1. Update version numbers in:
   - `quickercleaner/__init__.py`
   - `setup.py`
   - `pyproject.toml`
2. Update this changelog
3. Create a git tag
4. Build and publish to PyPI 