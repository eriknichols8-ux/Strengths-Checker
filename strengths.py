"""
CliftonStrengths module containing all 34 strength themes.
"""

# All 34 CliftonStrengths themes in alphabetical order
CLIFTON_STRENGTHS = [
    "Achiever",
    "Activator",
    "Adaptability",
    "Analytical",
    "Arranger",
    "Belief",
    "Command",
    "Communication",
    "Competition",
    "Connectedness",
    "Consistency",
    "Context",
    "Deliberative",
    "Developer",
    "Discipline",
    "Empathy",
    "Focus",
    "Futuristic",
    "Harmony",
    "Ideation",
    "Includer",
    "Individualization",
    "Input",
    "Intellection",
    "Learner",
    "Maximizer",
    "Positivity",
    "Relator",
    "Responsibility",
    "Restorative",
    "Self-Assurance",
    "Significance",
    "Strategic",
    "Woo"
]


def validate_strengths(strengths):
    """
    Validate that all strengths are from the official CliftonStrengths list.
    
    Args:
        strengths (list): List of strength names to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not strengths or len(strengths) != 5:
        return False, "Please select exactly 5 strengths."
    
    # Check for empty selections
    if any(not s or s == "Select a strength..." for s in strengths):
        return False, "Please select all 5 strengths."
    
    # Check for duplicates
    if len(strengths) != len(set(strengths)):
        return False, "Please select 5 different strengths (no duplicates)."
    
    # Check if all are valid CliftonStrengths
    invalid = [s for s in strengths if s not in CLIFTON_STRENGTHS]
    if invalid:
        return False, f"Invalid strength(s): {', '.join(invalid)}"
    
    return True, ""


def format_strengths_list(strengths):
    """
    Format a list of strengths as a comma-separated string.
    
    Args:
        strengths (list): List of strength names
        
    Returns:
        str: Formatted string of strengths
    """
    return ", ".join(strengths)
