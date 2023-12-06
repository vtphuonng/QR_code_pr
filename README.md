# Trang web quản lý mã QR
## Mục tiêu: Tạo một trang web hỗ trợ lưu trữ, quản lý thông tin mã QR

## Tính năng
### 1. Thêm dữ liệu
Người dùng có thể chọn file excel để lưu trữ dữ liệu upload mã QR bằng 2 phương thức: upload file ảnh hoặc quét mã bằng camera
### 2. Hiển thị danh sách dữ liệu:
Danh sách các file excel dữ liệu, dữ liệu của từng file được hiển thị trên giao diện giúp người dùng thuận lợi trong việc quản lý file excel và dữ liệu
### ... Các tính năng khác sẽ được update dần

## Hướng dẫn cài đặt
mở bash hoặc terminal trong folder mới
1. Clone dự án từ repository:
2. Cài đặt dependencies: pip install -r requirement.txt
3. Sửa đường dẫn file:
   - Trong file qr_website/QR_genarator/QR_generator.py thay đổi câu lệnh:
      - self.path = r'path\to\project\qr_pr\media\profile'
   - Trong file qr_website/QR_genarator/test2.py thay đổi câu lệnh:
      - exited_count = os.listdir('path\to\project\qr_pr\qr_website\QR_genarator\image')
      - save_path = f'path\to\project\qr_pr\qr_website\QR_genarator\image\{img_name}'
   - Trong file qr_website/db/files_manager.py thay đổi câu lệnh:
      - self.excelPath = r'path\to\project\qr_pr\qr_website\db\excels'
5. Khởi động trang web: python/python3 manage.py runserver (trang web sẽ deploy ở địa chỉ IP: http://127.0.0.1:8000)

## Tình trạng dự án:
đang phát triển



