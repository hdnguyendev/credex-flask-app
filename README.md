# CredEx - Quản lý tài khoản cá nhân

CredEx là một ứng dụng web Flask giúp quản lý thông tin tài khoản cá nhân một cách an toàn và tiện lợi.

## Tính năng

- Đăng ký và đăng nhập tài khoản
- Quản lý thông tin tài khoản (tên, tên đăng nhập, mật khẩu, URL, ghi chú)
- Phân loại tài khoản theo danh mục
- Tìm kiếm và lọc tài khoản
- Chia sẻ tài khoản an toàn với mã PIN và thời hạn
- Mã hóa mật khẩu để bảo vệ thông tin

## Yêu cầu

- Python 3.8 trở lên
- pip (Python package manager)

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/credex-flask.git
cd credex-flask
```

2. Tạo môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt các thư viện:
```bash
pip install -r requirements.txt
```

4. Tạo file .env:
```bash
cp .env.example .env
```

5. Khởi tạo database:
```bash
flask db upgrade
```

## Chạy ứng dụng

1. Kích hoạt môi trường ảo (nếu chưa kích hoạt):
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Chạy ứng dụng:
```bash
flask run
```

3. Truy cập ứng dụng tại http://localhost:5000

## Sử dụng

1. Đăng ký tài khoản mới
2. Đăng nhập vào hệ thống
3. Tạo danh mục để phân loại tài khoản
4. Thêm thông tin tài khoản
5. Chia sẻ tài khoản với người khác

## Bảo mật

- Mật khẩu được mã hóa trước khi lưu vào database
- Sử dụng CSRF token để bảo vệ form
- Cookie được cấu hình với các tùy chọn bảo mật
- Chia sẻ tài khoản yêu cầu mã PIN và có thời hạn (mã hoá đơn giản thôi)
