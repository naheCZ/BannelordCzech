import argparse
from typing import Optional, NoReturn
from enum import Enum, unique, auto


@unique
class Operation(Enum):
    DIFF = auto(),
    SAVE = auto()


class ArgumentsParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        self._args: Optional[argparse.Namespace] = None
        self._operation = None

        self._parser.add_argument('--diff', action='store_true', dest='diff', help='Make diff between two versions')
        self._parser.add_argument('--save', action='store_true', dest='save', help='Save all text to excel file')
        self._parser.add_argument('--old', action='store', dest='old_version', type=str, help='Old version for diff')

    @property
    def old_version(self) -> str:
        return self._args.old_version

    @property
    def operation(self) -> Operation:
        return self._operation

    def parse(self) -> NoReturn:
        """
        Parse arguments and store them to object variable.
        :return: None
        """
        self._args = self._parser.parse_args()
        self.set_operation()

    def set_operation(self) -> NoReturn:
        if self._args.diff and self.check_diff():
            self._operation = Operation.DIFF
        elif self._args.save:
            self._operation = Operation.SAVE
        else:
            self.print_help()
            raise CommandLineArgumentsError()

    def check_diff(self) -> bool:
        return self._args.old_version is not None

    def print_help(self):
        self._parser.print_help()


class CommandLineArgumentsError(Exception):
    def __init__(self):
        super().__init__("Error in command line arguments")
