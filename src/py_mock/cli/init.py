import json
import os
import re
import sys


def main() -> None:
    if sys.prefix != sys.base_prefix:
        recommended = os.path.dirname(sys.prefix)

    else:
        recommended = ""

    user_choice = input(f"Where would you like specs to be stored? [{recommended}]: ")

    specs_parent = user_choice or recommended
    specs_dir = os.path.join(specs_parent, ".pymock")
    os.mkdir(specs_dir)

    files = os.listdir(specs_parent)
    if ".gitignore" in files:
        add_to_gitignore = 0
        user_add_to_gitignore = input("Add pymock to .gitignore? [yN]: ")
        if re.match(r"y(es)?", user_add_to_gitignore, flags=re.IGNORECASE):
            add_to_gitignore = 1

        if add_to_gitignore:
            gitignore = os.path.join(specs_parent, ".gitignore")
            with open(gitignore, "a") as f:
                f.write("\n")
                f.write("""# PyMock\n.pymock\n""")

    current_dir = os.path.dirname(__file__)
    py_mock_specs_dir = os.path.join(current_dir, "..", "config")
    paths_file = os.path.join(py_mock_specs_dir, "paths.json")
    specs_path_dict = {"specs_path": specs_dir}

    if os.path.exists(paths_file):
        with open(paths_file, "r") as f:
            path_dict = json.load(f)
            path_dict.update(specs_path_dict)
    else:
        path_dict = specs_path_dict

    with open(paths_file, "w") as f:
        json.dump(path_dict, f, indent=4)
