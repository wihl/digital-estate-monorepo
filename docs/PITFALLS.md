# Pitfalls

## 1. SQLite sync issues
- **Symptom**: Search results return deleted items or miss new items.
- **Cause**: The SQLite index is out of sync with the filesystem.
- **Fix**: Run the `/reindex` endpoint or restart the backend (if on-startup scan is enabled).

## 2. "File busy" on Windows/ExFAT
- **Symptom**: `PermissionError` when writing files.
- **Cause**: Antivirus or file explorer locking the file during a write.
- **Fix**: Use `safe_write` retries or ensure file handles are closed immediately after use.

## 3. Docker Volume Permissions
- **Symptom**: Backend cannot write to `tmp_data` or mounted SSD.
- **Cause**: UID/GID mismatch between Docker container and host.
- **Fix**: Ensure the mounted directory is readable/writable by the container user (root by default in our dev setup, which usually works, but watch out on Linux).
