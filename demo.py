#!/usr/bin/env python3
"""
Demo script for QuickerCleaner Elite Edition
Run this to test all components before the demo
"""

import sys
import os
import subprocess

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError as e:
        print(f"❌ tkinter - FAILED: {e}")
        return False
    
    try:
        import psutil
        print("✅ psutil - OK")
    except ImportError as e:
        print(f"❌ psutil - FAILED: {e}")
        return False
    
    try:
        import send2trash
        print("✅ send2trash - OK")
    except ImportError as e:
        print(f"❌ send2trash - FAILED: {e}")
        return False
    
    try:
        import win32com.client
        print("✅ win32com - OK")
    except ImportError as e:
        print(f"❌ win32com - FAILED: {e}")
        return False
    
    try:
        from quickercleaner.cleaner import DiskCleaner
        from quickercleaner.config import Config
        print("✅ QuickerCleaner modules - OK")
    except ImportError as e:
        print(f"❌ QuickerCleaner modules - FAILED: {e}")
        return False
    
    return True

def test_cli():
    """Test CLI functionality"""
    print("\n🔍 Testing CLI...")
    
    try:
        result = subprocess.run([
            sys.executable, "quickercleaner/main.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ CLI help - OK")
            return True
        else:
            print(f"❌ CLI help - FAILED: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ CLI test - FAILED: {e}")
        return False

def test_gui_import():
    """Test GUI import (without launching window)"""
    print("\n🔍 Testing GUI import...")
    
    try:
        # Test import without creating window
        import quickercleaner.gui
        print("✅ GUI import - OK")
        return True
    except Exception as e:
        print(f"❌ GUI import - FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("🧹 QuickerCleaner Elite Edition - Demo Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    # Test CLI
    if not test_cli():
        print("\n❌ CLI test failed.")
        return False
    
    # Test GUI import
    if not test_gui_import():
        print("\n❌ GUI import test failed.")
        return False
    
    print("\n🎉 All tests passed! Ready for demo.")
    print("\n📋 Demo Commands:")
    print("  GUI: python quickercleaner/gui.py")
    print("  CLI: python quickercleaner/main.py --help")
    print("  Scan: python quickercleaner/main.py --scan C: --dry-run")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 