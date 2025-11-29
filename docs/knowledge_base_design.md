# BÁO CÁO: THIẾT KẾ CƠ SỞ TRI THỨC HỆ THỐNG TƯ VẤN NGHĨA VỤ QUÂN SỰ

## Giới thiệu

Mục tiêu của Giai đoạn này là xây dựng một Cơ sở Tri thức (CSTT) hoàn chỉnh, có cấu trúc, chính xác về mặt pháp lý và có thể được sử dụng bởi một Bộ suy diễn (Giai đoạn 3). Quy trình thiết kế được thực hiện theo 3 giai đoạn chính.

---

## Giai đoạn 1: Xây dựng Mô hình Biểu diễn Tri thức (BDTT)

### Bước 1: Chọn lựa mô hình BDTT

Dựa vào quá trình thu thập và phân loại tri thức, ta thấy tri thức tồn tại ở hai dạng chính:
* **Tri thức Khái niệm:** Các thông tin đầu vào về công dân (ví dụ: tuổi, độ cận thị, hoàn cảnh gia đình).
* **Tri thức Quy định:** Các logic nghiệp vụ, các điều luật (ví dụ: NẾU `tuoi < 18` THÌ `TIEU_CHUAN_TUOI = "Không đạt"`).

Lựa chọn mô hình biểu diễn tri thức: **Mô hình Tri thức nhiều thành phần (Hybrid Model)**, kết hợp hai phương pháp:
* **Hệ luật dẫn (Rule-Based System):** Biểu diễn 40 quy tắc logic, điều kiện, và các trường hợp Tạm hoãn/Miễn.
* **Frame (Khái niệm):** Được đơn giản hóa để định nghĩa các "Sự kiện" (Facts) hay "Khái niệm" (Concepts) mà các luật sẽ sử dụng (ví dụ: `tuoi`, `loai_suc_khoe`, `la_con_cua_liet_si`...).

Cụ thể: lựa chọn mô hình tri thức nhiều thành phần với 3 thành phần chính: **(C, Ops, Rules)**.

### Bước 2: Phân tích Tri thức

#### Thành phần C (Concepts - Khái niệm/Sự kiện)
Bao gồm 29 sự kiện (facts) đầu vào mà hệ thống (Frontend) sẽ thu thập từ người dùng. Các sự kiện này được tổ chức thành 6 nhóm logic rõ rệt:

* **Thông tin Cơ bản (6 sự kiện):**
    * `tuoi`
    * `trinh_do_van_hoa`
    * `duoc_tam_hoan_vi_hoc`
    * `dia_phuong_kho_khan_giao_quan`
    * `vung_dac_biet_kho_khan`
    * `dan_toc_thieu_so_duoi_10000`
* **Tiêu chuẩn Sức khỏe (6 sự kiện):**
    * `loai_suc_khoe`
    * `chi_so_BMI`
    * `do_can_thi`
    * `vien_thi`
    * `nghien_ma_tuy`
    * `nhiem_HIV_AIDS`
* **Trường hợp Tạm hoãn (8 sự kiện):**
    * `du_suc_khoe_phuc_vu`
    * `lao_dong_duy_nhat`
    * `gia_dinh_thiet_hai_nang_khong_con_ld_khac`
    * `la_con_benh_binh_cd_61_80`
    * `co_anh_chi_em_dang_phuc_vu_tai_ngu`
    * `thuoc_dien_di_dan_3_nam_dau`
    * `dang_hoc_giao_duc_pho_thong`
    * `dang_hoc_dh_cd_chinh_quy`
* **Trường hợp Miễn (7 sự kiện):**
    * `la_con_cua_liet_si`
    * `la_con_cua_thuong_binh_hang_mot`
    * `la_anh_hoac_em_trai_cua_liet_si`
    * `la_mot_con_cua_thuong_binh_hang_hai`
    * `la_mot_con_benh_binh_cd_81_tro_len`
    * `la_mot_con_cdac_cd_81_tro_len`
    * `lam_cong_tac_co_yeu_khong_phai_quan_nhan`
* **Sự kiện Logic Chung (Tạm hoãn/Miễn) (1 sự kiện):**
    * `thoi_gian_cong_tac_vung_dbkk_thang` (Sự kiện này được dùng để kích hoạt `R_TAM_HOAN_6` hoặc `R_MIEN_5` tùy vào giá trị).
* **Tình nguyện (1 sự kiện):**
    * `tinh_nguyen_nhap_ngu`

#### Thành phần Ops (Toán tử)

* **Các toán tử so sánh:**
    * `==` (Bằng)
    * `!=` (Không bằng)
    * `>=` (Lớn hơn hoặc bằng)
    * `>` (Lớn hơn)
    * `<` (Nhỏ hơn)
    * `<=` (Nhỏ hơn hoặc bằng)
    * `IN` (Nằm trong một danh sách)
* **Các toán tử logic:**
    * `AND`
    * `OR`

#### Thành phần Rules (Luật)
Định nghĩa 40 luật, chia thành hai cấp độ:
1.  **Luật Trung gian (Cấp 1):** 33 luật tính toán cơ sở (ví dụ: `R_TUOI_*`, `R_SK_*`, `R_VH_*`, `R_TAM_HOAN_*`, `R_MIEN_*`).
2.  **Luật Kết luận (Cấp 2):** 7 luật `R_FINAL_*` dùng để tổng hợp kết quả cuối cùng.

### Bước 3: Mối liên hệ

* Các **Luật Trung gian (Cấp 1)** đọc **Sự kiện Đầu vào** (từ Nhóm A) để tạo ra các **Sự kiện Trung gian** (ví dụ: `TIEU_CHUAN_TUOI = "Đạt"`, `DIEN_MIEN = True`, `LY_DO_HOAN_DETAIL = "..."`).
* Các **Luật Kết luận (Cấp 2)** đọc các **Sự kiện Trung gian** để tạo ra **Kết quả Cuối cùng** (`KET_LUAN` và `GIAI_THICH`).

### Bước 4: Lập mô hình Tích hợp

Mô hình tích hợp sử dụng logic "Thu thập Lý do" (Reason Collection):
1.  Tất cả các luật trung gian chạy trước để tính toán mọi trạng thái của từng tiêu chí (tuổi, sức khỏe, văn hóa, trường hợp hoãn/miễn).
2.  Các luật `R_FINAL_CHECK_*` chạy sau để "thu thập" tất cả các lý do không đủ điều kiện vào một danh sách (fact) là `LY_DO_TONG_HOP`.
3.  Luật `R_FINAL_COMPILE_KET_LUAN` chạy cuối cùng. Nó kiểm tra danh sách `LY_DO_TONG_HOP`:
    * Nếu danh sách rỗng $\rightarrow$ `KET_LUAN = "ĐỦ ĐIỀU KIỆN"`.
    * Nếu danh sách có lý do $\rightarrow$ `KET_LUAN = "KHÔNG ĐỦ ĐIỀU KIỆN"` và `GIAI_THICH` = (nối các lý do trong danh sách).

---

## Giai đoạn 2: Tổ chức CSTT cụ thể trên máy tính

### 2.1. Lựa chọn phương pháp lưu trữ

Chúng ta đã chọn **Cách 1: Lưu trữ bằng tập tin văn bản có cấu trúc**.
* **Định dạng cụ thể:** **JSON**.
* **Lý do:**
    * **Khả năng tích hợp:** JSON dễ dàng được đọc và phân tích (parse) bởi ngôn ngữ lập trình Python, phù hợp với kiến trúc Frontend/Backend.
    * **Khả năng bảo trì:** Cấu trúc key-value của JSON rất rõ ràng, cho phép kỹ sư tri thức dễ dàng đọc, thêm, xóa hoặc sửa đổi các luật.
    * **Khả năng giải thích:** Cấu trúc JSON cho phép thêm các trường tùy chỉnh như `citation` và `quote` để hỗ trợ trực tiếp cho Cơ chế Giải thích.

### 2.2. Cấu trúc file `CSTT_v4.json`

File `CSTT_v4.json` là kết quả cuối cùng của Giai đoạn 2. Mỗi luật trong mảng `rules` có cấu trúc chuẩn hóa:
* **Định danh:** `id`, `description`.
* **Giải thích:** `citation` (vị trí điều luật), `quote` (trích dẫn luật).
* **Ưu tiên:** `priority` (sử dụng các nhóm `100`, `0`, `-50`, `-100` để quản lý thứ tự suy diễn).
* **Vế IF (Giả thiết):** `pre_conditions` (điều kiện tiên quyết), `conditions_operator` (`AND`/`OR`), `conditions` (danh sách các điều kiện).
* **Vế THEN (Kết luận):** `actions` (danh sách các hành động).

---

## Giai đoạn 3: Thiết kế các tác vụ cơ bản trên CSTT

Đây là giai đoạn thiết kế **Bộ suy diễn (Inference Engine)** (`Bo_suy_dien_v4.py`), thực hiện các tác vụ cơ bản trên CSTT đã lưu:

* **Tác vụ Nạp (Loading):** Hàm `__init__` đọc file `CSTT_v4.json`, phân tích và sắp xếp 40 luật vào bộ nhớ dựa trên `priority`.
* **Tác vụ So khớp (Matching):** Hàm `_check_condition` (so sánh 1 sự kiện) và `_evaluate_rule` (so sánh 1 luật). Các hàm này xử lý logic `AND`/`OR` và logic `!= "Đạt"` (khi sự kiện là `None`).
* **Tác vụ Cập nhật & Suy diễn:** Hàm `evaluate` là trái tim của hệ thống.
    * Nó triển khai thuật toán **Suy diễn tiến (Forward-Chaining)**.
    * Nó khởi tạo `known_facts` (bao gồm các giá trị mặc định như `FINAL_STOP = False`).
    * Nó lặp (`while`) qua CSTT đã sắp xếp, kích hoạt các luật, và cập nhật `known_facts`.
    * Nó hỗ trợ các `actions` (hành động) đặc biệt:
        * **`"add_to_list"`:** Thêm lý do vào `known_facts["LY_DO_TONG_HOP"]`.
        * **`"COMPILE_FINAL_RESULT"`:** Kích hoạt hàm `_compile_final_result` để tổng hợp kết luận cuối cùng.
        * **`"FINAL_STOP"`:** Dừng suy diễn ngay lập tức nếu `tinh_nguyen_nhap_ngu = True`.

### Kết luận Báo cáo

Giai đoạn Thiết kế Cơ sở Tri thức đã hoàn tất. Chúng ta đã thành công xây dựng một CSTT (`CSTT_v4.json`) logic, chính xác, và dễ bảo trì, cùng với một Bộ suy diễn (`Bo_suy_dien_v4.py`) đáp ứng đầy đủ các yêu cầu phức tạp của bài toán tư vấn.