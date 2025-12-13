from pathlib import Path

def cleanup_temp_files(root_path: Path, pattern: str = "*.tmp") -> int:
    """
    Recursively finds and deletes files matching the pattern within root_path.
    
    Args:
        root_path: The root directory to scan.
        pattern: The glob pattern to match (default: *.tmp).
        
    Returns:
        int: The number of files deleted.
    """
    if not root_path.exists() or not root_path.is_dir():
        return 0
        
    count = 0
    # Recursive glob for the pattern
    # Note: rglob returns generator, allowing us to iterate efficiently
    for p in root_path.rglob(pattern):
        if p.is_file():
            try:
                p.unlink()
                count += 1
            except OSError as e:
                print(f"Failed to delete temp file {p}: {e}")
                
    return count
