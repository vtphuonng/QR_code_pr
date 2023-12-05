from .sheet_management import *


class save_ex:
    def __init__(self, path):
        self.path = path

    # Tìm, tương tác với file excel và lưu dữ liệu vào file excel đó
    def write_list_to_Excel(self, lst, start_row, start_col, method=False):
        path_infor = self.getSheetPath(self.path)
        workbook = load_workbook(self.path)
        sheet = workbook[path_infor]
        print('forrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        print(sheet)
        check_emty = self.checkEmpty(lst)
        if check_emty == True:
            return 'QR not received'
        # sheet.insert_rows(2, len(lst))
        for y in range(len(lst)):
            check = self.check_dup(self.path, path_infor, lst[y][0])
            if check == False:
                sheet.insert_rows(2, 1)
                for x in range(len(lst[y])):
                    sheet.cell(row=start_row + y,
                               column=start_col + x,
                               value=lst[y][x])
            else:
                pass
            workbook.save(self.path)
        workbook.close()
        return 'saved'
        # for y, row in enumerate(list_2d):
        #    print(y)
        #    print(row)
        #    for x, cell in enumerate(row):
        #        sheet.cell(row=start_row + y,
        #                   column=start_col + x,
        #                   value=list_2d[y][x])

        # workbook.close()
        # return 'Excel saved'

    # def createFile(self):
    #     df = pd.read_excel(self.path)
    #     list_data = []
    #     for index in range(len(df)):
    #         row_list = df.loc[index, ['Description', 'path', 'flag']].values.flatten().tolist()
    #         list_data.append(row_list)
    #     return list_data

    # kiểm tra xem dữ liệu mới đã xuất hiện trong file excel chưa
    def get_dup(self, origin_path, target_sheet, check_val):
        workbook = load_workbook(origin_path)
        sheet = pd.read_excel(origin_path, target_sheet)
        print('sheetsheetsheetsheetsheetsheet')
        print(sheet)
        for i in sheet['Description']:
            if check_val == i:
                workbook.close()
                return True
        workbook.close()
        return False

    # lấy đường dẫn đến file excel
    @staticmethod
    def getSheetPath(excel_path):
        s = sheetGenerator(excel_path)
        return s.getSheetPath()[-1]

    @staticmethod
    def check_dup(origin_path, target_sheet, check_val):
        workbook = load_workbook(origin_path)
        sheet = pd.read_excel(origin_path, target_sheet)
        print('sheetsheetsheetsheetsheetsheet')
        print(sheet)
        for i in sheet['Description']:
            if check_val == i:
                workbook.close()
                return True
        workbook.close()
        return False

    @staticmethod
    def checkEmpty(lst):
        if len(lst) == 0:
            return True
        return False

# s = save_ex(r'D:\\VTP\\python_workspaces\\qr_pr\\media\\24-11-2023.xlsx')
# print(s.get_dup('https://www.exceldemy.com'))
