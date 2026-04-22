from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from log_analyzer.analyzer import analyze_entries, merge_analysis_results
from log_analyzer.parser import iter_entries_from_file

def analyze_single_file(path: Path) -> dict:
    """
    Read and analyze one log file.
    Returns a partial analysis result.
    """
    entries = iter_entries_from_file(path)
    return analyze_entries(entries)

def analyze_files_concurrently(paths, max_workers: int=4) -> dict:
    """
    Analyze multiple log files concurrently using a thread pool.
    """

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        partial_results = list(executor.map(analyze_single_file, paths))

    return merge_analysis_results(partial_results)