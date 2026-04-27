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
    methods: int = 0
    operators: int = 0
    operands: int = 0

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

METHOD_PATTERNS = {
    '.py': re.compile(r'^\s*def\s+\w+\s*\('),
    '.js': re.compile(r'^\s*(?:async\s+)?(?:function\s+\w+\s*\(|\w+\s*\([^)]*\)\s*\{)'),
    '.java': re.compile(r'^\s*(?:public|protected|private|static|final|\s)*[\w\<\>\[\]]+\s+\w+\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*\{?'),
    '.cpp': re.compile(r'^\s*(?:virtual|inline|static|explicit|\s)*[\w\<\>\[\]\:\*]+\s+[\w\:]+\s*\([^)]*\)\s*(?:const)?\s*\{?'),
    '.c': re.compile(r'^\s*(?:inline|static|\s)*[\w\<\>\[\]\*]+\s+\w+\s*\([^)]*\)\s*\{?'),
    '.h': re.compile(r'^\s*(?:virtual|inline|static|explicit|\s)*[\w\<\>\[\]\:\*]+\s+[\w\:]+\s*\([^)]*\)\s*(?:const)?\s*(?:\{|;)'),
    '.hpp': re.compile(r'^\s*(?:virtual|inline|static|explicit|\s)*[\w\<\>\[\]\:\*]+\s+[\w\:]+\s*\([^)]*\)\s*(?:const)?\s*(?:\{|;)'),
    '.ts': re.compile(r'^\s*(?:public|private|protected|async|static|\s)*(?:function\s+\w+\s*\(|\w+\s*\([^)]*\)\s*\{)'),
    '.go': re.compile(r'^\s*func\s+(?:\([^)]+\)\s+)?\w+\s*\('),
    '.rs': re.compile(r'^\s*(?:pub\s+(?:\([^\)]+\)\s+)?)?(?:async\s+)?fn\s+\w+\s*\<?\w*\>?\s*\('),
}

OPERATOR_PATTERN = re.compile(r'(\+{1,2}|\-{1,2}|\*|\/|%|=|==|!=|<=|>=|<|>|&&|\|\||!|&|\||\^|~|\+=|\-=|\*=|/=)')
OPERAND_PATTERN = re.compile(r'\b[a-zA-Z_0-9]+\b')

def count_lines(filepath: str, extension: str) -> FileStats:
    """Counts total, blank, comment, and code lines in a file."""
    stats = FileStats(path=filepath, extension=extension)
    syntax = COMMENT_SYNTAX.get(extension, {'single': '#', 'multi_start': None, 'multi_end': None})
    method_regex = METHOD_PATTERNS.get(extension)
    
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
                    stats.operators += len(OPERATOR_PATTERN.findall(stripped))
                    stats.operands += len(OPERAND_PATTERN.findall(stripped))
                    if method_regex and method_regex.search(line):
                        stats.methods += 1
                    
    except Exception as e:
        pass # Ignore unreadable files
        
    return stats
