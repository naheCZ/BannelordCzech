from bannelord_czech.converter import Converter
from bannelord_czech.differ import Differ
from bannelord_czech.cli.arguments_parser import ArgumentsParser, Operation


def main():
    parser = ArgumentsParser()
    parser.parse()

    if parser.operation == Operation.DIFF:
        make_diff(parser.old_version)
    elif parser.operation == Operation.SAVE:
        texts_to_excel()


def make_diff(old_version: str):
    converter = Converter()
    converter.convert()
    folder = converter.czech_folder_location
    differ = Differ(old_version, converter.get_version, folder)
    differ.check_files()


def texts_to_excel():
    pass


if __name__ == '__main__':
    main()
