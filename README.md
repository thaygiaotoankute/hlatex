# H_Latex Web

Phiên bản Web của phần mềm H_Latex - Công cụ hỗ trợ tạo mã LaTeX cho biểu đồ, bảng biến thiên, đồ thị, và các công cụ toán học khác.

## Tính năng

- **Chuyển đổi dữ liệu**: Chuyển đổi văn bản sang định dạng LaTeX với nhiều tùy chọn (ex, bt, vd, ...)
- **Bảng biến thiên**: Tạo bảng biến thiên tự động và thủ công
- **Đồ thị hàm số**: Vẽ đồ thị các hàm số thông dụng và tùy chỉnh
- **Hình không gian**: Tạo mã LaTeX cho các mẫu hình không gian
- **API**: Tích hợp các chức năng qua REST API

## Yêu cầu hệ thống

- Python 3.7 trở lên
- Các gói LaTeX: texlive-latex-base, texlive-fonts-recommended, texlive-lang-vietnamese, texlive-latex-extra, texlive-science
- Các thư viện Python được liệt kê trong file `requirements.txt`

## Cài đặt

### Cài đặt thủ công

```bash
# Clone repository
git clone https://github.com/yourusername/HLatex-Web.git
cd HLatex-Web

# Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate  # Trên Linux/Mac
venv\Scripts\activate  # Trên Windows

# Cài đặt các gói phụ thuộc
pip install -r requirements.txt

# Cấu hình biến môi trường
export SECRET_KEY="your_secret_key"  # Trên Linux/Mac
set SECRET_KEY="your_secret_key"  # Trên Windows

# Chạy ứng dụng
python app.py
```

### Cài đặt bằng Docker

```bash
# Build image
docker build -t hlatex-web .

# Chạy container
docker run -p 5000:5000 -e SECRET_KEY="your_secret_key" -d hlatex-web
```

## Sử dụng

### Chuyển đổi dữ liệu

1. Truy cập trang "Chuyển đổi dữ liệu"
2. Chọn loại chuyển đổi (ex, extf, bt, vd)
3. Dán nội dung cần chuyển đổi
4. Nhấn nút "Chuyển đổi"
5. Sao chép kết quả

### Tạo bảng biến thiên

1. Truy cập trang "Bảng biến thiên"
2. Chọn loại hàm số và nhập các tham số
3. Nhấn nút "Xuất code"
4. Sao chép mã LaTeX hoặc render thành PDF

### Vẽ đồ thị hàm số

1. Truy cập trang "Đồ thị"
2. Chọn loại hàm số hoặc nhập hàm tùy chỉnh
3. Thiết lập các tham số đồ thị
4. Nhấn nút "Xuất code"
5. Sao chép mã TikZ hoặc render thành PDF

### Tạo hình không gian

1. Truy cập trang "Hình không gian"
2. Chọn loại hình (tứ diện, hình chóp, lăng trụ, ...)
3. Nhập các tham số và nhãn điểm
4. Nhấn nút "Xuất code"
5. Sao chép mã TikZ hoặc render thành PDF

## API Documentation

### Kiểm tra giấy phép

```
GET /api/check-license
```

**Tham số:**
- `license_code` (tùy chọn): Mã giấy phép cần kiểm tra

**Response:**
```json
{
  "is_registered": true,
  "system_info": "..."
}
```

### Chuyển đổi dữ liệu

```
POST /api/convert
```

**Body:**
```json
{
  "text": "f(x) = x^2 + 2x + 1",
  "type": "ex"
}
```

**Response:**
```json
{
  "result": "\\begin{ex}f(x) = x^2 + 2x + 1\\end{ex}"
}
```

### Bảng biến thiên

```
POST /api/bbt
```

**Body:**
```json
{
  "function": "x^2 - 4",
  "domain": "[-3, 3]"
}
```

### Đồ thị hàm số

```
POST /api/graph
```

**Body:**
```json
{
  "function": "sin",
  "params": {
    "xmin": -5,
    "xmax": 5
  }
}
```

## Triển khai

Xem tài liệu [DEPLOYMENT.md](./DEPLOYMENT.md) để biết chi tiết về cách triển khai ứng dụng lên các nền tảng khác nhau.

## Đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/amazing-feature`)
3. Commit thay đổi (`git commit -m 'Add some amazing feature'`)
4. Push lên branch (`git push origin feature/amazing-feature`)
5. Mở Pull Request

## Giấy phép

Phân phối theo giấy phép [GPL-3.0](./LICENSE).

## Liên hệ

- Email: info@hlatex.com
- GitHub: https://github.com/PhucRua/HLatex
