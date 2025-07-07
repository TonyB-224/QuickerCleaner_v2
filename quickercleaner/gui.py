import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
from datetime import datetime
from quickercleaner.cleaner import DiskCleaner
from quickercleaner.config import Config

class QuickerCleanerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QuickerCleaner Elite Edition - Tony Technologies LLC")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        self.cleaner = DiskCleaner()
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="QuickerCleaner Elite Edition", font=("Segoe UI", 16, "bold"))
        self.label.pack(pady=20)
        self.scan_btn = ttk.Button(self.root, text="Scan C:", command=self.scan)
        self.scan_btn.pack(pady=10)
        self.clean_btn = ttk.Button(self.root, text="Clean C:", command=self.clean)
        self.clean_btn.pack(pady=10)
        self.output = scrolledtext.ScrolledText(self.root, height=10, width=60)
        self.output.pack(pady=10)

    def scan(self):
        self.output.insert(tk.END, "Scanning C:\\...\n")
        results = self.cleaner.scan_drive("C:")
        for cat, data in results['categories'].items():
            self.output.insert(tk.END, f"{cat}: {data['files']} files, {data['size']/1024/1024:.2f} MB\n")
        self.output.insert(tk.END, f"Total: {results['total_files']} files, {results['total_size']/1024/1024:.2f} MB\n")

    def clean(self):
        self.output.insert(tk.END, "Cleaning C:\\...\n")
        result = self.cleaner.clean_drive("C:")
        self.output.insert(tk.END, f"Cleaned {result.files_processed} files, freed {result.space_freed_bytes/1024/1024:.2f} MB\n")
        if result.errors:
            self.output.insert(tk.END, "Errors:\n")
            for e in result.errors:
                self.output.insert(tk.END, f"  {e}\n")

    def run(self):
        self.root.mainloop()

def main():
    app = QuickerCleanerGUI()
    app.run()

if __name__ == "__main__":
    main()
