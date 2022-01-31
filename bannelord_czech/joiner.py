import os
from bannelord_czech.bannelordModules import BannelordModules
from openpyxl import Workbook
import xml.etree.ElementTree as ET


class Joiner(object):
    def __init__(self):
        self.modules = BannelordModules(folder='E:/Bannelord - čeština/e1.5.8/Modules')

    def join(self):
        work_book = Workbook()

        for module in self.modules.get_modules:
            path_to_file = f'{self.modules.get_modules[module]}/ModuleData/Languages/CZ'

            current_sheet = work_book.active
            current_sheet.title = module
            current_sheet['A1'] = 'File'
            current_sheet['B1'] = 'String ID'
            current_sheet['C1'] = 'content'
            num = 2

            for file in os.listdir(path_to_file):
                if file.endswith('.xml'):
                    tree = ET.parse(f'{path_to_file}/{file}')
                    root = tree.getroot()
                    strings = root.find('strings')

                    if strings is not None:
                        for string in strings.iter('string'):
                            current_sheet[f'A{num}'] = file
                            current_sheet[f'B{num}'] = string.get('id')
                            current_sheet[f'C{num}'] = string.get('text')
                            num += 1

            new_sheet = work_book.create_sheet()
            work_book.active = new_sheet

        work_book.save('test.xlsx')


if __name__ == '__main__':
    joiner = Joiner()
    joiner.join()
