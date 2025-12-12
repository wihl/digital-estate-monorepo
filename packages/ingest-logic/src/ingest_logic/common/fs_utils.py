import os
import shutil
from typing import Union

def write_safe(path: str, content: Union[str, bytes]) -> None:
    """
    Writes content to a file using the 'Safe Write' pattern:
    1. Write to {path}.tmp
    2. Flush and fsync
    3. Rename {path}.tmp to {path} (atomic-ish replacement)
    
    This mitigates data corruption on ExFAT if power is lost during write.
    """
    tmp_path = path + ".tmp"
    mode = 'wb' if isinstance(content, bytes) else 'w'
    
    try:
        with open(tmp_path, mode) as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
            
        os.replace(tmp_path, path)
    except Exception as e:
        # cleanup tmp file if it exists and we failed
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise e

async def write_safe_stream(path: str, file_obj) -> None:
    """
    Async streaming version of write_safe for large files.
    'file_obj' should be a fastapi UploadFile or similar that has an async read method.
    """
    import aiofiles
    tmp_path = path + ".tmp"
    
    try:
        async with aiofiles.open(tmp_path, 'wb') as f:
            while True:
                chunk = await file_obj.read(1024 * 1024)  # 1MB chunks
                if not chunk:
                    break
                await f.write(chunk)
            await f.flush()
            # fsync needs to be done on the file descriptor
            os.fsync(f.file.fileno())
            
        os.replace(tmp_path, path)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise e
