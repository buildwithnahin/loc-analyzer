import argparse
from pathlib import Path
from .scanner import analyze_directory
from .reporter import print_report
from .config import DEFAULT_IGNORE_DIRS, DEFAULT_EXTENSIONS

def main():
    parser = argparse.ArgumentParser(description="Count lines of code in a directory.")
    parser.add_argument("directory", type=str, help="Path to the project directory")
    parser.add_argument("--ext", nargs="+", help="File extensions to include (e.g., .py .js)", default=None)
    parser.add_argument("--ignore", nargs="+", help="Directories to ignore", default=DEFAULT_IGNORE_DIRS)
    parser.add_argument("--threads", type=int, default=4, help="Number of threads to use")
    parser.add_argument("--json", type=str, help="Export results to JSON file", default=None)
    parser.add_argument("--csv", type=str, help="Export results to CSV file", default=None)
    
    args = parser.parse_args()
    
    target_dir = Path(args.directory)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Error: Directory '{target_dir}' does not exist.")
        return

    extensions = args.ext if args.ext else DEFAULT_EXTENSIONS

    print(f"Analyzing {target_dir}...")
    results = analyze_directory(target_dir, extensions, args.ignore, args.threads)
    
    print_report(results, export_json=args.json, export_csv=args.csv)

if __name__ == "__main__":
    main()
