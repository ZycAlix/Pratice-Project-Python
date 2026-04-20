from pathlib import Path
from typing import Iterator

def iter_log_files(directory: str) -> Iterator[Path]:
    """
    Yield all .log files under the given directory recursively.
    """
    base_path = Path(directory)

    if not base_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not base_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")
    
    yield from base_path.rglob("*.log")