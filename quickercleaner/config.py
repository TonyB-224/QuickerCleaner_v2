import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

class Config:
    """Configuration management for QuickerCleaner"""
    def __init__(self):
        load_dotenv()
        self.target_drive = os.getenv('QUICK_CLEANER_TARGET_DRIVE', 'D:')
        self.max_file_size_gb = float(os.getenv('QUICK_CLEANER_MAX_FILE_SIZE_GB', '10.0'))
        self.dry_run = os.getenv('QUICK_CLEANER_DRY_RUN', 'false').lower() == 'true'
        self.confirm_deletions = os.getenv('QUICK_CLEANER_CONFIRM_DELETIONS', 'true').lower() == 'true'
        self.log_level = os.getenv('QUICK_CLEANER_LOG_LEVEL', 'INFO')
        self.log_file = os.getenv('QUICK_CLEANER_LOG_FILE', 'quick_cleaner.log')
        protected_paths_str = os.getenv('QUICK_CLEANER_PROTECTED_PATHS', '')
        self.protected_paths = [p.strip() for p in protected_paths_str.split(',') if p.strip()]
        if not self.protected_paths:
            self.protected_paths = [
                os.path.expandvars('%USERPROFILE%\\Documents'),
                os.path.expandvars('%USERPROFILE%\\Desktop'),
                os.path.expandvars('%USERPROFILE%\\Pictures'),
                os.path.expandvars('%USERPROFILE%\\Downloads'),
                os.path.expandvars('%USERPROFILE%\\Videos'),
                os.path.expandvars('%USERPROFILE%\\Music'),
                os.path.expandvars('%WINDIR%'),
                os.path.expandvars('%PROGRAMFILES%'),
                os.path.expandvars('%PROGRAMFILES(X86)%')
            ]
    def validate(self) -> List[str]:
        errors = []
        if self.target_drive and not os.path.exists(self.target_drive):
            errors.append(f"Target drive {self.target_drive} does not exist")
        if self.max_file_size_gb <= 0:
            errors.append("Max file size must be greater than 0")
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.log_level not in valid_log_levels:
            errors.append(f"Invalid log level: {self.log_level}. Must be one of {valid_log_levels}")
        return errors
