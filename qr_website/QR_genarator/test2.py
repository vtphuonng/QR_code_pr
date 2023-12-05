import os
import cv2

from openpyxl import Workbook
from qr_website.db.To_excel import save_ex
from qr_website.db.files_manager import *
from qr_website.db.sheet_management import *

def scan_image(cin_img, path):
    try:
        img = cv2.imread(cin_img)
        qcd = cv2.QRCodeDetector()
        # Initialize the Excel workbook and worksheet
        wb = Workbook()
        ws = wb.active

        # Read a frame from the camera
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)
        decoded_objects = list(decoded_info)

        # If a QR code is detected, save the result to the Excel file and return the file path
        if len(decoded_objects) == 0:
            return 'Cannot read qr code', cin_img, False
        else:
            qr_code_result = decoded_objects[0]
            return qr_code_result, cin_img, retval


    except Exception as e:
        return e, cin_img, False


def get_from_vid(excel_path):
    camera_id = 0
    delay = 5
    window_name = 'OpenCV QR Code'

    qcd = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(camera_id)
    exited_count = os.listdir('D:\VTP\python_workspaces\qr_pr\qr_website\QR_genarator\image')
    img_counter = len(exited_count)
    m = save_ex(excel_path)
    lst2 = []
    while True:
        ret, frame = cap.read()

        if ret:
            ret_qr, decoded_info, points, _ = qcd.detectAndDecodeMulti(frame)
            decoded_objects = list(decoded_info)

            if ret_qr:
                for s, p in zip(decoded_info, points):
                    if s:
                        print(s)
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                    frame = cv2.polylines(frame, [p.astype(int)], True, color, 8)
            # cv2.imshow(window_name, frame)
            imgencode = cv2.imencode('.jpg', frame)[1]
            stringData = imgencode.tostring()
            yield (b'--frame\r\n'
                   b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')
            print(decoded_info)

            if len(decoded_info) != 0:
                print(decoded_objects[0] + 'rrrrrrrrrrrrrrrrrrrrrrrrrr')
                if decoded_objects[0]:
                    img_name = "opencv_frame_{}.jpg".format(img_counter)
                    save_path = f'D:\VTP\python_workspaces\qr_pr\qr_website\QR_genarator\image\{img_name}'
                    cv2.imwrite(save_path, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1
                    lst2.append([decoded_objects[0], save_path, True])
                    lst3 = [lst for lst in lst2 if len(lst) != 0]
                    m.write_list_to_Excel(lst3, 2, 2, True)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

    # cv2.destroyWindow(window_name)

# get_from_vid()
