# KIẾN TRÚC HỆ THỐNG

## Tổng quan

Hệ Chuyên Gia Hỗ Trợ Tuyển Chọn và Tư Vấn Nghĩa Vụ Quân Sự được thiết kế theo mô hình **Client-Server** với kiến trúc **3 tầng (3-tier architecture)** tách biệt rõ ràng giữa các lớp Presentation, Business Logic và Data.


---

## Kiến trúc tổng thể

### Sơ đồ phân tầng

```
┌───────────────────────────────────────────────────────────────────────┐
│                            USER LAYER                                 │
│                        (Presentation Tier)                            │
│                                                                       │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓      │
│  ┃           Streamlit Frontend (Port 8501)                    ┃      │
│  ┃                                                             ┃      │
│  ┃  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐  ┃      │
│  ┃  │   Tab 1:     │  │   Tab 2:     │  │    Tab 3-5:       │  ┃      │
│  ┃  │  Thông tin   │  │  Tiêu chuẩn  │  │  Hoàn cảnh        │  ┃      │
│  ┃  │  cơ bản      │  │  Sức khỏe    │  │  đặc biệt         │  ┃      │
│  ┃  └──────────────┘  └──────────────┘  └───────────────────┘  ┃      │
│  ┃                                                             ┃      │
│  ┃  • Biểu mẫu nhập liệu & Xác thực                            ┃      │
│  ┃  • Hiển thị & Định dạng kết quả                             ┃      │
│  ┃  • Trình bày trích dẫn pháp luật                            ┃      │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛      │
└────────────────────────────────┼──────────────────────────────────────┘
                                 │
                                 │ HTTP/REST API (JSON)
                                 │ Request: POST /consult
                                 │ Response: {ket_luan, giai_thich, trace}
                                 │
┌────────────────────────────────▼──────────────────────────────────────┐
│                          BUSINESS LAYER                               │
│                         (Application Tier)                            │
│                                                                       │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓      │
│  ┃             FastAPI Backend (Port 8000)                     ┃      │
│  ┃                                                             ┃      │
│  ┃  ┌────────────────────────────────────────────────────┐     ┃      │
│  ┃  │            API Endpoints                           │     ┃      │
│  ┃  │  • GET  /         → Health check                   │     ┃      │
│  ┃  │  • POST /consult  → Main consultation endpoint     │     ┃      │
│  ┃  │  • GET  /docs     → Swagger UI                     │     ┃      │
│  ┃  └──────────────────────┬─────────────────────────────┘     ┃      │
│  ┃                         │                                   ┃      │
│  ┃  ┌──────────────────────▼─────────────────────────────┐     ┃      │
│  ┃  │       Pydantic Models (Data Validation)            │     ┃      │
│  ┃  │  • CitizenFacts: 29 input fields                   │     ┃      │
│  ┃  │  • Type checking & constraints                     │     ┃      │
│  ┃  └──────────────────────┬─────────────────────────────┘     ┃      │
│  ┃                         │                                   ┃      │
│  ┃  ┌──────────────────────▼─────────────────────────────┐     ┃      │
│  ┃  │      Inference Engine (inference_engine.py)        │     ┃      │
│  ┃  │                                                    │     ┃      │
│  ┃  │  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓     │     ┃      │
│  ┃  │  ┃   Forward Chaining Algorithm              ┃     │     ┃      │
│  ┃  │  ┃                                           ┃     │     ┃      │
│  ┃  │  ┃  1. Load Rules (sorted by priority)       ┃     │     ┃      │
│  ┃  │  ┃     └─ Priority: 100→0→-5→-50→-100        ┃     │     ┃      │
│  ┃  │  ┃                                           ┃     │     ┃      │
│  ┃  │  ┃  2. Initialize Working Memory             ┃     │     ┃      │
│  ┃  │  ┃     └─ known_facts = initial_facts + def's┃     │     ┃      │
│  ┃  │  ┃                                           ┃     │     ┃      │
│  ┃  │  ┃  3. Matching Phase                        ┃     │     ┃      │
│  ┃  │  ┃     └─ _evaluate_rule(conditions, ops)    ┃     │     ┃      │
│  ┃  │  ┃     └─ _check_condition(fact, op, val)    ┃     │     ┃      │
│  ┃  │  ┃                                           ┃     │     ┃      │
│  ┃  │  ┃  4. Execution Phase                       ┃     │     ┃      │
│  ┃  │  ┃     └─ Execute actions (set/add_to_list)  ┃     │     ┃      │
│  ┃  │  ┃     └─ Update working memory              ┃     │     ┃      │
│  ┃  │  ┃                                           ┃     │     ┃      │
│  ┃  │  ┃  5. Trace Recording                       ┃     │     ┃      │
│  ┃  │  ┃     └─ Store fired rules in solution_trace┃     │     ┃      │
│  ┃  │  ┃                                           ┃     │     ┃      │
│  ┃  │  ┃  6. Conclusion Compilation                ┃     │     ┃      │
│  ┃  │  ┃     └─ _compile_final_result()            ┃     │     ┃      │
│  ┃  │  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛     │     ┃      │
│  ┃  └────────────────────────────────────────────────────┘     ┃      │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛      │
└────────────────────────────────┼──────────────────────────────────────┘                                                 │ File I/O (JSON Load)
                                 │
┌────────────────────────────────▼──────────────────────────────────────┐
│                           DATA LAYER                                  │
│                          (Data Tier)                                  │
│                                                                       │
│  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓      │
│  ┃            CSTT_v5.json (Knowledge Base)                    ┃      │
│  ┃                                                             ┃      │
│  ┃  {                                                          ┃      │
│  ┃    "rules": [                                               ┃      │
│  ┃      {                                                      ┃      │
│  ┃        "id": "TUOI_1",                                      ┃      │
│  ┃        "description": "Đạt chuẩn 18-25 tuổi",               ┃      │
│  ┃        "priority": 0,                                       ┃      │
│  ┃        "citation": "Điều 30, Luật NVQS 2015",               ┃      │
│  ┃        "quote": "Công dân đủ 18 tuổi...",                   ┃      │
│  ┃        "conditions": [                                      ┃      │
│  ┃          {"fact": "tuoi", "operator": ">=", "value": 18},   ┃      │
│  ┃          {"fact": "tuoi", "operator": "<=", "value": 25}    ┃      │
│  ┃        ],                                                   ┃      │
│  ┃        "actions": [                                         ┃      │
│  ┃          {"fact": "TIEU_CHUAN_TUOI", "value": "Đạt"},       ┃      │
│  ┃          {"fact": "LY_DO_TUOI_DETAIL", "value": "..."}      ┃      │
│  ┃        ]                                                    ┃      │
│  ┃      },                                                     ┃      │
│  ┃      ... (38 more rules)                                    ┃      │
│  ┃    ]                                                        ┃      │
│  ┃  }                                                          ┃      │
│  ┃                                                             ┃      │
│  ┃  ┌───────────────────────────────────────────────┐          ┃      │
│  ┃  │ • Total: 39 Rules                             │          ┃      │
│  ┃  │ • Volunteer Rule: 1 (Priority: 100)           │          ┃      │
│  ┃  │ • Intermediate Rules: 32 (Priority: 0, -5)    │          ┃      │
│  ┃  │ • Collection Rules: 5 (Priority: -50)         │          ┃      │
│  ┃  │ • Final Compilation: 1 (Priority: -100)       │          ┃      │
│  ┃  └───────────────────────────────────────────────┘          ┃      │
│  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛      │
└────────────────────────────────┼──────────────────────────────────────┘
```

---

## Chi tiết các tầng

### 1. Presentation Tier - Frontend (Streamlit)

#### Trách nhiệm
- Hiển thị giao diện người dùng
- Thu thập thông tin đầu vào (29 facts)
- Gọi API Backend
- Render kết quả tư vấn với format dễ đọc

#### Công nghệ
- **Framework:** Streamlit 1.28+
- **HTTP Client:** Requests library
- **Styling:** Custom CSS + .streamlit/config.toml

#### Cấu trúc giao diện

```
app.py (Main Entry Point)
│
├─ st.set_page_config()  → Cấu hình trang
│
├─ st.tabs([...])  → 5 tabs chính
│  │
│  ├─ Tab 1: Thông tin cơ bản
│  │  ├─ tuoi (numbeinput)
│  │  ├─ trinh_do_van_hoa (selectbox)
│  │  ├─ duoc_tam_hoan_vi_hoc (checkbox)
│  │  └─ ... (6 fields total)
│  │
│  ├─ Tab 2: Tiêu chuẩn sức khỏe
│  │  ├─ chi_so_BMI (numbeinput + auto-calculate)
│  │  ├─ do_can_thi (numbeinput)
│  │  ├─ vien_thi (checkbox)
│  │  └─ ... (6 fields total)
│  │
│  ├─ Tab 3: Trường hợp Tạm hoãn
│  │  ├─ st.expander("Lý do sức khỏe")
│  │  ├─ st.expander("Lý do học tập")
│  │  ├─ st.expander("Lý do gia đình")
│  │  └─ st.expander("Lý do đặc biệt") (8 fields)
│  │
│  ├─ Tab 4: Trường hợp Miễn
│  │  ├─ st.expander("Miễn tuyệt đối")
│  │  ├─ st.expander("Con một")
│  │  └─ st.expander("Thời gian công tác") (7 fields)
│  │
│  └─ Tab 5: Tình nguyện
│     └─ tinh_nguyen_nhap_ngu (checkbox)
│
├─ st.button("Bắt đầu tư vấn")  → Trigger consultation
│
└─ Display Results
   ├─ st.success/error(ket_luan)
   ├─ st.info(giai_thich)
   └─ st.expander("Chi tiết suy diễn")
      └─ Render solution_trace với citations
```

#### Luồng xử lý Frontend

```
User Input → Validate → Build JSON Payload → POST /consult
                                                    ↓
Response ← Parse JSON ← Receive API Response ← Backend
   ↓
Format & Display Results
```

---

### 2. Application Tier - Backend (FastAPI)

#### Trách nhiệm
- Cung cấp RESTful API endpoints
- Validate dữ liệu đầu vào (Pydantic)
- Điều phối Inference Engine
- Trả về kết quả JSON

#### Công nghệ
- **Framework:** FastAPI 0.100+
- **Validation:** Pydantic 2.0+
- **Server:** Uvicorn (ASGI)
- **API Docs:** Swagger UI (auto-generated)

#### API Endpoints

| Method | Endpoint | Request Body | Response | Mô tả |
|--------|----------|--------------|----------|-------|
| `GET` | `/` | - | `["Chào mừng..."]` | Health check |
| `POST` | `/consult` | `CitizenFacts` (29 fields) | `{ket_luan, giai_thich, trace}` | Main consultation |
| `GET` | `/docs` | - | Swagger UI HTML | Interactive API docs |
| `GET` | `/redoc` | - | ReDoc HTML | Alternative docs |

#### Data Models (Pydantic)

```python
class CitizenFacts(BaseModel):
    # Thông tin cơ bản (6 fields)
    tuoi: int
    trinh_do_van_hoa: str
    duoc_tam_hoan_vi_hoc: bool
    dia_phuong_kho_khan_giao_quan: bool
    vung_dac_biet_kho_khan: bool
    dan_toc_thieu_so_duoi_10000: bool
    
    # Tiêu chuẩn sức khỏe (6 fields)
    loai_suc_khoe: Optional[int]
    chi_so_BMI: float
    do_can_thi: float
    vien_thi: bool
    nghien_ma_tuy: bool
    nhiem_HIV_AIDS: bool
    
    # Trường hợp tạm hoãn (8 fields)
    du_suc_khoe_phuc_vu: bool = True
    lao_dong_duy_nhat: bool = False
    gia_dinh_thiet_hai_nang_khong_con_ld_khac: bool = False
    la_con_benh_binh_cd_61_80: bool = False
    co_anh_chi_em_dang_phuc_vu_tai_ngu: bool = False
    thuoc_dien_di_dan_3_nam_dau: bool = False
    dang_hoc_giao_duc_pho_thong: bool = False
    dang_hoc_dh_cd_chinh_quy: bool = False
    
    # Trường hợp miễn (8 fields)
    la_con_cua_liet_si: bool = False
    la_con_cua_thuong_binh_hang_mot: bool = False
    la_anh_hoac_em_trai_cua_liet_si: bool = False
    la_mot_con_cua_thuong_binh_hang_hai: bool = False
    la_mot_con_benh_binh_cd_81_tro_len: bool = False
    la_mot_con_cdac_cd_81_tro_len: bool = False
    lam_cong_tac_co_yeu_khong_phai_quan_nhan: bool = False
    thoi_gian_cong_tac_vung_dbkk_thang: int = 0
    
    # Tình nguyện (1 field)
    tinh_nguyen_nhap_ngu: bool
```

#### Luồng xử lý Backend

```
POST /consult
    ↓
Pydantic Validation (CitizenFacts)
    ↓
facts.dict() → initial_facts
    ↓
engine.evaluate(initial_facts)
    ↓
(ket_luan, giai_thich, solution_trace)
    ↓
Filter trace (remove FINAL_* rules)
    ↓
Return JSON Response
```

---

### 3. Business Logic - Inference Engine

#### Trách nhiệm
- Load Knowledge Base từ CSTT_v5.json
- Thực thi thuật toán Forward Chaining
- Quản lý Working Memory (known_facts)
- Tạo Solution Trace (explanation)

#### Kiến trúc Inference Engine 
[inference_engine_v4.py](../backend/inference_engine_v4.py)
```
inference_engine_v4.py
│
├─ Class: InferenceEngine
│  │
│  ├─ __init__(self, json_path: str)
│  │  ├─ Load CSTT_v5.json
│  │  ├─ Parse rules list
│  │  └─ Sort by priority (descending)
│  │
│  ├─ evaluate(self, initial_facts: dict)
│  │  ├─ Initialize known_facts
│  │  ├─ Run forward chaining loop
│  │  └─ Return (ket_luan, giai_thich, trace)
│  │
│  ├─ _evaluate_rule(self, rule, known_facts)
│  │  ├─ Check pre_conditions
│  │  ├─ Evaluate conditions with operator
│  │  └─ Return True/False
│  │
│  ├─ _check_condition(self, fact, operator, value, known_facts)
│  │  ├─ Handle operators: ==, !=, >, <, >=, <=
│  │  └─ Return boolean result
│  │
│  ├─ _execute_actions(self, actions, known_facts)
│  │  ├─ Handle "set" actions
│  │  ├─ Handle "add_to_list" actions
│  │  └─ Update known_facts in-place
│  │
│  └─ _compile_final_result(self, known_facts)
│     ├─ Build KET_LUAN string
│     ├─ Build GIAI_THICH string
│     └─ Set FINAL_STOP flag
```

#### Thuật toán Forward Chaining
[pseudocode_inference_engine.txt](./pseudocode_inference_engine.txt)
```
ALGORITHM: Forward Chaining Inference

INPUT: initial_facts (29 fields)
OUTPUT: (ket_luan, giai_thich, solution_trace)

1. INITIALIZATION
   ├─ known_facts ← initial_facts + defaults
   ├─ solution_trace ← {}
   └─ new_facts_found ← True

2. MAIN LOOP
   WHILE new_facts_found DO
      new_facts_found ← False
      
      FOR EACH rule IN sorted_rules DO
         IF rule NOT IN solution_trace THEN
            IF pre_conditions SATISFIED THEN
               IF conditions MATCH THEN
                  ├─ EXECUTE actions
                  ├─ UPDATE known_facts
                  ├─ RECORD in solution_trace
                  └─ new_facts_found ← True
                  
                  IF known_facts["FINAL_STOP"] THEN
                     BREAK
               END IF
            END IF
         END IF
      END FOR
   END WHILE

3. RETURN
   RETURN (
      known_facts["KET_LUAN"],
      known_facts["GIAI_THICH"],
      solution_trace
   )
```

#### Priority System

Rules được sắp xếp theo mức độ ưu tiên:

| Priority | Rule Type | Số lượng | Mô tả |
|----------|-----------|----------|-------|
| `100` | Intermediate (Age, Education) | 8 | Tính toán tiêu chuẩn cơ bản |
| `0` | Intermediate (Health, Cases) | 24 | Tính toán sức khỏe, hoàn cảnh |
| `-50` | Collection (FINAL_CHECK_*) | 6 | Thu thập lý do không đủ điều kiện |
| `-100` | Final (FINAL_COMPILE) | 1 | Tổng hợp kết luận cuối cùng |

---

### 4. Data Tier - Knowledge Base (CSTT_v5.json)
[CSTT_v5.json](../backend/data/CSTT_v5.json)
#### Cấu trúc file JSON
#### Phân loại Rules
**Tổng số: 39 luật**

**1. Intermediate Rules - Age (Priority: mặc định = 0)**
- `TUOI_1`: Đạt chuẩn thông thường (18-25 tuổi)
- `TUOI_2`: Đạt chuẩn có hoãn học (đến 27 tuổi)
- `TUOI_3`: Không đạt - dưới tuổi (< 18)
- `TUOI_4`: Không đạt - quá tuổi (> 27)
- `TUOI_5`: Không đạt - quá tuổi 25, không hoãn học

**2. Intermediate Rules - Health (Priority: 0 và -5)**
- `SK_1`: Đạt chuẩn - Tất cả các tiêu chí sức khỏe (Priority: -5)
- `SK_3`: Không đạt - Ma túy
- `SK_4`: Không đạt - Tật khúc xạ (cận thị > 1.5 diop, viễn thị)
- `SK_5`: Không đạt - BMI (< 18.0 hoặc > 29.9)
- `SK_6`: Không đạt - HIV/AIDS

**3. Intermediate Rules - Education (Priority: 0)**
- `VH_1`: Đạt chuẩn thông thường (Lớp 8+)
- `VH_2`: Đạt chuẩn - Địa phương khó khăn (Lớp 7)
- `VH_3`: Đạt chuẩn - Vùng ĐBKK / Dân tộc thiểu số (Lớp 5+)
- `VH_4`: Không đạt (Dưới Lớp 5)
- `VH_5`: Không đạt - Lớp 7, địa phương không khó khăn
- `VH_6`: Không đạt - Lớp 5-6, không thuộc diện đặc biệt

**4. Intermediate Rules - Deferment Cases (Priority: 0)**
- `TAM_HOAN_1`: Tạm hoãn - Sức khỏe
- `TAM_HOAN_2_a`: Tạm hoãn - Gia cảnh 1a (Lao động duy nhất)
- `TAM_HOAN_2_b`: Tạm hoãn - Gia cảnh 1b (Thiên tai, không còn lao động khác)
- `TAM_HOAN_3`: Tạm hoãn - Gia cảnh 2 (Con bệnh binh 61-80%)
- `TAM_HOAN_4`: Tạm hoãn - Gia cảnh 3 (Anh/em tại ngũ)
- `TAM_HOAN_5`: Tạm hoãn - Công tác 1 (Di dân 3 năm đầu)
- `TAM_HOAN_6`: Tạm hoãn - Công tác 2 (Cán bộ vùng ĐBKK < 24 tháng)
- `TAM_HOAN_7`: Tạm hoãn - Học tập

**5. Intermediate Rules - Exemption Cases (Priority: 0)**
- `MIEN_1_a`: Miễn - Gia cảnh 1a (Con liệt sĩ)
- `MIEN_1_b`: Miễn - Gia cảnh 1b (Con thương binh hạng 1)
- `MIEN_2`: Miễn - Gia cảnh 2 (Anh/em liệt sĩ)
- `MIEN_3_a`: Miễn - Gia cảnh 3a (Con một của thương binh hạng 2)
- `MIEN_3_b`: Miễn - Gia cảnh 3b (Con một của bệnh binh 81%+)
- `MIEN_3_c`: Miễn - Gia cảnh 3c (Con một của CĐDC 81%+)
- `MIEN_4`: Miễn - Công tác 1 (Cơ yếu)
- `MIEN_5`: Miễn - Công tác 2 (Cán bộ vùng ĐBKK 24+ tháng)

**6. Final Rules - Volunteer (Priority: 100)**
- `FINAL_TINH_NGUYEN`: Ưu tiên 1 - Xử lý tình nguyện (dừng sớm nếu tình nguyện)

**7. Collection Rules (Priority: -50)**
- `FINAL_CHECK_MIEN`: Thu thập lý do miễn nghĩa vụ
- `FINAL_CHECK_HOAN`: Thu thập lý do tạm hoãn
- `FINAL_CHECK_TUOI`: Thu thập lý do không đạt tuổi
- `FINAL_CHECK_SK`: Thu thập lý do không đạt sức khỏe
- `FINAL_CHECK_VH`: Thu thập lý do không đạt văn hóa

**8. Final Compilation Rule (Priority: -100)**
- `FINAL_COMPILE_KET_LUAN`: Tổng hợp kết luận cuối cùng

---

## Luồng dữ liệu End-to-End

### Kịch bản: Tư vấn cho công dân 20 tuổi, đang học ĐH

```
┌──────────────────────────────────────────────────────────────┐
│ 1. USER INPUT (Streamlit Frontend)                          │
├──────────────────────────────────────────────────────────────┤
│   Tab 1: tuoi = 20                                          │
│   Tab 1: trinh_do_van_hoa = 12/12                          │
│   Tab 2: chi_so_BMI = 22.0                                  │
│   Tab 3: dang_hoc_dh_cd_chinh_quy = True                    │
│   ... (25 other fields = default/False)                     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ HTTP POST /consult
                           │ Content-Type: application/json
                           │
┌──────────────────────────▼───────────────────────────────────┐
│ 2. BACKEND API (FastAPI)                                    │
├──────────────────────────────────────────────────────────────┤
│   Receive JSON payload                                      │
│   Validate with CitizenFacts model                          │
│   initial_facts = facts.dict()                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ engine.evaluate(initial_facts)
                           │
┌──────────────────────────▼───────────────────────────────────┐
│ 3. INFERENCE ENGINE (Forward Chaining)                      │
├──────────────────────────────────────────────────────────────┤
│   Iteration 1: Priority 100                                 │
│   ├─ AGE_1 fires → TIEU_CHUAN_TUOI = "Đạt"               │
│   └─ EDU_1 fires → TIEU_CHUAN_VAN_HOA = "Đạt"            │
│                                                             │
│   Iteration 2: Priority 0                                  │
│   ├─ HEALTH_1 fires → (No health issues detected)        │
│   ├─ DEFE8 fires → DIEN_HOAN = True                    │
│   └─         └─ LY_DO_HOAN_DETAIL = "Đang học ĐH..."       │
│                                                             │
│   Iteration 3: Priority -50                                │
│   └─ FINAL_CHECK_DEFER fires                               │
│       └─ Add to LY_DO_TONG_HOP: "Thuộc trường hợp..."      │
│                                                             │
│   Iteration 4: Priority -100                               │
│   └─ FINAL_COMPILE fires                                   │
│       ├─ KET_LUAN = "TẠM HOÃN nghĩa vụ quân sự"            │
│       └─ GIAI_THICH = "Bạn thuộc diện tạm hoãn..."         │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ Return (ket_luan, giai_thich, trace)
                           │
┌──────────────────────────▼───────────────────────────────────┐
│ 4. BACKEND API (Response Formatting)                        │
├──────────────────────────────────────────────────────────────┤
│   Filter trace (remove FINAL_* rules)                       │
│   Build JSON response:                                      │
│   {                                                          │
│     "ket_luan": "TẠM HOÃN nghĩa vụ quân sự",                │
│     "giai_thich": "Bạn thuộc diện tạm hoãn...",             │
│     "trace": [                                              │
│       {                                                      │
│         "id": "DEFE8",                                  │
│         "description": "...",                               │
│         "citation": "Điểm g, Khoản 1, Điều 41, Luật NVQS",  │
│         "quote": "Công dân được tạm hoãn..."                │
│       }                                                      │
│     ]                                                        │
│   }                                                          │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ HTTP 200 OK (JSON)
                           │
┌──────────────────────────▼───────────────────────────────────┐
│ 5. FRONTEND (Result Display)                                │
├──────────────────────────────────────────────────────────────┤
│   st.info("⏸️ TẠM HOÃN nghĩa vụ quân sự")                   │
│   st.write(giai_thich)                                      │
│   st.expander("Chi tiết suy diễn"):                         │
│     └─ Display citations & quotes                           │
└──────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture (Docker)

### Container Orchestration

[frontend/Dockerfile](../frontend/Dockerfile)\
[frontend/.dockerignore](../frontend/.dockerignore)\
[backend/Dockerfile](../backend/Dockerfile)\
[backend/.dockerignore](../backend/.dockerignore)\
[docker-compose.yml](../docker-compose.yml)

---

## Technology Stack Summary

| Layer | Component | Technology | Version | Purpose |
|-------|-----------|------------|---------|---------|
| **Presentation** | Frontend | Streamlit | 1.28+ | Web UI |
| **Presentation** | HTTP Client | Requests | 2.31+ | API calls |
| **Application** | API Framework | FastAPI | 0.100+ | RESTful API |
| **Application** | Validation | Pydantic | 2.0+ | Data models |
| **Application** | ASGI Server | Uvicorn | 0.23+ | Web server |
| **Business Logic** | Inference Engine | Python | 3.8+ | Forward Chaining |
| **Data** | Knowledge Base | JSON | - | Rule storage |
| **Infrastructure** | Containerization | Docker | 20.10+ | Deployment |
| **Infrastructure** | Orchestration | Docker Compose | 2.0+ | Multi-container |

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Forward Chaining Algorithm](https://en.wikipedia.org/wiki/Forward_chaining)
- [3-Tier Architecture Pattern](https://en.wikipedia.org/wiki/Multitiearchitecture)