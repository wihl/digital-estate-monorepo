# Project Invariants

These rules are non-negotiable architectural constraints.

## 1. Filesystem is Source of Truth
- The state of the digital estate is defined **solely** by the files on the disk (YAML, media, directories).
- **SQLite is a disposable index**. It can be deleted and rebuilt from the filesystem at any time without data loss. It is used only for FTS5 search and fast list queries.
- We do not store "original" data in the database.

## 2. YAML Round-Trip Integrity
- We use `ruamel.yaml` for all YAML operations.
- Edits must **preserve comments**, ordering, and structure of existing files.
- We must not clobber user-added comments in `person.yaml` or `timeline.yaml`.

## 3. Safe Writes Only
- All file writes must use the `safe_write` utility (write to `filename.tmp` -> fsync -> rename).
- This prevents data corruption on power loss or crash.

## 4. ExFAT Compatibility
- The storage target is likely an external SSD formatted as ExFAT.
- **No Symlinks**: Do not use symlinks.
- **Case-Insensitivity**: Treat `File.txt` and `file.txt` as the same file.
- **Path Lengths**: Keep directory nesting reasonable.
