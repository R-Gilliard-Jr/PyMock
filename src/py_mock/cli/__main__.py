import argparse
import inspect
import sys

from py_mock import cli

CLI_MODULES = {
    name: module for name, module in inspect.getmembers(cli, inspect.ismodule)
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        "pymock", description="Command line facilities for mocking tabular data."
    )
    parser.add_argument("command", type=str, help="PyMock command to be run.")
    parser.add_argument("-f", "--file", type=str, help="File.")
    parser.add_argument(
        "-i", "--instructions", type=str, help="Instructions for specs command."
    )
    parser.add_argument(
        "-o", "--out-directory", type=str, help="Directory to write output to."
    )

    return parser.parse_args(sys.argv[1:])


def main():
    parser = parse_args()
    CLI_MODULES[parser.command].main()


if __name__ == "__main__":
    sys.argv = ["pymock", "specs", "-i", "{'id': ['some_column']}"]
    main()
