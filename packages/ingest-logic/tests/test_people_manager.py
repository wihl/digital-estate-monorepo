import pytest
import os
import sys
from pathlib import Path

# Fix path to include packages if not already
# This is a bit hacky but ensures tests run in various environments
# Using conftest logic is better but this explicit fix helps for now
packages_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(packages_dir / "ingest-logic" / "src"))
sys.path.append(str(packages_dir / "contracts" / "src"))

from ingest_logic.people.manager import PersonManager
from contracts.models import Person, PersonNameType

@pytest.fixture
def person_manager(tmp_path):
    return PersonManager(str(tmp_path))

def test_create_person_returns_object(person_manager):
    """Test that create_person returns a Person object, not a dict."""
    p = person_manager.create_person(
        family="Test",
        given="User",
        dob="2000-01-01",
        bio="A test user"
    )
    
    assert isinstance(p, Person)
    assert p.names[0].surname == "Test"
    assert p.names[0].given == "User"
    assert p.vitals.birth.date == "2000-01-01"
    assert p.bio == "A test user"
    assert p.id is not None
    # Check injected runtime fields
    assert p.display_name == "Test, User"
    assert p.slug is not None

def test_persistence_integrity(person_manager):
    """Test that saving and reloading preserves data and type."""
    original = person_manager.create_person("Save", "Load", "1990-09-09")
    
    # Reload via get
    loaded = person_manager.get_person(original.slug)
    
    assert isinstance(loaded, Person)
    assert loaded.id == original.id
    assert loaded.names[0].surname == "Save"
    assert loaded.names[0].given == "Load"
    
def test_list_people_returns_objects(person_manager):
    """Test list_people returns list of Person objects."""
    person_manager.create_person("List", "One", "2020-01-01")
    person_manager.create_person("List", "Two", "2020-02-02")
    
    people = person_manager.list_people()
    assert len(people) == 2
    assert all(isinstance(p, Person) for p in people)

def test_corrupt_data_handling(person_manager, tmp_path):
    """Test that reading invalid data raises error (get) or handles gracefully (list)."""
    # Create a manually valid structure but violate strict schema? 
    # Or just garbage.
    
    # 1. Create a directory structure manually
    bad_dir = tmp_path / "people" / "bad_shard" / "bad_person--1234"
    bad_dir.mkdir(parents=True)
    
    bio = bad_dir / "bio.yaml"
    
    # Missing required 'names'
    bio.write_text('id: "1234"\nvitals:\n  birth:\n    date: "2000-01-01"')
    
    # Rel path
    rel_path = f"bad_shard/bad_person--1234"
    
    # get_person should raise ValueError or similar
    with pytest.raises(ValueError):
        person_manager.get_person(rel_path)
        
    # list_people effectively skips? Or logs.
    # Our implementation had a broad try/except pass for list.
    people = person_manager.list_people()
    assert len(people) == 0
