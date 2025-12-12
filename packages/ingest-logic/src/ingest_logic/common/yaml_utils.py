from ruamel.yaml import YAML
from typing import Any
from .fs_utils import write_safe
from io import StringIO

def get_yaml() -> YAML:
    """Configures ruamel.yaml to preserve comments and layout."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)
    return yaml

def load_yaml(path: str) -> Any:
    """Safe loads a YAML file using ruamel."""
    if not os.path.exists(path):
        return None
    
    yaml = get_yaml()
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.load(f)

def save_yaml(path: str, data: Any) -> None:
    """Saves data to YAML using safe write pattern."""
    yaml = get_yaml()
    stream = StringIO()
    yaml.dump(data, stream)
    content = stream.getvalue()
    write_safe(path, content)

import os
