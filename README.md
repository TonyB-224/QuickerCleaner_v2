# QuickerCleaner Elite Edition

A powerful Windows disk cleanup tool with a beautiful GUI interface.

## Features

- **Beautiful Dark Theme GUI** - Modern interface with disk info panel
- **Smart Cleanup** - Removes temp files, browser cache, downloads, and more
- **Safe Operations** - Only cleans safe locations, never system files
- **Real-time Progress** - See cleanup progress with detailed output
- **Disk Information** - View disk usage and available space

## Quick Start

### Run from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI version
python quickercleaner/gui.py

# Run CLI version  
python quickercleaner/main.py
```

### Build Executable
```bash
# Build standalone executable
python build.py
```

The executable will be created as `dist/QuickerCleaner_Elite.exe`

## What It Cleans

- Windows Temp files
- Browser cache (Chrome, Firefox, Edge)
- Downloads folder (optional)
- Recycle Bin
- Windows Update cache
- System logs

## Safety

- Only cleans safe, non-system locations
- Never touches important system files
- Shows exactly what will be deleted before cleaning
- Confirmation dialog before any cleanup

## Requirements

- Windows 10/11
- Python 3.8+
- Required packages in `requirements.txt`

## License

MIT License - see LICENSE.txt for details.
