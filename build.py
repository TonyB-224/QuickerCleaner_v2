#!/usr/bin/env python3
"""
Simple build script for QuickerCleaner Elite Edition
"""

import os
import subprocess
import sys

def main():
    print("Building QuickerCleaner Elite Edition...")
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
    
    # Build the executable
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name=QuickerCleaner_Elite',
        '--add-data=quickercleaner;quickercleaner',
        'quickercleaner/gui.py'
    ]
    
    print("Running PyInstaller...")
    subprocess.check_call(cmd)
    
    print("Build complete! Executable: dist/QuickerCleaner_Elite.exe")

if __name__ == "__main__":
    main() 