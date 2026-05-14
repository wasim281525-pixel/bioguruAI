import re
from pathlib import Path


def extract_metadata_from_filename(filepath: str) -> dict:
    """Extract chapter number, class, and source from a filename."""
    name = Path(filepath).stem
    metadata = {"source": "NCERT", "class": "11", "chapter": name}

    # Detect class level from path
    if "class12" in filepath or "class_12" in filepath:
        metadata["class"] = "12"
    elif "class11" in filepath or "class_11" in filepath:
        metadata["class"] = "11"

    # Try to extract chapter number
    match = re.search(r"ch(?:apter)?[-_]?(\d+)", name, re.IGNORECASE)
    if match:
        metadata["chapter_num"] = int(match.group(1))

    metadata["source"] = f"NCERT Class {metadata['class']}"
    return metadata
