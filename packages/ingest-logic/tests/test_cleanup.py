import pytest
from pathlib import Path
from ingest_logic.archive.cleanup import cleanup_temp_files

def test_cleanup_removes_tmp_files(tmp_path):
    """
    Test that cleanup_temp_files removes files matching pattern.
    """
    # Create mix of files
    (tmp_path / "keep.txt").touch()
    (tmp_path / "waste.tmp").touch()
    
    # subdirectory
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "keep_sub.txt").touch()
    (sub / "waste_sub.tmp").touch()
    
    deleted_count = cleanup_temp_files(tmp_path)
    
    assert deleted_count == 2
    assert (tmp_path / "keep.txt").exists()
    assert not (tmp_path / "waste.tmp").exists()
    assert (sub / "keep_sub.txt").exists()
    assert not (sub / "waste_sub.tmp").exists()

def test_cleanup_custom_pattern(tmp_path):
    """
    Test cleanup with custom pattern.
    """
    (tmp_path / "waste.log").touch()
    (tmp_path / "keep.tmp").touch() 
    
    deleted_count = cleanup_temp_files(tmp_path, pattern="*.log")
    
    assert deleted_count == 1
    assert not (tmp_path / "waste.log").exists()
    assert (tmp_path / "keep.tmp").exists()

def test_cleanup_invalid_path(tmp_path):
    """
    Test cleanup handles non-existent paths gracefully.
    """
    count = cleanup_temp_files(tmp_path / "ghost")
    assert count == 0
