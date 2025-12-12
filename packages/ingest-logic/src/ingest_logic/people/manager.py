import os
import shutil
from typing import List, Dict, Optional
from ..common.fs_utils import write_safe
from ..common.yaml_utils import save_yaml, load_yaml
from .identity import generate_person_id, get_shard_path
import re

class PersonManager:
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.people_dir = os.path.join(root_path, "people")
        self._ensure_root()

    def _ensure_root(self):
        if not os.path.exists(self.people_dir):
            os.makedirs(self.people_dir, exist_ok=True)

    def _slugify_name(self, name: str) -> str:
        """Sanitize name for directory usage (ExFAT safe)."""
        # Remove control chars and restricted ExFAT chars: * " / \ < > : ? |
        name = re.sub(r'[\x00-\x1f*"/\\<>:?|]', '', name)
        name = name.strip().replace(' ', '_')
        return name

    def create_person(self, family: str, given: str, dob: str, suffix: str = "", bio: str = "") -> Dict:
        person_id = generate_person_id(family, given, suffix, dob)
        shard = get_shard_path(person_id)
        
        # Directory Name: <ReadableName>--<ShortID>
        # ReadableName: Family, Given
        readable_name = f"{family}, {given}"
        if suffix:
            readable_name += f" {suffix}"
        
        safe_name = self._slugify_name(readable_name)
        dir_name = f"{safe_name}--{person_id}"
        
        # Full Path: /people/<shard>/<dir_name>
        target_dir = os.path.join(self.people_dir, shard, dir_name)
        
        if os.path.exists(target_dir):
            # Idempotency check: if ID matches, it's the same person definition? 
            # Or collision? For now, we assume same person.
            pass
        else:
            os.makedirs(target_dir, exist_ok=True)

        data = {
            "id": person_id,
            "names": [{
                "type": "primary",
                "given": given,
                "surname": family,
                "suffix": suffix
            }],
            "vitals": {
                "birth": {
                    "date": dob
                }
            },
            "bio": bio
        }
        
        bio_path = os.path.join(target_dir, "bio.yaml")
        if not os.path.exists(bio_path):
             save_yaml(bio_path, data)
        
        data['slug'] = os.path.join(shard, dir_name) # relative path as slug/locator
        data['display_name'] = f"{family}, {given}".strip(', ')
        return data

    def list_people(self) -> List[Dict]:
        """
        Scans arbitrarily deep to find bio.yaml files.
        Optimized to look mainly in 2-level shards if we strictly enforce it, 
        but os.walk is safer for MVP correctness.
        """
        people = []
        if not os.path.exists(self.people_dir):
            return people

        for root, dirs, files in os.walk(self.people_dir):
            if "bio.yaml" in files:
                try:
                    data = load_yaml(os.path.join(root, "bio.yaml"))
                    if data:
                        # Construct relative path slug
                        rel_path = os.path.relpath(root, self.people_dir)
                        data['slug'] = rel_path
                        
                        # Flatten name for simple listing if needed
                        primary_name = next((n for n in data.get('names', []) if n.get('type') == 'primary'), {})
                        flat_name = f"{primary_name.get('surname', '')}, {primary_name.get('given', '')}"
                        data['display_name'] = flat_name.strip(', ')
                        
                        people.append(data)
                except Exception:
                    pass # Skip unreadable
        return people

    def get_person(self, relative_path: str) -> Optional[Dict]:
        """
        Retrieves person by relative path from people root.
        e.g. 'a1/b2/Doe_John--123.../bio.yaml'
        """
        # Sanity check path traversal
        if ".." in relative_path or relative_path.startswith("/"):
            return None
            
        full_path = os.path.join(self.people_dir, relative_path, "bio.yaml")
        if not os.path.exists(full_path):
            return None
            
        data = load_yaml(full_path)
        if data:
            data['slug'] = relative_path
        return data
