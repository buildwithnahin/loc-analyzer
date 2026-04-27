import json
import csv
from typing import List, Dict
from collections import defaultdict
from .counter import FileStats

def print_report(results: List[FileStats], export_json: str = None, export_csv: str = None):
    if not results:
        print("No matching files found.")
        return

    # Aggregate by extension
    summary_by_ext = defaultdict(lambda: {"files": 0, "total": 0, "blank": 0, "comment": 0, "code": 0})
    total = {"files": 0, "total": 0, "blank": 0, "comment": 0, "code": 0}

    for stats in results:
        ext = stats.extension
        summary_by_ext[ext]["files"] += 1
        summary_by_ext[ext]["total"] += stats.total_lines
        summary_by_ext[ext]["blank"] += stats.blank_lines
        summary_by_ext[ext]["comment"] += stats.comment_lines
        summary_by_ext[ext]["code"] += stats.code_lines
        
        total["files"] += 1
        total["total"] += stats.total_lines
        total["blank"] += stats.blank_lines
        total["comment"] += stats.comment_lines
        total["code"] += stats.code_lines

    print(f"\n{'-'*80}")
    print(f"{'Language/Ext':<15} | {'Files':<6} | {'Total Lines':<12} | {'Blank':<10} | {'Comment':<10} | {'Code':<10}")
    print(f"{'-'*80}")
    
    for ext, s in summary_by_ext.items():
        print(f"{ext:<15} | {s['files']:<6} | {s['total']:<12} | {s['blank']:<10} | {s['comment']:<10} | {s['code']:<10}")
    
    print(f"{'-'*80}")
    print(f"{'TOTAL':<15} | {total['files']:<6} | {total['total']:<12} | {total['blank']:<10} | {total['comment']:<10} | {total['code']:<10}")
    print(f"{'-'*80}\n")

    if export_json:
        with open(export_json, 'w') as f:
            json.dump({
                "summary_by_extension": summary_by_ext,
                "total": total,
                "files": [s.__dict__ for s in results]
            }, f, indent=4)
        print(f"Exported JSON to {export_json}")

    if export_csv:
        with open(export_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Path", "Extension", "Total Lines", "Blank Lines", "Comment Lines", "Code Lines"])
            for r in results:
                writer.writerow([r.path, r.extension, r.total_lines, r.blank_lines, r.comment_lines, r.code_lines])
        print(f"Exported CSV to {export_csv}")
