# 🗑️ Ứng Dụng Phân Loại Rác Thải Thông Minh (AI Garbage Classification)

Ứng dụng desktop sử dụng **Deep Learning** để phân loại 12 loại rác thải từ hình ảnh với giao diện hiện đại, thân thiện và độ chính xác cao.

## 📋 Mô Tả Project

Dự án này là một **Đồ Án Tốt Nghiệp (DACN)** xây dựng hệ thống nhận diện rác thải tự động bằng:
- **Model AI**: ResNet50 & VGG16 được fine-tune trên dataset rác thải
- **Framework**: TensorFlow/Keras
- **Giao diện**: CustomTkinter (GUI modern, responsive)
- **Các loại rác nhận diện**: Pin, rác hữu cơ, thủy tinh nâu/xanh/trắng, carton, quần áo, kim loại, giấy, nhựa, giày, rác thường

## 💻 Yêu Cầu Hệ Thống

### Tối thiểu
- **OS**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: 3.9 - 3.11
- **RAM**: 4GB (khuyến nghị 8GB+)
- **GPU**: Tùy chọn (NVIDIA GPU với CUDA tối ưu hóa)
- **Disk**: 3-4GB (model + dependencies)

### Khuyến nghị
- **Python**: 3.10 hoặc 3.11
- **RAM**: 8GB+
- **GPU**: NVIDIA với CUDA 11.8+ (xử lý nhanh hơn 10x)

## 🚀 Hướng Dẫn Cài Đặt (Step-by-Step)

### Bước 1: Chuẩn Bị Môi Trường

**Windows:**
```bash
# Kiểm tra Python đã cài chưa
python --version

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 --version
python3 -m venv venv
source venv/bin/activate
```

### Bước 2: Clone/Tải Source Code
```bash
# Nếu có git
git clone <repository-url>
cd garbage-classification-project-main

# Hoặc tải file ZIP và giải nén
cd garbage-classification-project-main
```

### Bước 3: Cài Đặt Dependencies
```bash
# Nâng cấp pip trước (quan trọng!)
pip install --upgrade pip

# Cài tất cả thư viện từ requirements.txt
pip install -r requirements.txt
```

**⏱️ Lưu ý**: Cài đặt có thể mất 5-15 phút tùy tốc độ internet

### Bước 4: Tải Model
Đảm bảo các file model `.h5` có trong thư mục `models/`:
- `resnet50_garbage_classifier.h5`
- `resnet50_garbage_classifier2.h5`
- `resnet50_garbage_classifier3.h5` (tùy chọn)
- `vgg16_garbage_classifier.h5`

Nếu chưa có, liên hệ để lấy file hoặc tải từ source gốc.

### Bước 5: Chạy Ứng Dụng
```bash
python app.py
```

Giao diện sẽ mở ra trong vòng 3-5 giây.

## 📖 Cách Sử Dụng

1. **Chọn Model** (dropdown bên trái):
   - ResNet50 - Model chính, độ chính xác cao
   - VGG16 - Model khác để so sánh

2. **Tải Hình Ảnh**:
   - Nhấn nút **📸 CHỤP ẢNH** để chụp từ webcam
   - Chọn ảnh từ máy (định dạng: JPG, PNG)

3. **Dự Đoán**:
   - Nhấn **🔍 DỰ ĐOÁN NGAY** để chạy mô hình
   - Chờ 2-5 giây (tùy GPU)

4. **Kết Quả**:
   - Xem emoji + tên loại rác chính
   - Xem % độ chính xác
   - Xem tất cả 12 dự đoán bên phải

5. **Lưu Kết Quả**:
   - Nhấn **💾 LƯU KẾT QUẢ** để lưu vào `saves/`

## 📁 Cấu Trúc Thư Mục

```
garbage-classification-project/
├── app.py                 # Entry point - chạy chương trình
├── labels.py             # Danh sách 12 loại rác
├── requirements.txt      # Dependencies
├── convert_models.py     # Convert model format (nếu cần)
│
├── models/               # Folder chứa .h5 models
│   ├── resnet50_garbage_classifier.h5
│   ├── vgg16_garbage_classifier.h5
│   └── ...
│
├── core/                 # Logic chính
│   ├── model_loader.py   # Load & chạy model
│   ├── history.py        # Quản lý lịch sử
│   └── __init__.py
│
├── ui/                   # Giao diện
│   ├── main_window.py    # Cửa sổ chính
│   ├── components/       # Widget UI
│   │   ├── preview.py    # Hiển thị ảnh
│   │   ├── loading.py    # Animation loading
│   │   └── __init__.py
│   ├── windows/          # Cửa sổ phụ
│   │   ├── history_window.py  # Xem lịch sử
│   │   └── __init__.py
│   └── __init__.py
│
├── utils/                # Utilities
│   ├── camera.py         # Xử lý camera
│   ├── constants.py      # Hằng số, màu sắc
│   ├── helpers.py        # Hàm phụ trợ
│   └── __init__.py
│
├── saves/                # Lưu kết quả
│   ├── history.json      # Lịch sử dự đoán
│   └── ketqua_*.txt      # Kết quả chi tiết
│
└── README.md             # File này
```

## 🔧 Troubleshooting

| Lỗi | Giải Pháp |
|-----|---------|
| **ModuleNotFoundError: No module named 'tensorflow'** | Chạy `pip install -r requirements.txt` lại |
| **Camera không hoạt động** | Kiểm tra camera permission, try USB camera |
| **Model loading quá chậm** | Bình thường lần đầu, lần sau sẽ cache |
| **Memory Error** | Đóng các ứng dụng khác, nâng cấp RAM hoặc dùng GPU |
| **Kết quả không chính xác** | Ảnh phải rõ, ánh sáng tốt, góc chụp hợp lý |

## 📊 Tính Năng

✅ **12 loại rác** được phân loại  
✅ **2 mô hình** để lựa chọn (ResNet50, VGG16)  
✅ **Webcam & File** input  
✅ **Lịch sử** dự đoán  
✅ **Giao diện** hiện đại, responsive  
✅ **Fullscreen mode**  
✅ **Export kết quả**  

## 👥 Thông Tin

- **Loại**: Đồ Án Tốt Nghiệp (DACN)
- **Ngôn ngữ**: Python 3.10+
- **Framework**: TensorFlow 2.17, CustomTkinter 5.2
- **Ngày tạo**: 2026

## 📝 License

Dự án này được sử dụng cho mục đích học tập và nghiên cứu.

---

**💡 Tip**: Chụp ảnh trong ánh sáng tốt và góc 45° sẽ cho kết quả tốt nhất!