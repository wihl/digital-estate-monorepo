import pytest
import os
import shutil
from pathlib import Path
from fastapi.testclient import TestClient

# Import the app. Adjust import based on your structure.
# Assuming main.py is in apps/desktop-private/backend/main.py
# and we are running pytest from apps/desktop-private/backend/
from main import app, config_manager

@pytest.fixture
def client():
    """
    FastAPI TestClient fixture.
    """
    return TestClient(app)

@pytest.fixture
def tmp_config_dir(tmp_path):
    """
    Creates a temporary directory for config.json and patches ConfigManager.
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    
    # Save original values
    orig_dir = config_manager.config_dir
    orig_file = config_manager.config_file
    
    # Patch
    config_manager.config_dir = config_dir
    config_manager.config_file = config_dir / "config.json"
    config_manager._ensure_dir()
    
    yield config_dir
    
    # Restore
    config_manager.config_dir = orig_dir
    config_manager.config_file = orig_file

@pytest.fixture
def tmp_archive_root(tmp_path):
    """
    Creates a temporary directory to act as the archive root.
    """
    path = tmp_path / "archive_root"
    path.mkdir()
    return path
