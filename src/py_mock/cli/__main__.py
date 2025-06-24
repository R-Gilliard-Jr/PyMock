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

    return parser.parse_args(sys.argv[1:])


def main():
    parser = parse_args()
    CLI_MODULES[parser.command].main()


if __name__ == "__main__":
    sys.argv = ["pymock", "init"]
    main()
