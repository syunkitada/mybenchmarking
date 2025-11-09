"""System profile storage operations."""

from pathlib import Path
from typing import List

from ..models.system import SystemProfile
from .base import load_and_validate_json, save_model_to_json


def save_system_profile(profile: SystemProfile, systems_dir: Path) -> Path:
    """
    Save a system profile to JSON file.

    Args:
        profile: SystemProfile to save
        systems_dir: Directory to save profiles in

    Returns:
        Path to saved profile file

    Raises:
        IOError: If file cannot be written
    """
    systems_dir.mkdir(parents=True, exist_ok=True)
    filepath = systems_dir / f"{profile.profile_id}.json"
    save_model_to_json(filepath, profile)
    return filepath


def load_system_profile(profile_id: str, systems_dir: Path) -> SystemProfile:
    """
    Load a system profile from JSON file.

    Args:
        profile_id: Profile identifier
        systems_dir: Directory containing profiles

    Returns:
        Loaded SystemProfile

    Raises:
        FileNotFoundError: If profile file doesn't exist
        ValidationError: If JSON doesn't match schema
    """
    filepath = systems_dir / f"{profile_id}.json"
    return load_and_validate_json(filepath, SystemProfile)


def list_system_profiles(systems_dir: Path) -> List[SystemProfile]:
    """
    List all system profiles in the directory.

    Args:
        systems_dir: Directory containing profiles

    Returns:
        List of SystemProfile objects, sorted by profile_id

    Raises:
        ValidationError: If any JSON file is invalid
    """
    if not systems_dir.exists():
        return []

    profiles = []
    for filepath in sorted(systems_dir.glob("*.json")):
        try:
            profile = load_and_validate_json(filepath, SystemProfile)
            profiles.append(profile)
        except Exception as e:
            # Log error but continue processing other files
            print(f"Warning: Failed to load {filepath}: {e}")

    return profiles


def profile_exists(profile_id: str, systems_dir: Path) -> bool:
    """
    Check if a system profile exists.

    Args:
        profile_id: Profile identifier
        systems_dir: Directory containing profiles

    Returns:
        True if profile exists, False otherwise
    """
    filepath = systems_dir / f"{profile_id}.json"
    return filepath.exists()
