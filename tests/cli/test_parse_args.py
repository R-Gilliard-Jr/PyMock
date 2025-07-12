import inspect
import sys

from py_mock import cli
from py_mock.cli.__main__ import parse_args

CLI_MODULES = {
    name: module for name, module in inspect.getmembers(cli, inspect.ismodule)
}


def test_parse_args():
    sys.argv = ["pymock", "init"]
    parser = parse_args()
    command = parser.command
    module = CLI_MODULES[command].__name__
    assert command == "init", f"Incorrect command {command}"
    assert module == "py_mock.cli.init", f"Incorrect module {module}"

    sys.argv = ["pymock", "specs", "-f", "some_file", "-i", "some_instructions"]
    parser = parse_args()
    command = parser.command
    file = parser.file
    instructions = parser.instructions
    module = CLI_MODULES[command].__name__
    assert command == "specs", f"Incorrect command {command}"
    assert file == "some_file", f"Incorrect file {file}"
    assert instructions == "some_instructions", f"Incorrect instructions {instructions}"
    assert module == "py_mock.cli.specs", f"Incorrect module {module}"

    sys.argv = ["pymock", "mock", "-f", "some_file", "-o", "some_dir"]
    parser = parse_args()
    command = parser.command
    module = module = CLI_MODULES[command].__name__
    assert module == "py_mock.cli.mock", f"Incorrect module {module}"
