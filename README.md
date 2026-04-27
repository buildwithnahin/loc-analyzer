# LOC Analyzer

A fast, multithreaded CLI tool to count lines of code in your projects. It breaks down total lines into blank, comment, and code lines, and supports filtering by extensions and ignoring specific directories.

## Project Structure
- `src/loc_analyzer/cli.py` - Argument parsing and entry point
- `src/loc_analyzer/scanner.py` - Multithreaded directory traversal
- `src/loc_analyzer/counter.py` - Core logic for parsing file syntax and counting
- `src/loc_analyzer/reporter.py` - Formatting console output and CSV/JSON export
- `src/loc_analyzer/config.py` - Default target extensions and ignored folders

## Running the Program

Run the analyzer via the `run.py` script:

```bash
python run.py /path/to/your/project
```

### Options
*   `--ext`: Specify extensions manually (e.g., `--ext .py .js`)
*   `--ignore`: Specify directories to ignore (overrides defaults like node_modules)
*   `--threads`: Number of threads to use (default 4)
*   `--json`: Export report to a JSON file
*   `--csv`: Export per-file details to a CSV file.

### Example
```bash
python run.py . --ext .py .html --threads 8 --json report.json
```
