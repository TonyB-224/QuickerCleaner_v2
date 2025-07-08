import argparse
import logging
import sys
import os

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

def main():
    parser = argparse.ArgumentParser(description="QuickerCleaner - Elite Windows Disk Cleanup Tool by Tony Technologies LLC")
    parser.add_argument('--scan', metavar='DRIVE', help='Scan drive for cleanup opportunities')
    parser.add_argument('--clean', metavar='DRIVE', help='Clean specified drive')
    parser.add_argument('--dry-run', action='store_true', help='Preview only, do not delete files')
    parser.add_argument('--min-age', type=int, default=365, help='Minimum file age in days')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    config = Config()
    if args.dry_run:
        config.dry_run = True
    cleaner = DiskCleaner(config)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.scan:
        results = cleaner.scan_drive(args.scan)
        print(f"Scan Results for {args.scan}:")
        for cat, data in results['categories'].items():
            print(f"  {cat}: {data['files']} files, {data['size']/1024/1024:.2f} MB")
        print(f"Total: {results['total_files']} files, {results['total_size']/1024/1024:.2f} MB")
    elif args.clean:
        result = cleaner.clean_drive(args.clean)
        print(f"Cleaned {result.files_processed} files, freed {result.space_freed_bytes/1024/1024:.2f} MB in {result.duration_seconds:.2f}s")
        if result.errors:
            print("Errors:")
            for e in result.errors:
                print(f"  {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
