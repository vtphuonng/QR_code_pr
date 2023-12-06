from .test2 import *
# from qr_website.db.db_generator import data_generation
import shutil
import os
import glob
from qr_website.db.To_excel import *

def get_lastest():
    path = r"D:\VTP\python_workspaces\qr_pr\media\profile"

    files = list(filter(os.path.isfile, glob.glob(path + "\*")))

    files.sort(key=os.path.getctime)

    return files[-1]

class qr_processing:
    def __init__(self, excel_path):
        self.path = r'D:\VTP\python_workspaces\qr_pr\media\profile'
        self.excel_path = excel_path
    @staticmethod
    def distributes(values, db, tb1, tb2):
            if values[-1] == True:
                tb_name = tb1

            else:
                tb_name = tb2
            return db, tb_name

    # Gửi danh sách chứa thông tin của các dữ liệu ảnh mới về hàm tương tác với database
    def save_into_db(self, img_folder):
        #path = get_lastest()
        q_list = []
        for imp in img_folder:
            path = self.path + '\\' + str(imp)
            scanned = scan_image(path, self.excel_path)
            if scanned[-1] == True:
                scanned = list(scanned)
                shutil.copy2(scanned[1], str(scanned[1].replace('profile', 'Image_storage')))
                scanned[1] = str(scanned[1].replace('profile', 'Image_storage'))
                q_list.append(scanned)
                print(f'3 {scanned}')
                os.remove(str(scanned[1].replace('Image_storage', 'profile')))

        print('------------------')
        print(self.excel_path)
        ex = save_ex(self.excel_path)
        ex.write_list_to_Excel(q_list, 2, 2)

    # Trả về danh sách thông tin các mã QR mới được nhập
    def get_dir(self):
        get_file = os.listdir(self.path)
        print(get_file)
        return get_file


# m = qr_processing(r'D:\VTP\python_workspaces\qr_pr\media\24-11-2023.xlsx')
# lst = m.get_dir()
# print(lst)
# m.save_into_db(lst)