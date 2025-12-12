import os
import uuid
import re
from typing import List, Dict, Optional
from ..common.fs_utils import write_safe
from ..common.yaml_utils import save_yaml, load_yaml

class PersonManager:
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.people_dir = os.path.join(root_path, "people")
        self._ensure_root()

    def _ensure_root(self):
        if not os.path.exists(self.people_dir):
            os.makedirs(self.people_dir, exist_ok=True)

    def _slugify(self, text: str) -> str:
        """Simple slugify: lowercase, remove special chars, replace spaces with dashes."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'\s+', '-', text).strip()
        return text

    def list_people(self) -> List[Dict]:
        people = []
        if not os.path.exists(self.people_dir):
            return people

        for entry in os.scandir(self.people_dir):
            if entry.is_dir():
                bio_path = os.path.join(entry.path, "bio.yaml")
                if os.path.exists(bio_path):
                    data = load_yaml(bio_path)
                    # Enrich with slug for frontend routing
                    if data:
                        data['slug'] = entry.name
                        people.append(data)
        return people

    def create_person(self, name: str, bio: str = "") -> Dict:
        base_slug = self._slugify(name)
        slug = base_slug
        
        # Handle duplicate slugs
        counter = 1
        while os.path.exists(os.path.join(self.people_dir, slug)):
            slug = f"{base_slug}-{counter}"
            counter += 1

        person_dir = os.path.join(self.people_dir, slug)
        os.makedirs(person_dir)

        person_id = str(uuid.uuid4())
        data = {
            "id": person_id,
            "name": name,
            "bio": bio
        }
        
        bio_path = os.path.join(person_dir, "bio.yaml")
        save_yaml(bio_path, data)
        
        data['slug'] = slug
        return data

    def get_person(self, slug: str) -> Optional[Dict]:
        path = os.path.join(self.people_dir, slug, "bio.yaml")
        if not os.path.exists(path):
            return None
        data = load_yaml(path)
        if data:
            data['slug'] = slug
        return data
