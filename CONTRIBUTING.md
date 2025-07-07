# Contributing to QuickerCleaner Elite Edition 🧹

Thank you for your interest in contributing to QuickerCleaner! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

We welcome contributions from the community! Here are the main ways you can help:

### 🐛 Reporting Bugs

1. **Check existing issues** - Search the [Issues](https://github.com/TonyB-224/QuickerCleaner/issues) page to see if the bug has already been reported
2. **Create a new issue** - Use the bug report template and provide:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (Windows version, Python version)
   - Screenshots if applicable

### 💡 Suggesting Features

1. **Check existing issues** - Search for similar feature requests
2. **Create a feature request** - Use the feature request template and describe:
   - What you'd like to see
   - Why it would be useful
   - How it could work
   - Any mockups or examples

### 🔧 Code Contributions

#### Prerequisites

- Python 3.8+
- Windows 10/11
- Git
- Basic knowledge of Python and Windows systems

#### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/QuickerCleaner.git
   cd QuickerCleaner
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Install development tools**
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

#### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation if needed

3. **Run tests and quality checks**
   ```bash
   # Run tests
   pytest
   
   # Check code formatting
   black --check .
   
   # Run linting
   flake8 .
   
   # Type checking
   mypy quickercleaner/
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Coding Standards

### Python Code Style

- **Follow PEP 8** - Use Black for automatic formatting
- **Type hints** - Use type hints for all function parameters and return values
- **Docstrings** - Use Google-style docstrings for all public functions
- **Line length** - Maximum 88 characters (Black default)

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(cleaner): add support for custom file patterns
fix(gui): resolve memory leak in progress bar
docs(readme): update installation instructions
```

### Testing Guidelines

- **Unit tests** - Test individual functions and classes
- **Integration tests** - Test complete workflows
- **Test coverage** - Aim for at least 80% coverage
- **Test naming** - Use descriptive test names that explain what is being tested

### Documentation

- **Code comments** - Explain complex logic, not obvious code
- **README updates** - Update README.md for user-facing changes
- **Docstrings** - Document all public APIs
- **Examples** - Provide usage examples for new features

## 🏗️ Project Structure

```
QuickerCleaner/
├── quickercleaner/          # Main package
│   ├── __init__.py         # Package initialization
│   ├── main.py             # CLI entry point
│   ├── gui.py              # GUI interface
│   ├── cleaner.py          # Core cleaning logic
│   └── config.py           # Configuration management
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .github/                # GitHub workflows and templates
├── pyproject.toml          # Project configuration
├── requirements.txt        # Dependencies
└── README.md              # Project documentation
```

## 🔍 Review Process

1. **Pull Request Creation**
   - Fill out the PR template completely
   - Link related issues
   - Provide clear description of changes

2. **Code Review**
   - All PRs require at least one review
   - Address review comments promptly
   - Maintainers may request changes

3. **CI/CD Checks**
   - All tests must pass
   - Code quality checks must pass
   - Coverage requirements must be met

4. **Merge**
   - Squash commits if requested
   - Delete feature branch after merge

## 🚀 Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

### Release Steps

1. **Update version** in `quickercleaner/__init__.py`
2. **Update CHANGELOG.md** with release notes
3. **Create release tag**
4. **GitHub Actions** will automatically:
   - Build the package
   - Run tests
   - Create GitHub release
   - Publish to PyPI (if configured)

## 🛡️ Security

### Reporting Security Issues

**DO NOT** create a public issue for security vulnerabilities. Instead:

1. Email: tbullard224@gmail.com
2. Include "SECURITY" in the subject line
3. Provide detailed description of the vulnerability
4. Include steps to reproduce

### Security Guidelines

- Never commit sensitive information (API keys, passwords)
- Use environment variables for configuration
- Validate all user inputs
- Follow the principle of least privilege

## 📞 Getting Help

### Questions and Support

- **GitHub Issues** - For bugs and feature requests
- **Email** - tbullard224@gmail.com
- **Documentation** - Check README.md and QUICK_START.md

### Development Resources

- **Python Documentation** - https://docs.python.org/
- **Windows API** - https://docs.microsoft.com/en-us/windows/win32/
- **GitHub Flow** - https://guides.github.com/introduction/flow/

## 🙏 Recognition

Contributors will be recognized in:
- **README.md** - Contributors section
- **Release notes** - For significant contributions
- **GitHub contributors** - Automatic recognition

## 📄 License

By contributing to QuickerCleaner, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to QuickerCleaner! 🎉 