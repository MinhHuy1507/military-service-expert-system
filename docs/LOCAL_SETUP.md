# Hướng dẫn Cài đặt & Chạy Thủ công (Local Development)

Tài liệu này hướng dẫn chi tiết cách cài đặt và chạy hệ thống trên môi trường local, phù hợp cho mục đích phát triển (development) và gỡ lỗi (debugging).

## Yêu cầu hệ thống

- **Python:** 3.8 trở lên
- **Git**
- **Terminal:** PowerShell (Windows) hoặc Bash (macOS/Linux)

---

## Quy trình cài đặt

### Bước 0: Clone Repository

```powershell
# Clone repository về máy
git clone https://github.com/MinhHuy1507/military-service-expert-system
cd military-service-expert-system
```

### Bước 1: Cài đặt Backend

```powershell
# Di chuyển vào thư mục backend
cd backend

# Tạo môi trường ảo
python -m venv backend_venv

# Kích hoạt môi trường (Windows)
.\backend_venv\Scripts\activate

# Kích hoạt môi trường (macOS/Linux)
# source backend_venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy server với hot-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend sẽ chạy tại: `http://localhost:8000`

### Bước 2: Cài đặt Frontend

Mở **terminal mới** từ thư mục gốc `military-service-expert-system`:

```powershell
# Di chuyển vào thư mục frontend
cd frontend

# Tạo môi trường ảo
python -m venv frontend_venv

# Kích hoạt môi trường (Windows)
.\frontend_venv\Scripts\activate

# Kích hoạt môi trường (macOS/Linux)
# source frontend_venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy Streamlit app
streamlit run app.py
```

✅ Frontend sẽ tự động mở tại: `http://localhost:8501`

---

## Gỡ lỗi thường gặp (Troubleshooting)

### Lỗi không tìm thấy module
Đảm bảo bạn đã kích hoạt môi trường ảo (`backend_venv` hoặc `frontend_venv`) trước khi chạy lệnh `pip install` hoặc chạy ứng dụng.

### Lỗi Port already in use
Nếu port 8000 hoặc 8501 đang bị chiếm dụng, hãy tắt tiến trình đang chạy hoặc đổi port trong lệnh chạy:
- Backend: `uvicorn main:app --port 8001`
- Frontend: `streamlit run app.py --server.port 8502`
