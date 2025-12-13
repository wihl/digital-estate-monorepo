import pytest
import os
from pathlib import Path

def test_health_ok(client):
    """M1-001: Health check returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Backend is running"}

def test_config_initially_null(client, tmp_config_dir):
    """M1-003: Config is null initially."""
    response = client.get("/config")
    assert response.status_code == 200
    assert response.json() == {"archive_root": None}

def test_set_archive_root_persistence(client, tmp_config_dir, tmp_archive_root):
    """M1-003: Set archive root persists."""
    # Set it
    payload = {"path": str(tmp_archive_root)}
    response = client.post("/config/archive-root", json=payload)
    assert response.status_code == 200
    assert response.json()["archive_root"] == str(tmp_archive_root)
    
    # Verify persistence (by getting it back)
    # Since config_manager reads from disk on load, this verifies disk write.
    response = client.get("/config")
    assert response.status_code == 200
    assert response.json()["archive_root"] == str(tmp_archive_root)

def test_set_archive_root_creates_people_dir(client, tmp_config_dir, tmp_archive_root):
    """M1-004: Setting archive root bootstraps people directory."""
    payload = {"path": str(tmp_archive_root)}
    response = client.post("/config/archive-root", json=payload)
    assert response.status_code == 200
    
    people_dir = tmp_archive_root / "people"
    assert people_dir.exists()
    assert people_dir.is_dir()

def test_set_archive_root_rejects_missing_path(client, tmp_config_dir, tmp_path):
    """M1-003/004: Rejects non-existent path."""
    ghost = tmp_path / "ghost"
    payload = {"path": str(ghost)}
    response = client.post("/config/archive-root", json=payload)
    assert response.status_code == 400
    assert "Path does not exist" in response.json()["detail"]

def test_set_archive_root_requires_writable(client, tmp_config_dir, tmp_path):
    """M1-004: Rejects read-only path."""
    ro_dir = tmp_path / "readonly"
    ro_dir.mkdir()
    # Remove write perms
    import stat
    ro_dir.chmod(ro_dir.stat().st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
    
    try:
        if os.access(ro_dir, os.W_OK):
             pytest.skip("Running as root/privileged, cannot simulate readonly easily")
             
        payload = {"path": str(ro_dir)}
        response = client.post("/config/archive-root", json=payload)
        assert response.status_code == 403
        assert "Permission denied" in response.json()["detail"]
    finally:
        ro_dir.chmod(stat.S_IWUSR | stat.S_IRUSR | stat.S_IXUSR)

def test_resolved_paths(client, tmp_config_dir, tmp_path):
    """M1-005: Verifies path resolution."""
    # Create a dir manually
    target = tmp_path / "target"
    target.mkdir()
    
    # cd to tmp_path roughly for relative path test? 
    # Hard to change CWD of the running app safely in tests. 
    # We can pass an absolute path that contains .. though
    
    complex_path = target / ".." / "target"
    payload = {"path": str(complex_path)}
    
    response = client.post("/config/archive-root", json=payload)
    assert response.status_code == 200
    resolved = response.json()["archive_root"]
    assert resolved == str(target.resolve())
