import os
import sys

# Add packages to path so we can import ingest_logic and contracts
package_root = os.path.abspath("../../../packages")
sys.path.append(os.path.join(package_root, "ingest-logic", "src"))
sys.path.append(os.path.join(package_root, "contracts", "src"))
     
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
 
print(f"Created person: {person.display_name} ({person.id})")
print(f"Slug: {person.slug}")
