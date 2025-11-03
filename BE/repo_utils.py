# repo_utils.py to handle git repository operations that are easy to do in pure Python
import os
import tempfile
import shutil
from git import Repo

# Clone a git repository to a temporary directory
def clone_repo(url: str):
    tmp = tempfile.mkdtemp(prefix="codegenius_")
    try:
        Repo.clone_from(url, tmp, depth=1)
        return tmp, tmp
    except Exception as e:
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError(f"Clone failed: {e}")
    
# Collect all files in the repository, ignoring certain directories
def collect_files(root: str) -> list:
    files = []
    ignore = {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignore]
        for f in filenames:
            files.append(os.path.join(dirpath, f))
    return files

# Generate a tree-like string representation of the file structure
def write_tree(root: str, files: list) -> str:
    lines = []
    for f in sorted(files):
        rel = os.path.relpath(f, root)
        depth = rel.count(os.sep)
        indent = "  " * depth
        lines.append(f"{indent}└─ {os.path.basename(f)}")
    return "\n".join(lines) if lines else "Empty repository."

# Get current timestamp in EAT timezone
def get_timestamp() -> str:
    """Return ISO 8601 timestamp localized to East African Time (EAT / UTC+3)."""
    from datetime import datetime, timezone, timedelta
    eat_zone = timezone(timedelta(hours=3))
    return datetime.now(eat_zone).isoformat(timespec="seconds").replace("+03:00", "EAT")
