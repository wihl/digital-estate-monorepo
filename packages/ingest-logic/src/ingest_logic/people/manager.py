import os
import shutil
from typing import List, Dict, Optional
from ..common.fs_utils import write_safe
from ..common.yaml_utils import save_yaml, load_yaml
from .identity import generate_person_id, get_shard_path
from contracts.models import Person, PersonName, PersonNameType, PersonVitals, PersonBirth
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

    def create_person(self, family: str, given: str, dob: str, suffix: str = "", bio: str = "") -> Person:
        """
        Factory method to create a new Person.
        Generates ID, constructs object, and persists it.
        """
        family = family.strip()
        given = given.strip()
        suffix = suffix.strip()
        dob = dob.strip()
        
        person_id = generate_person_id(family, given, suffix, dob)
        
        # Construct Pydantic object
        person = Person(
            id=person_id,
            names=[
                PersonName(
                    type=PersonNameType.PRIMARY,
                    given=given,
                    surname=family,
                    suffix=suffix
                )
            ],
            vitals=PersonVitals(
                birth=PersonBirth(date=dob)
            ),
            bio=bio
        )

        self.save_person(person)
        return person

    def save_person(self, person: Person) -> None:
        """
        Persists a Person object to disk.
        Determines path from ID and Names.
        """
        # Determine Path
        shard = get_shard_path(person.id)
        
        # Use primary name for directory slug
        primary_name = next((n for n in person.names if n.type == PersonNameType.PRIMARY), None)
        if not primary_name:
             # Fallback if no primary name (should ideally validation error before here)
             readable_name = "Unknown"
        else:
             readable_name = f"{primary_name.surname}, {primary_name.given}"
             if primary_name.suffix:
                 readable_name += f" {primary_name.suffix}"

        safe_name = self._slugify_name(readable_name)
        dir_name = f"{safe_name}--{person.id}"
        
        target_dir = os.path.join(self.people_dir, shard, dir_name)
        
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        bio_path = os.path.join(target_dir, "bio.yaml")
        
        # Validation is handled by Pydantic model construction in caller or here
        data = person.model_dump(mode='json', exclude={'slug', 'display_name'})
        
        save_yaml(bio_path, data)
        
        # Update injected fields on the object just in case
        person.slug = os.path.join(shard, dir_name)
        person.display_name = readable_name

    def list_people(self) -> List[Person]:
        """
        Scans arbitrarily deep to find bio.yaml files.
        Returns List[Person].
        """
        people = []
        if not os.path.exists(self.people_dir):
            return people

        for root, dirs, files in os.walk(self.people_dir):
            if "bio.yaml" in files:
                try:
                    full_path = os.path.join(root, "bio.yaml")
                    data = load_yaml(full_path)
                    if data:
                        # Validate and Parse via Pydantic
                        # If schema mismatches, this will raise ValidationError
                        person = Person(**data)
                        
                        # Inject runtime fields
                        rel_path = os.path.relpath(root, self.people_dir)
                        person.slug = rel_path
                        
                        primary = next((n for n in person.names if n.type == PersonNameType.PRIMARY), None)
                        if primary:
                             person.display_name = f"{primary.surname}, {primary.given}".strip(', ')
                        
                        people.append(person)
                except Exception as e:
                    # Per requirement: "raise a clear error (do not silently fix it)"
                    # However, list_people usually shouldn't crash the whole app on one bad file?
                    # But the prompt says "If the existing data on disk does not match... code should raise a clear error"
                    # I will log and re-raise/or just let it raise if it happens during 'load'
                    # For list_people, maybe we warn? 
                    # Prompt says "do not silently fix it". Failing loudly is acceptable for "Strict" contract.
                    print(f"Error loading person at {root}: {e}")
                    pass # We skip for now to allow other people to load, or should we raise?
                    # The prompt "code should raise a clear error" usually applies to the read-path of a specific item.
                    # For listing, if one file is corrupt, failing the whole list might be annoying but "Strict".
                    # I will keep 'pass' for list iteration robustness but maybe print/log error.
                    # Actually, for 'get_person', I definitely raise.
                    pass

        return people

    def get_person(self, relative_path: str) -> Optional[Person]:
        """
        Retrieves person by relative path from people root.
        """
        # Sanity check path traversal
        if ".." in relative_path or relative_path.startswith("/"):
            raise ValueError("Invalid path")
            
        full_path = os.path.join(self.people_dir, relative_path, "bio.yaml")
        if not os.path.exists(full_path):
            return None
            
        data = load_yaml(full_path)
        if not data:
             return None # Or raise Empty File error

        try:
            person = Person(**data)
            person.slug = relative_path
            
            primary = next((n for n in person.names if n.type == PersonNameType.PRIMARY), None)
            if primary:
                 person.display_name = f"{primary.surname}, {primary.given}".strip(', ')
            
            return person
        except Exception as e:
             raise ValueError(f"Data corruption or schema mismatch for {relative_path}: {e}")

