import os
import xml.etree.ElementTree as ET
from bannelord_czech.bannelordModules import BannelordModules
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class Differ(object):
    def __init__(self, old_version, new_version, folder):
        self._old_version = old_version
        self._new_version = new_version

        self._old_modules = BannelordModules(folder=f'{folder}{self._old_version}/Modules')
        self._new_modules = BannelordModules(folder=f'{folder}{self._new_version}/Modules')

    def check_files(self):
        work_book = Workbook()

        for module in self._new_modules.get_modules:
            path_to_file = f'{self._new_modules.get_modules[module]}/ModuleData/Languages/CZ'

            current_sheet = work_book.active
            current_sheet.title = module
            current_sheet['A1'] = 'File'
            current_sheet['B1'] = 'String ID'
            current_sheet['C1'] = 'Old text'
            current_sheet['D1'] = 'New text'
            num = 2

            for file in os.listdir(path_to_file):
                if file.endswith('.xml'):
                    new_tree = ET.parse(f'{path_to_file}/{file}')
                    new_root = new_tree.getroot()

                    if module in self._old_modules.get_modules:
                        path_to_old_file = f'{self._old_modules.get_modules[module]}/ModuleData/Languages/CZ'

                        if os.path.isfile(f'{path_to_old_file}/{file}'):
                            old_tree = ET.parse(f'{path_to_old_file}/{file}')
                            old_root = old_tree.getroot()

                            if not new_root.find('strings'):
                                continue

                            for string in new_root.find('strings').iter('string'):
                                old_string = old_root.find('strings').find(f"string[@id='{string.get('id')}']")
                                if old_string is None:
                                    self.fill_rows(string, file, current_sheet, num)
                                    num += 1
                                elif string.get('text') != old_string.get('text'):
                                    self.fill_rows(string, file, current_sheet, num)
                                    current_sheet[f'C{num}'] = old_string.get('text')
                                    num += 1
                        else:
                            try:
                                for string in new_root.find('strings').iter('string'):
                                    self.fill_rows(string, file, current_sheet, num)
                                    num += 1
                            except AttributeError:
                                print(f'File: {path_to_file}/{file} has not have strings')
                    else:
                        try:
                            for string in new_root.find('strings').iter('string'):
                                self.fill_rows(string, file, current_sheet, num)
                                num += 1
                        except AttributeError:
                            print(f'File: {path_to_file}/{file} has not have strings')

            new_sheet = work_book.create_sheet()
            work_book.active = new_sheet

        work_book.remove(work_book.active)  # Empty one created at the end of the cycle
        work_book.save(f'{self._old_version} to {self._new_version} .xlsx')

    @staticmethod
    def fill_rows(string: ET.Element, file: str, sheet: Worksheet, num: int):
        sheet[f'A{num}'] = file
        sheet[f'B{num}'] = string.get('id')
        sheet[f'D{num}'] = string.get('text')
