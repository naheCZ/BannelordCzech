import os
import xml.etree.ElementTree as ET
from typing import Dict, Optional


class BannelordModules(object):
    def __init__(self, folder: Optional[str] = None):
        self._folder: str = 'E:/Hry/steamapps/common/Mount & Blade II Bannerlord/Modules/'

        if folder is not None:
            if not folder.endswith('/'):
                folder = f'{folder}/'

            self._folder = folder

        self._modules: Dict[str, str] = self.load_modules()
        self._version: str = self.load_version()

    def load_modules(self) -> Dict[str, str]:
        modules = {}

        for module_folder in os.listdir(self._folder):
            module = f'{self._folder}{module_folder}'

            if os.path.isdir(module):
                modules[module_folder] = module

        return modules

    def load_version(self) -> str:
        version = 'e0.0.0'

        for module in self._modules:
            sub_module = f'{self._modules[module]}/SubModule.xml'

            if os.path.isfile(sub_module):
                tree = ET.parse(sub_module)
                root: ET.ElementTree = tree.getroot()
                module_version: str = root.find('Version').get('value')

                if module_version > version:
                    version = module_version

        return version

    @property
    def get_modules(self):
        return self._modules

    @property
    def get_version(self):
        return self._version
