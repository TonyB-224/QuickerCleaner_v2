# 🧹 QuickerCleaner Elite Edition v2.0.0

**The Ultimate Windows Disk Cleanup Tool with Bulletproof Safety Features**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue.svg)](https://www.microsoft.com/windows)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](https://github.com/TonyB-224/QuickerCleaner)

**Professional-grade disk cleanup with enterprise-level safety features. Clean your Windows system with confidence.**

## ✨ Elite Features

- **🛡️ Bulletproof Safety** - Files moved to Recycle Bin, never permanently deleted
- **👁️ Enhanced Dry Run** - See exactly what files will be affected before cleaning
- **🛑 Emergency Stop** - Cancel cleanup operation at any time
- **🎛️ Drive Selection** - Choose source and destination drives with file explorer
- **⚙️ Configurable Settings** - Customize file age limits and protected paths
- **📊 Real-time Progress** - Detailed output with file counts and sizes
- **🎨 Beautiful Dark GUI** - Modern, professional interface

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11**
- **Python 3.8 or higher**
- **Git** (for cloning)

### Run from Source
```bash
# Clone the repository
git clone https://github.com/TonyB-224/QuickerCleaner.git
cd QuickerCleaner

# Install dependencies
pip install -r requirements.txt

# Run GUI version (recommended)
python quickercleaner/gui.py

# Run CLI version
python quickercleaner/main.py --help

# Alternative: Install and use as package
pip install -e .
quicker-cleaner-gui  # GUI version
quicker-cleaner --help  # CLI version
```

### Download Executable
Download the latest release from [Releases](https://github.com/TonyB-224/QuickerCleaner/releases)

### Build Your Own Executable
```bash
# Build standalone executable
python build.py
```

## 🏃 Running as a Package

You can also launch the GUI with:
```bash
python -m quickercleaner
```

## ⚠️ Import Errors? Read This!

Always run scripts from the project root (where README.md is located). For example:
```bash
python quickercleaner/gui.py
```
**Do NOT run scripts from inside the quickercleaner folder.**

If you see an import error, change to the project root and try again.

## 🛡️ Safety Features

- **Recycle Bin Backup** - All files moved to recycle bin (recoverable)
- **Protected Paths** - Important folders never touched
- **File Age Verification** - Only clean files older than specified age
- **Double Confirmation** - Enhanced confirmation dialogs
- **Emergency Stop** - Cancel operation mid-process
- **Detailed Preview** - See exactly what will be cleaned

## 📁 What Gets Cleaned

- **Windows Temp Files** - System and user temporary files
- **Browser Cache** - Chrome, Firefox, Edge cache data
- **Downloads Folder** - Old downloaded files (optional)
- **System Logs** - Old log files and error reports
- **Update Cache** - Windows Update temporary files

## ⚙️ Configuration

Access settings through the GUI to customize:
- **Minimum file age** (default: 365 days)
- **Protected paths** (Documents, Desktop, etc.)
- **Cleanup categories** (temp files, cache, logs)

## 🔧 Requirements

- **OS:** Windows 10/11
- **Python:** 3.8 or higher
- **Dependencies:** See `requirements.txt`

## 📄 License

MIT License - see [LICENSE.txt](LICENSE.txt) for details.

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔧 Troubleshooting

### Common Issues

**Import Error: No module named 'send2trash'**
```bash
pip install send2trash
```

**Import Error: No module named 'win32com'**
```bash
pip install pywin32
```

**GUI won't start**
- Ensure you're running on Windows
- Check that tkinter is available: `python -c "import tkinter"`

**Permission Denied errors**
- Run as Administrator for system directories
- Check that target directories are not in use

### Demo Checklist

Before running the demo:
- [ ] Python 3.8+ installed
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Running on Windows 10/11
- [ ] Test GUI launch: `python quickercleaner/gui.py`
- [ ] Test CLI help: `python quickercleaner/main.py --help`

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/TonyB-224/QuickerCleaner/issues)
- **Email:** tbullard224@gmail.com

---

**Built with ❤️ by Tony Technologies LLC**
