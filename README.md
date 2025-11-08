# Hệ Chuyên Gia Hỗ Trợ Tuyển Chọn và Tư Vấn Nghĩa Vụ Quân Sự

## Tổng quan

Hệ thống sử dụng kỹ thuật suy diễn tiến (Forward Chaining) để tư vấn tình trạng nghĩa vụ quân sự dựa trên các quy định pháp luật hiện hành.

### Công nghệ sử dụng
- **Backend**: FastAPI (Python)
- **Frontend**: Streamlit (Python)
- **Logic Engine**: Forward Chaining Inference Engine
- **Containerization**: Docker & Docker Compose

## Hướng dẫn Cài đặt và Chạy

### Phương án 1: Sử dụng Docker

**Yêu cầu**: Docker Desktop hoặc Docker Engine

```powershell
# Sử dụng Docker Compose
docker-compose up -d --build
```

Truy cập:
- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

Xem thêm: [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

---

### Phương án 2: Chạy thủ công (Development)

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip (Python package manager)

### Bước 1: Cài đặt Backend

```powershell
# Di chuyển vào thư mục backend
cd backend

# Tạo môi trường ảo
python -m venv backend_venv
.\backend_venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### Bước 2: Cài đặt Frontend

Mở terminal mới:

```powershell
# Di chuyển vào thư mục frontend
cd frontend

# Tạo môi trường ảo
python -m venv frontend_venv
.\frontend_venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy Streamlit app
streamlit run app.py
```

Frontend sẽ tự động mở tại: `http://localhost:8501`

## Cấu trúc Dự án

```
app/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── inference_engine_v4.py  # Inference Engine version 4
│   ├── requirements.txt        # Backend dependencies
│   ├── data/
│   │   └── CSTT_v4.json        # Knowledge Base (Rules)
│   └── models/
│       └── query_models.py     # Pydantic models
│
├── frontend/
│   ├── app.py                  # Streamlit application
│   ├── backup_versions/        # Orther streamlit versions
│   └── requirements.txt        # Frontend dependencies
│
└── README.md
```