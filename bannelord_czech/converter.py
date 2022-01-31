import xml.etree.ElementTree as ET
import os
import pathlib
import ntpath
from bannelord_czech.bannelordModules import BannelordModules


class Converter(object):
    def __init__(self, folder: str = 'E:/Bannelord - čeština/'):
        if not folder.endswith('/'):
            folder = f'{folder}/'

        self.czech_folder: str = folder
        self.modules = BannelordModules()

    @property
    def czech_folder_location(self) -> str:
        return self.czech_folder

    @property
    def get_version(self) -> str:
        return self.modules.get_version

    def convert(self):
        language_modules = []

        for module in self.modules.get_modules:
            language_dir = f'{self.modules.get_modules[module]}/ModuleData/Languages'

            if os.path.isdir(language_dir):
                language_modules.append(module)

        for module in language_modules:
            path_to_file = f'{self.modules.get_modules[module]}/ModuleData/Languages'

            for file in os.listdir(path_to_file):
                if file.endswith('.xml'):
                    self.change_language(f'{path_to_file}/{file}', module)

    def change_language(self, file: str, module: str):
        tree = ET.parse(file)
        root = tree.getroot()
        tag: ET.Element = root.find('tags').find('tag')
        tag.set('language', 'Čeština')

        # save to file
        path_for_save = f'{self.czech_folder}{self.modules.get_version}/Modules/{module}/ModuleData/Languages/CZ/'

        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')

        if not os.path.isdir(path_for_save):
            pathlib.Path(path_for_save).mkdir(parents=True, exist_ok=True)

        file_name = ntpath.basename(file)
        tree.write(f'{path_for_save}{file_name}', encoding='utf-8', xml_declaration=True, method='xml')


if __name__ == "__main__":
    converter = Converter()
    converter.convert()
