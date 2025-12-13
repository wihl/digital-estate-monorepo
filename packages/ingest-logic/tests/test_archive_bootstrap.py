import pytest
from pathlib import Path
import os
import stat
from ingest_logic.archive.bootstrap import bootstrap_archive

def test_bootstrap_valid_path(tmp_path):
    """
    Test that bootstrap_archive creates the expected structure in a valid, empty directory.
    """
    bootstrap_archive(tmp_path)
    
    people_dir = tmp_path / "people"
    assert people_dir.exists()
    assert people_dir.is_dir()

def test_bootstrap_path_not_exists(tmp_path):
    """
    Test that bootstrap_archive raises ValueError if the path does not exist.
    """
    non_existent = tmp_path / "ghost"
    with pytest.raises(ValueError, match="Path does not exist"):
        bootstrap_archive(non_existent)

def test_bootstrap_path_not_dir(tmp_path):
    """
    Test that bootstrap_archive raises ValueError if path is a file.
    """
    f = tmp_path / "file.txt"
    f.touch()
    
    with pytest.raises(ValueError, match="Path is not a directory"):
        bootstrap_archive(f)

def test_bootstrap_readonly(tmp_path):
    """
    Test that bootstrap_archive raises PermissionError if path is not writable.
    """
    # Create a readonly directory
    ro_dir = tmp_path / "readonly"
    ro_dir.mkdir()
    
    # Remove write permissions
    current_mode = ro_dir.stat().st_mode
    ro_dir.chmod(current_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
    
    try:
        # Note: In some Docker environments running as root, this might still succeed.
        # But assuming standard permissions, it should fail.
        # If running as root (likely in container), we might need to rely on the fact 
        # that we are checking os.access(W_OK) specifically.
        
        # If os.access check passes (root powers), but actual write fails, it might raise OSError.
        # However, our code explicitly checks os.access first.
        
        # If running as root, root usually has W_OK even if permission bits are off.
        # So this test might be flaky in root containers unless we drop privileges.
        # But let's try strict check expectation.
        
        if os.access(ro_dir, os.W_OK):
             pytest.skip("Running as root/privileged, cannot simulate readonly easily")
             
        with pytest.raises(PermissionError, match="Path is not writable"):
            bootstrap_archive(ro_dir)
            
    finally:
        # Restore permissions so cleanup can solve it
        ro_dir.chmod(stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)

def test_bootstrap_conflict(tmp_path):
    """
    Test that bootstrap_archive raises ValueError if 'people' exists as a file.
    """
    people_file = tmp_path / "people"
    people_file.touch()
    
    with pytest.raises(ValueError, match="Cannot create 'people' directory"):
        bootstrap_archive(tmp_path)
