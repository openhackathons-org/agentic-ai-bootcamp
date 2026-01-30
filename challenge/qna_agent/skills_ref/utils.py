from pathlib import Path
from .models import SkillProperties
from .validator import validate
from .parser import read_properties,read_instruction
def list_skills(skills_dir: Path) -> list[SkillProperties]:
    """List all skills from a single skills directory (internal helper).

    Scans the skills directory for subdirectories containing SKILL.md files,
    parses YAML frontmatter, and returns skill metadata.

    Skills are organized as:
    skills/
    ├── skill-name/
    │   ├── SKILL.md        # Required: instructions with YAML frontmatter
    │   ├── script.py       # Optional: supporting files
    │   └── config.json     # Optional: supporting files

    Args:
        skills_dir: Path to the skills directory.
        source: Source of the skills ('user' or 'project').

    Returns:
        List of skill metadata dictionaries with name, description, path, and source.
    """
    # Check if skills directory exists
    if not skills_dir.exists():
        return []

    skills: list[SkillProperties] = []

    # Iterate through subdirectories
    for skill_dir in skills_dir.iterdir():

        # Validate a skill directory
        problems = validate(skill_dir)
        if problems:
            print("Validation errors:", problems)
        
        props = read_properties(skill_dir)

        # Parse metada
        if props:
            skills.append(props)

    return skills

def load_skill_instruction(skill_dir: Path) -> str:
    """List all skills from a single skills directory (internal helper).

    Scans the skills directory for subdirectories containing SKILL.md files,
    parses YAML frontmatter, and returns skill metadata.

    Skills are organized as:
    skills/
    ├── skill-name/
    │   ├── SKILL.md        # Required: instructions with YAML frontmatter
    │   ├── script.py       # Optional: supporting files
    │   └── config.json     # Optional: supporting files

    Args:
        skills_dir: Path to the skills directory.
        source: Source of the skills ('user' or 'project').

    Returns:
        List of skill metadata dictionaries with name, description, path, and source.
    """
    # Check if skills directory exists
    if not skill_dir.exists():
        return []

    # Validate a skill directory
    problems = validate(skill_dir)
    if problems:
        print("Validation errors:", problems)
    
    instruction = read_instruction(skill_dir)

    return instruction