import os
import pandas as pd
from datetime import date
import datetime
class files_generator:
    def __init__(self):
        self.excelPath = r'D:\VTP\python_workspaces\qr_pr\qr_website\db\excels'

    def createFiles(self, files_list):
        valid_infor = self.checkTodayExisted(files_list)
        file_name = valid_infor[-1]
        if valid_infor[0] != False:
            return f'{self.excelPath}\\{file_name}.xlsx'
        df = pd.DataFrame([[0, 0, 0]], columns=['Description', 'path', 'flag'])
        df.to_excel(f'{self.excelPath}\\{file_name}.xlsx')
        return f'{self.excelPath}\\{file_name}.xlsx'
    def getFiles(self):
        files_sys = os.listdir(self.excelPath)
        files_list = []
        for file in files_sys:
            row = []
            if file.endswith('.xlsx'):
                target_path = f'{self.excelPath}\\{file}'
                create_time = os.path.getctime(target_path)
                last_modified = os.path.getctime(target_path)
                create_date = datetime.datetime.fromtimestamp(create_time).strftime('%d-%m-%Y %H:%M:%S')
                last_modified_date = datetime.datetime.fromtimestamp(last_modified).strftime('%d-%m-%Y %H:%M:%S')
                # row = [file, target_path, create_date, last_modified_date]
                if file != 'No Record':
                    row.append(file)
                    row.append(target_path)
                    row.append(create_date)
                    row.append(last_modified_date)
            else:
                row = [['No Record'],['No Record'],['No Record'],['No Record']]
            if len(row) != 0:
                files_list.append(row)
        # return [[filename, filepath], ...]
        return files_list

    @staticmethod
    def checkTodayExisted(files_list):
        today = date.today()
        today_str = today.strftime("%Y")
        file_str = today_str + '.xlsx'
        for file_infor in files_list:
            if file_str == file_infor[0]:
                return True, today_str
        return False, today_str
#
# f = files_generator()
# # print(f.getFiles())
# lst = f.getFiles()
# print(lst)
# create = f.createFiles(lst)
# print(create)

# file = files_generator()
# file_lst = file.getFiles()
# print(file_lst)