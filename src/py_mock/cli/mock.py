import json
import os

from py_mock.cli.__main__ import parse_args
from py_mock.mocking.MockData import MockData
from py_mock.specs.Specs import Specs


def main() -> None:
    parser = parse_args()
    try:
        assert parser.file
    except AssertionError:
        raise ValueError("File argument (-f, --file) is required with command specs.")

    specs_path = Specs.get_specs_path()._specs_path
    file = os.path.basename(parser.file)
    file_path = os.path.join(specs_path, file)
    with open(file_path, "r") as f:
        specs = json.load(f)

    path = parser.out_directory

    MockData(specs).generate_data().export(path)


if __name__ == "__main__":
    import sys

    sys.argv = ["pymock", "mock", "-f", "some_specs", "-o", "some_dir"]
    main()
