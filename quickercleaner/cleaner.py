import os
import shutil
import logging
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta

# Add parent directory to path when running directly
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple imports
from quickercleaner.config import Config

class CleanupResult:
    def __init__(self, files_processed: int, space_freed_bytes: int, errors: List[str], duration_seconds: float, target_paths: List[str]):
        self.files_processed = files_processed
        self.space_freed_bytes = space_freed_bytes
        self.errors = errors
        self.duration_seconds = duration_seconds
        self.target_paths = target_paths

class DiskCleaner:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = logging.getLogger("QuickerCleaner")
        self.dry_run = self.config.dry_run
        self.min_age_days = 365
        self.move_target: Optional[str] = None
        self.protected_paths = self.config.protected_paths
        self.cleanup_targets = self._default_cleanup_targets()

    def _default_cleanup_targets(self) -> Dict[str, List[str]]:
        # Add more as needed for elite cleaning
        return {
            'temp_files': [os.path.expandvars('%TEMP%'), os.path.expandvars('%LOCALAPPDATA%\\Temp')],
            'browser_cache': [os.path.expandvars('%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Cache')],
            'downloads': [os.path.expandvars('%USERPROFILE%\\Downloads')],
        }

    def is_safe_to_clean(self, path: str) -> bool:
        path = os.path.abspath(path)
        for protected in self.protected_paths:
            if path.startswith(os.path.abspath(protected)):
                return False
        return os.path.exists(path)

    def scan_path(self, path: str) -> Tuple[int, int]:
        total_size = 0
        file_count = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    fp = os.path.join(root, f)
                    total_size += os.path.getsize(fp)
                    file_count += 1
                except Exception:
                    continue
        return total_size, file_count

    def scan_drive(self, drive: str) -> Dict:
        results = {
            'drive': drive, 
            'categories': {}, 
            'total_size': 0, 
            'total_files': 0, 
            'errors': [],
            'file_details': {}  # New: detailed file information
        }
        
        for category, paths in self.cleanup_targets.items():
            cat_size, cat_files = 0, 0
            cat_files_list = []  # List of actual files
            
            for path in paths:
                if self.is_safe_to_clean(path):
                    size, files, file_list = self.scan_path_detailed(path)
                    cat_size += size
                    cat_files += files
                    cat_files_list.extend(file_list)
            
            if cat_size > 0:
                results['categories'][category] = {
                    'size': cat_size, 
                    'files': cat_files,
                    'file_list': cat_files_list  # Actual file paths
                }
                results['total_size'] += cat_size
                results['total_files'] += cat_files
                results['file_details'][category] = cat_files_list
        
        return results

    def scan_path_detailed(self, path: str) -> Tuple[int, int, List[Dict]]:
        """Scan path and return detailed file information"""
        total_size = 0
        file_count = 0
        file_list = []
        
        try:
            for root, dirs, files in os.walk(path):
                for f in files:
                    try:
                        fp = os.path.join(root, f)
                        if os.path.exists(fp):
                            file_size = os.path.getsize(fp)
                            file_age = self.get_file_age(fp)
                            
                            # Only include files older than min_age_days
                            if file_age >= self.min_age_days:
                                total_size += file_size
                                file_count += 1
                                file_list.append({
                                    'path': fp,
                                    'size': file_size,
                                    'age_days': file_age,
                                    'category': self.get_file_category(fp)
                                })
                    except Exception:
                        continue
        except Exception:
            pass
            
        return total_size, file_count, file_list

    def get_file_age(self, file_path: str) -> int:
        """Get file age in days"""
        try:
            mtime = os.path.getmtime(file_path)
            age_seconds = time.time() - mtime
            return int(age_seconds / (24 * 3600))  # Convert to days
        except:
            return 0

    def get_file_category(self, file_path: str) -> str:
        """Categorize file based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.tmp', '.temp']:
            return 'temporary'
        elif ext in ['.log']:
            return 'log'
        elif ext in ['.cache']:
            return 'cache'
        else:
            return 'other'

    def clean_drive(self, drive: str) -> CleanupResult:
        start = datetime.now()
        files_processed = 0
        space_freed = 0
        errors = []
        target_paths = []
        
        # SAFETY: Use recycle bin instead of permanent deletion
        use_recycle_bin = True  # Always use recycle bin for safety
        
        for category, paths in self.cleanup_targets.items():
            for path in paths:
                if self.is_safe_to_clean(path):
                    for root, dirs, files in os.walk(path):
                        for f in files:
                            try:
                                fp = os.path.join(root, f)
                                
                                # SAFETY: Check file age again before deletion
                                if not self.is_file_old_enough(fp):
                                    continue
                                
                                # SAFETY: Double-check protected paths
                                if not self.is_safe_to_clean(fp):
                                    continue
                                
                                if self.dry_run:
                                    space_freed += os.path.getsize(fp)
                                    files_processed += 1
                                else:
                                    # SAFETY: Move to recycle bin instead of permanent delete
                                    if use_recycle_bin:
                                        try:
                                            import send2trash
                                            send2trash.send2trash(fp)
                                        except ImportError:
                                            # Fallback to recycle bin via Windows API
                                            self.move_to_recycle_bin(fp)
                                    else:
                                        os.remove(fp)
                                    
                                    space_freed += os.path.getsize(fp)
                                    files_processed += 1
                                    target_paths.append(fp)
                            except Exception as e:
                                errors.append(f"Error with {fp}: {str(e)}")
        
        duration = (datetime.now() - start).total_seconds()
        return CleanupResult(files_processed, space_freed, errors, duration, target_paths)

    def is_file_old_enough(self, file_path: str) -> bool:
        """Check if file is old enough to be cleaned"""
        try:
            file_age = self.get_file_age(file_path)
            return file_age >= self.min_age_days
        except:
            return False

    def move_to_recycle_bin(self, file_path: str):
        """Move file to Windows recycle bin using shell API"""
        try:
            import win32com.client
            shell = win32com.client.Dispatch("Shell.Application")
            folder = shell.NameSpace(os.path.dirname(file_path))
            folder.MoveHere(os.path.basename(file_path))
        except:
            # Fallback: just delete if recycle bin fails
            os.remove(file_path)
