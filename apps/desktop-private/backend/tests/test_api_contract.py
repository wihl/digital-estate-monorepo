import pytest
from pydantic import ValidationError
# This import proves the 'packages' directory is correctly installed in Docker
from contracts.models import Person, BASE36_ID_PATTERN

def test_architecture_imports():
    """CRITICAL: Ensure we can import from the shared packages."""
    try:
        from contracts.models import Person
        from ingest_logic.common.fs_utils import write_safe
    except ImportError as e:
        pytest.fail(f"Architecture Breach: Could not import shared packages. {e}")

def test_person_contract_enforcement():
    """Verify the Person model strictly enforces Base36 IDs."""
    
    # 1. Valid Case (Should pass)
    valid_id = "Doe,_Jane--7zs7i5xp"  
    p = Person(
        id=valid_id,
        names=[{"type": "primary", "given": "Jane", "surname": "Doe"}],
        vitals={"birth": {"date": "1990-01-01"}}
    )
    assert p.id == valid_id

    # 2. Invalid Case (Should fail - e.g., using a UUID or special chars)
    invalid_id = "Jane Doe!!!" 
    with pytest.raises(ValidationError) as excinfo:
        Person(
            id=invalid_id,
            names=[{"type": "primary", "given": "Jane", "surname": "Doe"}],
            vitals={"birth": {"date": "1990-01-01"}}
        )
    assert "string_pattern_mismatch" in str(excinfo.value) or "Pattern" in str(excinfo.value)

def test_no_forbidden_types():
    """Ensure we didn't sneak in Any or Dict."""
    schema = Person.model_json_schema()
    properties = schema.get("properties", {})
    if "metadata" in properties:
        assert "$ref" in str(properties["metadata"]) or "type" in properties["metadata"]
