import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Set
from .counter import count_lines, FileStats

def analyze_directory(root_dir: Path, extensions: List[str], ignore_dirs: List[str], threads: int) -> List[FileStats]:
    """Recursively traverses the directory and counts lines using threads."""
    files_to_process = []
    
    # Normalize extensions to ensure they start with '.'
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    ignore_set = set(ignore_dirs)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter directories mapped in-place to avoid going into ignored dirs
        dirnames[:] = [d for d in dirnames if d not in ignore_set]
        
        for file in filenames:
            ext = Path(file).suffix
            if ext in extensions:
                files_to_process.append((os.path.join(dirpath, file), ext))
                
    results = []
    
    # Using ThreadPoolExecutor for concurrent file parsing
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_file = {
            executor.submit(count_lines, filepath, ext): filepath 
            for filepath, ext in files_to_process
        }
        
        for future in as_completed(future_to_file):
            stats = future.result()
            if stats.total_lines > 0:
                results.append(stats)
                
    return results
