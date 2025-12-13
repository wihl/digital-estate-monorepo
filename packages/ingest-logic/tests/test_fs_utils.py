import pytest
from pathlib import Path
from ingest_logic.common.fs_utils import write_safe
import os

def test_safe_write_basics(tmp_path):
    """M1-005: safe_write works and leaves no temps."""
    target = tmp_path / "data.json"
    content = '{"key": "value"}'
    
    write_safe(str(target), content)
    
    assert target.exists()
    assert target.read_text() == content
    
    # Check for temps
    temps = list(tmp_path.glob("*.tmp"))
    assert len(temps) == 0

def test_safe_write_overwrite(tmp_path):
    """M1-005: safe_write overwrites correctly."""
    target = tmp_path / "data.json"
    target.write_text("old")
    
    write_safe(str(target), "new")
    assert target.read_text() == "new"

def test_safe_write_binary(tmp_path):
    """M1-005: safe_write handles binary."""
    target = tmp_path / "data.bin"
    content = b"\x00\x01\x02"
    
    write_safe(str(target), content)
    assert target.read_bytes() == content
