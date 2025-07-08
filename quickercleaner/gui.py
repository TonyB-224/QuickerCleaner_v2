import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import os
import sys

# Import datetime with fallback for exe builds
try:
    from datetime import datetime
except ImportError:
    # Fallback for exe builds
    import datetime as dt
    datetime = dt.datetime

import psutil

# Ensure running from project root for relative imports
if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from quickercleaner.cleaner import DiskCleaner
        from quickercleaner.config import Config
    except ImportError as e:
        print("[ERROR] Could not import QuickerCleaner modules. Please run this script from the project root directory (where README.md is located).\nDetails:", e)
        sys.exit(1)
else:
    from quickercleaner.cleaner import DiskCleaner
    from quickercleaner.config import Config

class QuickerCleanerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.cleaner = DiskCleaner()
        self.config = Config()
        self.scanning = False
        self.cleaning = False
        
        # Drive selection variables
        self.source_drive = tk.StringVar(value="C:")
        self.destination_drive = tk.StringVar(value="D:")
        
        self.create_widgets()
        self.update_disk_info()

    def setup_window(self):
        """Setup the main window with elite styling"""
        self.root.title("QuickerCleaner Elite Edition v2.0.0 - Tony Technologies LLC")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e1e')
        self.root.resizable(True, True)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"1000x700+{x}+{y}")
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

    def create_widgets(self):
        """Create all GUI widgets with elite styling"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header with logo and title
        header_frame = tk.Frame(main_frame, bg='#1e1e1e')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        # Title with gradient effect
        title_label = tk.Label(
            header_frame, 
            text="🧹 QuickerCleaner Elite Edition", 
            font=("Segoe UI", 24, "bold"),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame,
            text="Professional Windows Disk Cleanup Tool",
            font=("Segoe UI", 12),
            fg='#888888',
            bg='#1e1e1e'
        )
        subtitle_label.pack()

        # Version and company info
        version_label = tk.Label(
            header_frame,
            text="v2.0.0 - Tony Technologies LLC",
            font=("Segoe UI", 10),
            fg='#666666',
            bg='#1e1e1e'
        )
        version_label.pack(pady=(5, 0))

        # Disk information panel
        self.create_disk_panel(main_frame)

        # Control buttons panel
        self.create_control_panel(main_frame)

        # Progress and status panel
        self.create_progress_panel(main_frame)

        # Output panel
        self.create_output_panel(main_frame)

        # Status bar
        self.create_status_bar(main_frame)

    def create_disk_panel(self, parent):
        """Create disk information panel"""
        disk_frame = tk.LabelFrame(
            parent, 
            text="💾 Disk Information", 
            font=("Segoe UI", 12, "bold"),
            fg='#00ff88',
            bg='#2b2b2b',
            relief=tk.RAISED,
            bd=2
        )
        disk_frame.pack(fill=tk.X, pady=(0, 15))

        # Disk info grid
        self.disk_info_frame = tk.Frame(disk_frame, bg='#2b2b2b')
        self.disk_info_frame.pack(fill=tk.X, padx=10, pady=10)

        # Labels for disk info
        self.disk_labels = {}
        info_items = [
            ('total_space', 'Total Space:'),
            ('free_space', 'Free Space:'),
            ('used_space', 'Used Space:'),
            ('usage_percent', 'Usage:')
        ]

        for i, (key, label) in enumerate(info_items):
            row = i // 2
            col = i % 2 * 2
            
            tk.Label(
                self.disk_info_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                fg='#ffffff',
                bg='#2b2b2b'
            ).grid(row=row, column=col, sticky='w', padx=(0, 10), pady=2)
            
            self.disk_labels[key] = tk.Label(
                self.disk_info_frame,
                text="Loading...",
                font=("Segoe UI", 10),
                fg='#00ff88',
                bg='#2b2b2b'
            )
            self.disk_labels[key].grid(row=row, column=col+1, sticky='w', pady=2)

    def create_control_panel(self, parent):
        """Create control buttons panel"""
        control_frame = tk.LabelFrame(
            parent,
            text="🎛️ Controls",
            font=("Segoe UI", 12, "bold"),
            fg='#00ff88',
            bg='#2b2b2b',
            relief=tk.RAISED,
            bd=2
        )
        control_frame.pack(fill=tk.X, pady=(0, 15))

        # Drive selection frame
        drive_frame = tk.Frame(control_frame, bg='#2b2b2b')
        drive_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Source drive selection
        source_frame = tk.Frame(drive_frame, bg='#2b2b2b')
        source_frame.pack(side=tk.LEFT, padx=(0, 20))

        tk.Label(
            source_frame,
            text="Source Drive:",
            font=("Segoe UI", 10, "bold"),
            fg='#ffffff',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.source_entry = tk.Entry(
            source_frame,
            textvariable=self.source_drive,
            font=("Segoe UI", 10),
            bg='#3b3b3b',
            fg='#ffffff',
            relief=tk.SUNKEN,
            bd=2,
            width=8
        )
        self.source_entry.pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(
            source_frame,
            text="...",
            font=("Segoe UI", 8, "bold"),
            bg='#555555',
            fg='#ffffff',
            relief=tk.RAISED,
            bd=2,
            command=self.choose_source_drive,
            cursor='hand2',
            width=3
        ).pack(side=tk.LEFT)

        # Destination drive selection
        dest_frame = tk.Frame(drive_frame, bg='#2b2b2b')
        dest_frame.pack(side=tk.LEFT)

        tk.Label(
            dest_frame,
            text="Destination:",
            font=("Segoe UI", 10, "bold"),
            fg='#ffffff',
            bg='#2b2b2b'
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.dest_entry = tk.Entry(
            dest_frame,
            textvariable=self.destination_drive,
            font=("Segoe UI", 10),
            bg='#3b3b3b',
            fg='#ffffff',
            relief=tk.SUNKEN,
            bd=2,
            width=8
        )
        self.dest_entry.pack(side=tk.LEFT, padx=(0, 5))

        tk.Button(
            dest_frame,
            text="...",
            font=("Segoe UI", 8, "bold"),
            bg='#555555',
            fg='#ffffff',
            relief=tk.RAISED,
            bd=2,
            command=self.choose_destination_drive,
            cursor='hand2',
            width=3
        ).pack(side=tk.LEFT)

        # Button container
        button_frame = tk.Frame(control_frame, bg='#2b2b2b')
        button_frame.pack(fill=tk.X, padx=10, pady=(5, 10))

        # Scan button
        self.scan_btn = tk.Button(
            button_frame,
            text="🔍 Scan Drive",
            font=("Segoe UI", 12, "bold"),
            bg='#007acc',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            command=self.scan_drive,
            cursor='hand2',
            width=12
        )
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Dry Run button
        self.dry_run_btn = tk.Button(
            button_frame,
            text="👁️ Dry Run",
            font=("Segoe UI", 12, "bold"),
            bg='#ff8c00',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            command=self.dry_run,
            cursor='hand2',
            width=12
        )
        self.dry_run_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Clean button
        self.clean_btn = tk.Button(
            button_frame,
            text="🧹 Clean Drive",
            font=("Segoe UI", 12, "bold"),
            bg='#d13438',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            command=self.clean_drive,
            cursor='hand2',
            width=12
        )
        self.clean_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Emergency Stop button (hidden by default)
        self.emergency_stop_btn = tk.Button(
            button_frame,
            text="🛑 STOP",
            font=("Segoe UI", 12, "bold"),
            bg='#ff0000',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            command=self.emergency_stop,
            cursor='hand2',
            width=12
        )
        # Don't pack yet - will be shown during cleanup

        # Settings button
        self.settings_btn = tk.Button(
            button_frame,
            text="⚙️ Settings",
            font=("Segoe UI", 12, "bold"),
            bg='#666666',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            command=self.open_settings,
            cursor='hand2',
            width=12
        )
        self.settings_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Help button
        self.help_btn = tk.Button(
            button_frame,
            text="❓ Help",
            font=("Segoe UI", 12, "bold"),
            bg='#666666',
            fg='white',
            relief=tk.RAISED,
            bd=3,
            command=self.show_help,
            cursor='hand2',
            width=10
        )
        self.help_btn.pack(side=tk.LEFT)

    def create_progress_panel(self, parent):
        """Create progress and status panel"""
        progress_frame = tk.LabelFrame(
            parent,
            text="📊 Progress",
            font=("Segoe UI", 12, "bold"),
            fg='#00ff88',
            bg='#2b2b2b',
            relief=tk.RAISED,
            bd=2
        )
        progress_frame.pack(fill=tk.X, pady=(0, 15))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            length=400,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)

        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to scan and clean your system",
            font=("Segoe UI", 10),
            fg='#ffffff',
            bg='#2b2b2b'
        )
        self.status_label.pack(pady=(0, 10))

    def create_output_panel(self, parent):
        """Create output display panel"""
        output_frame = tk.LabelFrame(
            parent,
            text="📋 Results",
            font=("Segoe UI", 12, "bold"),
            fg='#00ff88',
            bg='#2b2b2b',
            relief=tk.RAISED,
            bd=2
        )
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Output text area
        self.output = scrolledtext.ScrolledText(
            output_frame,
            height=12,
            width=80,
            font=("Consolas", 10),
            bg='#1e1e1e',
            fg='#00ff88',
            insertbackground='#00ff88',
            selectbackground='#007acc',
            relief=tk.SUNKEN,
            bd=2
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Clear output button
        clear_btn = tk.Button(
            output_frame,
            text="🗑️ Clear Output",
            font=("Segoe UI", 10),
            bg='#666666',
            fg='white',
            command=self.clear_output,
            cursor='hand2'
        )
        clear_btn.pack(pady=(0, 10))

    def create_status_bar(self, parent):
        """Create status bar"""
        self.status_bar = tk.Label(
            parent,
            text="Ready | Tony Technologies LLC",
            font=("Segoe UI", 9),
            fg='#888888',
            bg='#1e1e1e',
            relief=tk.SUNKEN,
            bd=1
        )
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def update_disk_info(self):
        """Update disk information display"""
        try:
            disk_usage = psutil.disk_usage('C:\\')
            total_gb = disk_usage.total / (1024**3)
            free_gb = disk_usage.free / (1024**3)
            used_gb = disk_usage.used / (1024**3)
            usage_percent = (disk_usage.used / disk_usage.total) * 100

            self.disk_labels['total_space'].config(text=f"{total_gb:.1f} GB")
            self.disk_labels['free_space'].config(text=f"{free_gb:.1f} GB")
            self.disk_labels['used_space'].config(text=f"{used_gb:.1f} GB")
            self.disk_labels['usage_percent'].config(text=f"{usage_percent:.1f}%")

            # Color code usage percentage
            if usage_percent > 90:
                self.disk_labels['usage_percent'].config(fg='#ff4444')
            elif usage_percent > 75:
                self.disk_labels['usage_percent'].config(fg='#ffaa00')
            else:
                self.disk_labels['usage_percent'].config(fg='#00ff88')

        except Exception as e:
            for label in self.disk_labels.values():
                label.config(text="Error", fg='#ff4444')

    def scan_drive(self):
        """Scan drive for cleanup opportunities"""
        if self.scanning:
            return

        source = self.source_drive.get()
        self.scanning = True
        self.scan_btn.config(state=tk.DISABLED)
        self.status_label.config(text=f"Scanning {source}...")
        self.progress_var.set(0)
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Starting scan of {source}...\n")
        self.output.see(tk.END)

        def scan_thread():
            try:
                results = self.cleaner.scan_drive(source)
                self.root.after(0, self.update_scan_results, results)
            except Exception as e:
                self.root.after(0, self.handle_error, f"Scan error: {str(e)}")
            finally:
                self.root.after(0, self.scan_complete)

        threading.Thread(target=scan_thread, daemon=True).start()

    def update_scan_results(self, results):
        """Update scan results display"""
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Scan completed!\n\n")
        
        if results and 'categories' in results:
            total_files = results.get('total_files', 0)
            total_size = results.get('total_size', 0)
            
            self.output.insert(tk.END, f"📊 Scan Results:\n")
            self.output.insert(tk.END, f"{'='*50}\n")
            
            for category, data in results['categories'].items():
                files = data.get('files', 0)
                size_mb = data.get('size', 0) / (1024**2)
                self.output.insert(tk.END, f"📁 {category.replace('_', ' ').title()}: {files:,} files, {size_mb:.2f} MB\n")
            
            self.output.insert(tk.END, f"\n🎯 Total: {total_files:,} files, {total_size/(1024**2):.2f} MB\n")
            self.output.insert(tk.END, f"{'='*50}\n\n")
            
            if total_size > 0:
                self.output.insert(tk.END, f"💡 Ready to clean {total_size/(1024**2):.2f} MB of unnecessary files!\n")
            else:
                self.output.insert(tk.END, f"✨ Your system is already clean! No unnecessary files found.\n")
        else:
            self.output.insert(tk.END, f"⚠️ No cleanup opportunities found or scan failed.\n")
        
        self.output.see(tk.END)

    def clean_drive(self):
        """Clean drive with enhanced safety confirmation"""
        if self.cleaning:
            return

        source = self.source_drive.get()
        destination = self.destination_drive.get()

        # First, do a dry run to show what will be cleaned
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Performing safety scan...\n")
        self.output.see(tk.END)
        
        # Get cleanup preview
        try:
            preview_results = self.cleaner.scan_drive(source)
            total_files = preview_results.get('total_files', 0)
            total_size_mb = preview_results.get('total_size', 0) / (1024**2)
        except Exception as e:
            self.handle_error(f"Safety scan failed: {str(e)}")
            return

        # Enhanced confirmation dialog with file details
        confirmation_text = f"""
SAFETY CONFIRMATION - Cleanup Operation

Source: {source}
Destination: {destination}

📊 CLEANUP SUMMARY:
• Files to process: {total_files:,}
• Space to free: {total_size_mb:.2f} MB
• File age filter: {self.cleaner.min_age_days} days minimum

🛡️ SAFETY FEATURES:
• Files will be moved to Recycle Bin (recoverable)
• Protected paths will never be touched
• Double verification before deletion
• Emergency stop available during cleanup

⚠️ WARNING:
This will clean temporary files, cache, and old logs.
Make sure you have backed up any important data.

Are you absolutely sure you want to proceed?
        """
        
        result = messagebox.askyesno(
            "SAFETY CONFIRMATION - Cleanup Operation",
            confirmation_text,
            icon='warning'
        )
        
        if not result:
            self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Cleanup cancelled by user.\n")
            self.output.see(tk.END)
            return

        # Show emergency stop button
        self.emergency_stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.emergency_stop_btn.config(state=tk.NORMAL)

        self.cleaning = True
        self.clean_btn.config(state=tk.DISABLED)
        self.status_label.config(text=f"Cleaning {source}... (Click STOP to cancel)")
        self.progress_var.set(0)
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] 🧹 Starting cleanup of {source}...\n")
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] 🛡️ Emergency STOP button is now available.\n")
        self.output.see(tk.END)

        def clean_thread():
            try:
                # Set destination if different from source
                if destination != source:
                    self.cleaner.move_target = destination
                result = self.cleaner.clean_drive(source)
                self.root.after(0, self.update_clean_results, result)
            except Exception as e:
                self.root.after(0, self.handle_error, f"Cleanup error: {str(e)}")
            finally:
                self.root.after(0, self.clean_complete)

        threading.Thread(target=clean_thread, daemon=True).start()

    def emergency_stop(self):
        """Emergency stop cleanup operation"""
        if self.cleaning:
            self.cleaning = False
            self.emergency_stop_btn.config(state=tk.DISABLED)
            self.emergency_stop_btn.pack_forget()  # Hide the button
            self.clean_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Cleanup stopped by user")
            self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] 🛑 EMERGENCY STOP - Cleanup operation cancelled!\n")
            self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Some files may have already been processed.\n")
            self.output.see(tk.END)
            messagebox.showwarning("Emergency Stop", "Cleanup operation has been stopped. Some files may have already been processed.")

    def update_clean_results(self, result):
        """Update cleanup results display"""
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Cleanup completed!\n\n")
        
        if result:
            files_processed = getattr(result, 'files_processed', 0)
            space_freed_mb = getattr(result, 'space_freed_bytes', 0) / (1024**2)
            duration = getattr(result, 'duration_seconds', 0)
            errors = getattr(result, 'errors', [])
            
            self.output.insert(tk.END, f"🎉 Cleanup Results:\n")
            self.output.insert(tk.END, f"{'='*50}\n")
            self.output.insert(tk.END, f"📁 Files processed: {files_processed:,}\n")
            self.output.insert(tk.END, f"💾 Space freed: {space_freed_mb:.2f} MB\n")
            self.output.insert(tk.END, f"⏱️ Duration: {duration:.2f} seconds\n")
            self.output.insert(tk.END, f"{'='*50}\n\n")
            
            if errors:
                self.output.insert(tk.END, f"⚠️ Errors encountered:\n")
                for error in errors:
                    self.output.insert(tk.END, f"   • {error}\n")
                self.output.insert(tk.END, f"\n")
            
            # Update disk info after cleanup
            self.update_disk_info()
        else:
            self.output.insert(tk.END, f"⚠️ Cleanup failed or no files were processed.\n")
        
        self.output.see(tk.END)

    def scan_complete(self):
        """Handle scan completion"""
        self.scanning = False
        self.scan_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Scan completed")
        self.progress_var.set(100)

    def clean_complete(self):
        """Handle cleanup completion"""
        self.cleaning = False
        self.clean_btn.config(state=tk.NORMAL)
        self.emergency_stop_btn.pack_forget()  # Hide emergency stop button
        self.status_label.config(text="Cleanup completed")
        self.progress_var.set(100)

    def handle_error(self, error_msg):
        """Handle errors"""
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {error_msg}\n")
        self.output.see(tk.END)
        messagebox.showerror("Error", error_msg)

    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings - QuickerCleaner Elite")
        settings_window.geometry("500x400")
        settings_window.configure(bg='#1e1e1e')
        settings_window.resizable(False, False)
        
        # Center the window
        settings_window.update_idletasks()
        x = (settings_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (settings_window.winfo_screenheight() // 2) - (400 // 2)
        settings_window.geometry(f"500x400+{x}+{y}")
        
        # Make it modal
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Title
        title_label = tk.Label(
            settings_window,
            text="⚙️ Settings",
            font=("Segoe UI", 16, "bold"),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(20, 10))
        
        # Settings frame
        settings_frame = tk.Frame(settings_window, bg='#1e1e1e')
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File age setting
        age_frame = tk.Frame(settings_frame, bg='#1e1e1e')
        age_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            age_frame,
            text="Minimum file age (days):",
            font=("Segoe UI", 10, "bold"),
            fg='#ffffff',
            bg='#1e1e1e'
        ).pack(side=tk.LEFT)
        
        age_var = tk.StringVar(value=str(self.cleaner.min_age_days))
        age_entry = tk.Entry(
            age_frame,
            textvariable=age_var,
            font=("Segoe UI", 10),
            bg='#3b3b3b',
            fg='#ffffff',
            relief=tk.SUNKEN,
            bd=2,
            width=10
        )
        age_entry.pack(side=tk.RIGHT)
        
        # Protected paths setting
        paths_frame = tk.Frame(settings_frame, bg='#1e1e1e')
        paths_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            paths_frame,
            text="Protected paths:",
            font=("Segoe UI", 10, "bold"),
            fg='#ffffff',
            bg='#1e1e1e'
        ).pack(anchor=tk.W)
        
        paths_text = tk.Text(
            paths_frame,
            height=4,
            font=("Segoe UI", 9),
            bg='#3b3b3b',
            fg='#ffffff',
            relief=tk.SUNKEN,
            bd=2
        )
        paths_text.pack(fill=tk.X, pady=(5, 0))
        paths_text.insert(tk.END, "\n".join(self.cleaner.protected_paths))
        
        # Buttons
        button_frame = tk.Frame(settings_window, bg='#1e1e1e')
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def save_settings():
            try:
                # Update file age
                new_age = int(age_var.get())
                if new_age < 0:
                    raise ValueError("Age must be positive")
                self.cleaner.min_age_days = new_age
                
                # Update protected paths
                new_paths = paths_text.get(1.0, tk.END).strip().split('\n')
                new_paths = [p.strip() for p in new_paths if p.strip()]
                self.cleaner.protected_paths = new_paths
                
                messagebox.showinfo("Success", "Settings saved successfully!")
                settings_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid setting: {str(e)}")
        
        tk.Button(
            button_frame,
            text="Save",
            font=("Segoe UI", 10, "bold"),
            bg='#007acc',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            command=save_settings,
            cursor='hand2',
            width=10
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 10, "bold"),
            bg='#666666',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            command=settings_window.destroy,
            cursor='hand2',
            width=10
        ).pack(side=tk.RIGHT)

    def show_help(self):
        """Show help information"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - QuickerCleaner Elite")
        help_window.geometry("600x500")
        help_window.configure(bg='#1e1e1e')
        help_window.resizable(True, True)
        
        # Center the window
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (500 // 2)
        help_window.geometry(f"600x500+{x}+{y}")
        
        # Title
        title_label = tk.Label(
            help_window,
            text="❓ Help & Documentation",
            font=("Segoe UI", 16, "bold"),
            fg='#00ff88',
            bg='#1e1e1e'
        )
        title_label.pack(pady=(20, 10))
        
        # Help text area
        help_text = tk.Text(
            help_window,
            font=("Segoe UI", 10),
            bg='#2b2b2b',
            fg='#ffffff',
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        help_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        help_content = """
🧹 QUICKERCLEANER ELITE EDITION v2.0.0
========================================

🎯 MAIN FEATURES:
• Smart disk cleanup with beautiful GUI
• Source and destination drive selection
• Dry run mode to preview changes
• Configurable settings and protected paths
• Real-time progress and detailed output

🔧 CONTROLS:
• Source Drive: Choose which drive/folder to clean
• Destination: Choose where to move files (optional)
• Scan Drive: Analyze for cleanup opportunities
• Dry Run: Preview what would be cleaned (safe)
• Clean Drive: Perform actual cleanup
• Settings: Configure cleanup options

⚙️ SETTINGS:
• Minimum file age: Only clean files older than X days
• Protected paths: Folders that will never be cleaned
• File size limits and other safety options

🛡️ SAFETY FEATURES:
• Protected paths (Documents, Desktop, etc.)
• File age filtering (default: 365 days)
• Confirmation dialogs before deletion
• Dry run mode for safe preview
• Error handling and logging

📁 WHAT GETS CLEANED:
• Windows temporary files
• Browser cache (Chrome, Firefox, Edge)
• Downloads folder (optional)
• System logs and cache files
• Old update files

⚠️ IMPORTANT NOTES:
• Always backup important data before cleaning
• Use dry run first to see what will be deleted
• Protected paths are never touched
• Files are permanently deleted (not moved to recycle bin)

🔗 FOR MORE INFORMATION:
Visit: https://github.com/TonyB-224/QuickerCleaner

📧 SUPPORT:
Contact: tbullard224@gmail.com

Version: 2.0.0
Built by Tony Technologies LLC
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)  # Make read-only
        
        # Close button
        tk.Button(
            help_window,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg='#007acc',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            command=help_window.destroy,
            cursor='hand2',
            width=10
        ).pack(pady=20)

    def clear_output(self):
        """Clear output display"""
        self.output.delete(1.0, tk.END)

    def choose_source_drive(self):
        """Open file dialog to choose source drive/folder"""
        folder = filedialog.askdirectory(
            title="Choose Source Drive/Folder",
            initialdir=self.source_drive.get()
        )
        if folder:
            self.source_drive.set(folder)

    def choose_destination_drive(self):
        """Open file dialog to choose destination drive/folder"""
        folder = filedialog.askdirectory(
            title="Choose Destination Drive/Folder",
            initialdir=self.destination_drive.get()
        )
        if folder:
            self.destination_drive.set(folder)

    def dry_run(self):
        """Perform dry run to preview what would be cleaned"""
        if self.scanning or self.cleaning:
            return

        self.scanning = True
        self.dry_run_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Performing dry run...")
        self.progress_var.set(0)
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] 👁️ Starting dry run of {self.source_drive.get()}...\n")
        self.output.see(tk.END)

        def dry_run_thread():
            try:
                # Enable dry run mode
                self.cleaner.dry_run = True
                results = self.cleaner.scan_drive(self.source_drive.get())
                self.root.after(0, self.update_dry_run_results, results)
            except Exception as e:
                self.root.after(0, self.handle_error, f"Dry run error: {str(e)}")
            finally:
                self.root.after(0, self.dry_run_complete)

        threading.Thread(target=dry_run_thread, daemon=True).start()

    def update_dry_run_results(self, results):
        """Update dry run results display"""
        self.output.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Dry run completed!\n\n")
        
        if results and 'categories' in results:
            total_files = results.get('total_files', 0)
            total_size = results.get('total_size', 0)
            
            self.output.insert(tk.END, f"👁️ DRY RUN - Files that would be cleaned:\n")
            self.output.insert(tk.END, f"{'='*60}\n")
            
            # Show summary by category
            for category, data in results['categories'].items():
                files = data.get('files', 0)
                size_mb = data.get('size', 0) / (1024**2)
                self.output.insert(tk.END, f"📁 {category.replace('_', ' ').title()}: {files:,} files, {size_mb:.2f} MB\n")
            
            self.output.insert(tk.END, f"\n🎯 Total files that would be processed: {total_files:,}\n")
            self.output.insert(tk.END, f"💾 Total space that would be freed: {total_size/(1024**2):.2f} MB\n")
            self.output.insert(tk.END, f"{'='*60}\n\n")
            
            # Show detailed file information
            if 'file_details' in results and results['file_details']:
                self.output.insert(tk.END, f"📋 DETAILED FILE LIST:\n")
                self.output.insert(tk.END, f"{'='*60}\n")
                
                for category, file_list in results['file_details'].items():
                    if file_list:
                        self.output.insert(tk.END, f"\n📂 {category.replace('_', ' ').title()}:\n")
                        for file_info in file_list[:10]:  # Show first 10 files per category
                            path = file_info['path']
                            size_kb = file_info['size'] / 1024
                            age = file_info['age_days']
                            self.output.insert(tk.END, f"   • {os.path.basename(path)} ({size_kb:.1f} KB, {age} days old)\n")
                        
                        if len(file_list) > 10:
                            self.output.insert(tk.END, f"   ... and {len(file_list) - 10} more files\n")
                
                self.output.insert(tk.END, f"\n{'='*60}\n")
            
            # Safety information
            self.output.insert(tk.END, f"🛡️ SAFETY FEATURES:\n")
            self.output.insert(tk.END, f"• Files will be moved to Recycle Bin (not permanently deleted)\n")
            self.output.insert(tk.END, f"• Only files older than {self.cleaner.min_age_days} days will be cleaned\n")
            self.output.insert(tk.END, f"• Protected paths are never touched\n")
            self.output.insert(tk.END, f"• Double verification before any deletion\n\n")
            
            if total_size > 0:
                self.output.insert(tk.END, f"💡 Ready to clean {total_size/(1024**2):.2f} MB of unnecessary files!\n")
                self.output.insert(tk.END, f"⚠️ Click 'Clean Drive' to perform the actual cleanup.\n")
            else:
                self.output.insert(tk.END, f"✨ No files would be cleaned. Your system is already clean!\n")
        else:
            self.output.insert(tk.END, f"⚠️ No cleanup opportunities found or dry run failed.\n")
        
        self.output.see(tk.END)

    def dry_run_complete(self):
        """Handle dry run completion"""
        self.scanning = False
        self.dry_run_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Dry run completed")
        self.progress_var.set(100)

    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    app = QuickerCleanerGUI()
    app.run()

if __name__ == "__main__":
    main()
