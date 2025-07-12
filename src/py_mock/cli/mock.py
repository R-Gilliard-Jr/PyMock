from py_mock.cli.__main__ import parse_args
from py_mock.mocking.MockData import MockData


def main() -> None:
    parser = parse_args()
    try:
        assert parser.file
    except AssertionError:
        raise ValueError("File argument (-f, --file) is required with command specs.")

    specs = parser.file
    path = parser.out_directory

    MockData(specs).generate_data.export(path)


if __name__ == "__main__":
    import sys

    sys.argv = ["pymock", "mock", "-f", "some_specs", "-o", "some_dir"]
    main()
