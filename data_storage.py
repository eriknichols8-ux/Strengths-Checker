"""
Data storage module for saving and loading people and their CliftonStrengths.
"""

import json
import os
from typing import Dict, List, Optional


DATA_FILE = "saved_people.json"


def load_saved_people() -> Dict[str, List[str]]:
    """
    Load saved people and their strengths from JSON file.
    
    Returns:
        dict: Dictionary with names as keys and list of 5 strengths as values
    """
    if not os.path.exists(DATA_FILE):
        return {}
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading saved people: {e}")
        return {}


def save_person(name: str, strengths: List[str]) -> bool:
    """
    Save a person and their strengths to the data file.
    
    Args:
        name (str): Person's name
        strengths (list): List of 5 CliftonStrengths
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load existing data
        people = load_saved_people()
        
        # Add or update person
        people[name] = strengths
        
        # Save back to file
        with open(DATA_FILE, 'w') as f:
            json.dump(people, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Error saving person: {e}")
        return False


def delete_person(name: str) -> bool:
    """
    Delete a person from saved data.
    
    Args:
        name (str): Person's name to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        people = load_saved_people()
        
        if name in people:
            del people[name]
            
            with open(DATA_FILE, 'w') as f:
                json.dump(people, f, indent=2)
            
            return True
        return False
    except Exception as e:
        print(f"Error deleting person: {e}")
        return False


def get_person_strengths(name: str) -> Optional[List[str]]:
    """
    Get a person's saved strengths.
    
    Args:
        name (str): Person's name
        
    Returns:
        list or None: List of 5 strengths if found, None otherwise
    """
    people = load_saved_people()
    return people.get(name)
