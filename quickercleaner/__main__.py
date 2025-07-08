"""
QuickerCleaner Elite Edition - Package Entrypoint
Allows running: python -m quickercleaner
"""

import sys

if __name__ == "__main__":
    try:
        from quickercleaner.gui import QuickerCleanerGUI
        QuickerCleanerGUI().run()
    except Exception as e:
        print("[ERROR] Could not launch QuickerCleaner GUI.\nDetails:", e)
        sys.exit(1) 