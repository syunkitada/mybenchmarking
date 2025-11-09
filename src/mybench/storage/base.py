"""Base storage functions for JSON file operations."""

import json
import tempfile
from pathlib import Path
from typing import Any, Dict, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def atomic_save_json(filepath: Path, data: Dict[str, Any]) -> None:
    """
    Save JSON data to file atomically using temp-and-move pattern.

    Args:
        filepath: Target file path
        data: Dictionary to save as JSON

    Raises:
        IOError: If file operations fail
    """
    # Ensure parent directory exists
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Write to temporary file first
    temp_fd, temp_path = tempfile.mkstemp(
        dir=filepath.parent, prefix=f".{filepath.name}.", suffix=".tmp"
    )

    try:
        with open(temp_fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            f.write("\n")  # Trailing newline for Git-friendly files

        # Atomic move
        Path(temp_path).replace(filepath)
    except Exception:
        # Clean up temp file on error
        Path(temp_path).unlink(missing_ok=True)
        raise


def load_and_validate_json(filepath: Path, model: type[T]) -> T:
    """
    Load JSON file and validate against Pydantic model.

    Args:
        filepath: File path to load
        model: Pydantic model class for validation

    Returns:
        Validated model instance

    Raises:
        FileNotFoundError: If file doesn't exist
        ValidationError: If JSON doesn't match model schema
        JSONDecodeError: If file is not valid JSON
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return model.model_validate(data)


def save_model_to_json(filepath: Path, model: BaseModel) -> None:
    """
    Save Pydantic model to JSON file atomically.

    Args:
        filepath: Target file path
        model: Pydantic model instance

    Raises:
        IOError: If file operations fail
    """
    data = model.model_dump(mode="json")
    atomic_save_json(filepath, data)
