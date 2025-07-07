import os
import shutil
import logging
import sys
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
        results = {'drive': drive, 'categories': {}, 'total_size': 0, 'total_files': 0, 'errors': []}
        for category, paths in self.cleanup_targets.items():
            cat_size, cat_files = 0, 0
            for path in paths:
                if self.is_safe_to_clean(path):
                    size, files = self.scan_path(path)
                    cat_size += size
                    cat_files += files
            if cat_size > 0:
                results['categories'][category] = {'size': cat_size, 'files': cat_files}
                results['total_size'] += cat_size
                results['total_files'] += cat_files
        return results

    def clean_drive(self, drive: str) -> CleanupResult:
        start = datetime.now()
        files_processed = 0
        space_freed = 0
        errors = []
        target_paths = []
        for category, paths in self.cleanup_targets.items():
            for path in paths:
                if self.is_safe_to_clean(path):
                    for root, dirs, files in os.walk(path):
                        for f in files:
                            try:
                                fp = os.path.join(root, f)
                                if self.dry_run:
                                    space_freed += os.path.getsize(fp)
                                    files_processed += 1
                                else:
                                    os.remove(fp)
                                    space_freed += os.path.getsize(fp)
                                    files_processed += 1
                                    target_paths.append(fp)
                            except Exception as e:
                                errors.append(str(e))
        duration = (datetime.now() - start).total_seconds()
        return CleanupResult(files_processed, space_freed, errors, duration, target_paths)
