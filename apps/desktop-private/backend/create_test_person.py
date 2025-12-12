import os
import sys

# Add packages to path so we can import ingest_logic
sys.path.append(os.path.abspath("../../../packages"))

from ingest_logic.people.manager import PersonManager

# Point to the backend's local tmp_data
ROOT_DIR = os.path.abspath("tmp_data")
print(f"Creating person in: {ROOT_DIR}")

manager = PersonManager(ROOT_DIR)

person = manager.create_person(
    family="Doe",
    given="Jane",
    dob="1990-01-01",
    bio="Test subject for ingestion."
)

print(f"Created person: {person['display_name']} ({person['id']})")
print(f"Slug: {person['slug']}")
