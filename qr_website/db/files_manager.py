import os
import pandas as pd
from datetime import date
import datetime
from pathlib import Path
class files_generator:
    def __init__(self):
        self.excelPath = r'D:\VTP\python_workspaces\qr_pr\qr_website\db\excels'
    # Tạo file mới và trả về tên file mới được tạo, đường dẫn đến vị trí file
    def createFiles(self, file_name):
        valid_infor = self.checkExisted(file_name, self.excelPath)
        if valid_infor[0] != False:
            return True, f'{self.excelPath}\\{file_name}.xlsx'
        df = pd.DataFrame([[0, 0, 0]], columns=['Description', 'path', 'flag'])
        df.to_excel(f'{self.excelPath}\\{file_name}.xlsx')
        return False, f'{self.excelPath}\\{file_name}.xlsx'
    
    # Lấy danh sách các file excel hiện có trong hệ thống
    def getFiles(self):
        files_sys = os.listdir(self.excelPath)
        files_list = []
        for file in files_sys:
            row = []
            if file.endswith('.xlsx'):
                target_path = f'{self.excelPath}\\{file}'
                create_time = os.path.getctime(target_path)
                last_modified = os.path.getmtime(target_path)
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
    # kiểm tra xem file được gọi đã xuất hiện chưa
    @staticmethod
    def checkTodayExisted(files_list):
        today = date.today()
        today_str = today.strftime("%Y")
        file_str = today_str + '.xlsx'
        for file_infor in files_list:
            if file_str == file_infor[0]:
                return True, today_str
        return False, today_str

    @staticmethod
    def checkExisted(file_name, excel_path):
        existed_file = os.listdir(excel_path)
        target = file_name+'.xlsx'
        for file_infor in existed_file:
            if target in file_infor:
                return True, target
        return False, target

    def deleteFile(self, file_path):
        recycle_path = str(file_path).replace('excels', 'recycleBin')
        os.replace(file_path, recycle_path)
        return 'File Deleted'

    def recoveryFile(self, recycle_path):
        recover_path = str(recycle_path).replace('recycleBin', 'excels')
        os.replace(recycle_path, recover_path)
        return 'File Recovered'

class recycleManage(files_generator):
    def getDummy(self):
        try:
            recycle_path = str(self.excelPath).replace('excels', 'recycleBin')
            print('f1'+recycle_path)
            dum_list = os.listdir(rf'{recycle_path}')
            lst = []
            if dum_list == 0:
                return lst
            for dum in dum_list:
                row = []
                dum_name = dum
                dum_path = f"{recycle_path}\\{dum}"
                deleted_time = os.path.getmtime(f'{recycle_path}')
                create_time = os.path.getctime(f'{dum_path}')
                print('F2'+str(create_time))
                create_date = datetime.datetime.fromtimestamp(create_time).strftime('%d-%m-%Y %H:%M:%S')
                delete_date = datetime.datetime.fromtimestamp(deleted_time).strftime('%d-%m-%Y %H:%M:%S')
                row.append(dum_name)
                row.append(dum_path)
                row.append(create_date)
                row.append(delete_date)
                lst.append(row)
            return lst
        except Exception as e:
            print(e)
            return []

    def removeFile(self):
        recycle_path = str(self.excelPath).replace('excels', 'recycleBin')
        os.remove(recycle_path)
        return 'File Is Abandoned From Recycle Bin'
# f = files_generator()
# # print(f.getFiles())
# lst = f.getFiles()
# print(lst)
# create = f.createFiles(lst)
# print(create)

# file = files_generator()
# file_lst = file.getFiles()
# print(file_lst)