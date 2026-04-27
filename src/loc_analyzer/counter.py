import re
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class FileStats:
    path: str
    extension: str
    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0

COMMENT_SYNTAX = {
    '.py': {'single': '#', 'multi_start': '"""', 'multi_end': '"""'},
    '.js': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.java': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.cpp': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.c': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.h': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.hpp': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.ts': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.go': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
    '.rs': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
}

def count_lines(filepath: str, extension: str) -> FileStats:
    """Counts total, blank, comment, and code lines in a file."""
    stats = FileStats(path=filepath, extension=extension)
    syntax = COMMENT_SYNTAX.get(extension, {'single': '#', 'multi_start': None, 'multi_end': None})
    
    in_multiline_comment = False
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stats.total_lines += 1
                stripped = line.strip()
                
                if not stripped:
                    stats.blank_lines += 1
                    continue
                
                if syntax['multi_start'] and syntax['multi_end']:
                    if in_multiline_comment:
                        stats.comment_lines += 1
                        if syntax['multi_end'] in stripped:
                            in_multiline_comment = False
                        continue
                    
                    if stripped.startswith(syntax['multi_start']):
                        stats.comment_lines += 1
                        if syntax['multi_end'] not in stripped[len(syntax['multi_start']):]:
                            in_multiline_comment = True
                        continue
                
                if stripped.startswith(syntax['single']):
                    stats.comment_lines += 1
                else:
                    stats.code_lines += 1
                    
    except Exception as e:
        pass # Ignore unreadable files
        
    return stats
