import re
from typing import Callable, Optional


# Adapted from https://github.com/HHS/ACF-pir-data/blob/dev/src/pir_pipeline/utils/utils.py
def clean_name(name: str, how: str = "snake", func: Optional[Callable] = None) -> str:
    """Convert a name to a new case

    Args:
        name (str): A name to convert
        how (str): What method to use to convert.\n\n\t"snake": Converts to snake case.\n\n\t"title": Converts to title case (can un-snake).

    Returns:
        str: Converted name
    """
    if func:
        new_name = func(name)
    else:
        new_name = name

    if how == "snake":
        new_name = re.sub(r"\W", "_", new_name.lower())
        new_name = re.sub(r"_+", "_", new_name)
    elif how == "title":
        new_name = re.sub(r"_", " ", name)
        new_name = new_name.title()
        new_name = re.sub(r"\bId\b", "ID", new_name)
        if new_name in ["Uqid", "Uid"]:
            new_name = new_name.upper()

    return new_name
