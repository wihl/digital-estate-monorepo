from pathlib import Path
import os

def bootstrap_archive(root_path: Path) -> None:
    """
    Validates and initializes the Archive Root.
    
    1. Checks if path exists and is a directory.
    2. Checks for write permissions.
    3. Creates required subdirectories (people/) if missing.
    
    Raises:
        ValueError: If path is invalid.
        PermissionError: If path is not writable.
    """
    if not root_path.exists():
        raise ValueError(f"Path does not exist: {root_path}")
    
    if not root_path.is_dir():
        raise ValueError(f"Path is not a directory: {root_path}")
        
    if not os.access(root_path, os.W_OK):
        raise PermissionError(f"Path is not writable: {root_path}")
        
    # Initialize required structure
    people_dir = root_path / "people"
    if people_dir.exists() and not people_dir.is_dir():
        raise ValueError(f"Cannot create 'people' directory: a file with that name already exists in {root_path}")
        
    people_dir.mkdir(exist_ok=True)
