import hashlib

def _int_to_base36(n: int) -> str:
    """Converts an integer to a base36 string."""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    if n == 0:
        return "0"
    
    res = []
    while n > 0:
        n, r = divmod(n, 36)
        res.append(alphabet[r])
    return "".join(reversed(res))

def generate_person_id(family: str, given: str, suffix: str, dob: str) -> str:
    """
    Generates a unique ID based on the canonical identity string:
    <family>|<given>|<suffix>|<YYYY-MM-DD>
    
    The string is UTF-8 encoded, treated as a big-endian integer, 
    and converted to Base36.
    """
    # Normalize inputs
    family = (family or "").strip()
    given = (given or "").strip()
    suffix = (suffix or "").strip()
    dob = (dob or "").strip()
    
    canonical = f"{family}|{given}|{suffix}|{dob}"
    
    # Mathematical analysis implementation:
    # "interpreted as utf8_bytes expressed as a big-median integer X"
    utf8_bytes = canonical.encode('utf-8')
    integer_value = int.from_bytes(utf8_bytes, byteorder='big')
    
    base36_id = _int_to_base36(integer_value)
    return base36_id

def get_shard_path(person_id: str) -> str:
    """
    Returns the relative shard path for a person ID.
    Format: /p0p1/p2p3/
    Example: 13x9q2z -> 13/x9/
    """
    # Pad with 0 if somehow shorter than 4 chars (unlikely for proper names)
    clean_id = person_id.lower().ljust(4, '0')
    return f"{clean_id[0:2]}/{clean_id[2:4]}"
