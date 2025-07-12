from py_mock.cli.__main__ import parse_args
from py_mock.specs.Specs import Specs


def main() -> None:
    parser = parse_args()
    try:
        assert parser.file
    except AssertionError:
        raise ValueError("File argument (-f, --file) is required with command specs.")

    path = parser.file
    instructions = parser.instructions

    Specs(path, instructions).extract_column_metadata().export()


if __name__ == "__main__":
    import sys

    sys.argv = ["pymock", "specs", "-f", "some_file"]
    main()
