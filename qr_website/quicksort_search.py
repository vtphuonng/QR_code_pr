def to_list(search_by_name_records):
            all = []
            for b in search_by_name_records:
                all.append(b)
            return all


# def quick_select_by_title(cin, target):
#         final = []
#         if len(cin) > 1:
#             picked = cin[-1]
#             if f'{target}' in picked.title :
#                 final.append(picked)
#             elif f'{target}' in picked.book_id:
#                 final.append(picked)
#             elif f'{target}' in picked.borower_name:
#                 final.append(picked)
#             elif f'{target}' in picked.borrow_day:
#                 final.append(picked)
#             elif f'{target}' in picked.author:
#                 final.append(picked)
#
#             mid_index = len(cin)//2
#             temp = picked
#             cin[-1] = cin[mid_index]
#             cin[mid_index] = temp
#             left = []
#             right = []
#             for i in range(0,mid_index):
#                 left.append(cin[i])
#             for i in range(mid_index,len(cin)):
#                 right.append(cin[i])
#
#             return quick_select_by_title(left,target) + quick_select_by_title(right,target)
#         else:
#             try:
#                 if cin[0].title in target:
#                     final.append(cin[0])
#                 elif f'{target}' in cin[0].book_id:
#                     final.append(cin[0])
#                 elif f'{target}' in cin[0].borower_name:
#                     final.append(cin[0])
#                 elif f'{target}' in cin[0].borrow_day:
#                     final.append(cin[0])
#                 elif f'{target}' in cin[0].author:
#                     final.append(cin[0])
#             except Exception as e:
#                 pass
#         return final


def quick_select_by_id(cin, target):
        final = []
        if len(cin) > 1:
            picked = cin[-1]
            print(picked.excel_id)
            print(type(picked.excel_id))
            print(target)
            if picked.excel_id == f'{target}':
                final.append(picked)    
            
            mid_index = len(cin)//2
            temp = picked
            cin[-1] = cin[mid_index]
            cin[mid_index] = temp
            left = []
            right = []
            for i in range(0, mid_index):
                left.append(cin[i])
            for i in range(mid_index, len(cin)):
                right.append(cin[i])

            return quick_select_by_id(left, target) + quick_select_by_id(right, target)
        else:
            try:
                if cin[0].excel_id == f'{target}':
                    final.append(cin[0])
            except Exception as e:
                pass
        return final