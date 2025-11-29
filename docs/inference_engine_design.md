# BÁO CÁO: THIẾT KẾ BỘ SUY DIỄN (INFERENCE ENGINE)

## Bước 1: Thu thập các bài toán cụ thể

* **Mục tiêu:** Xác định rõ đầu vào (input), đầu ra (output) mong muốn và các ràng buộc.
* **Thực hiện:**
    * **Đầu vào (Giả thiết `GT`):** Là 29 sự kiện (facts) về công dân (ví dụ: `tuoi`, `do_can_thi`, `la_con_cua_liet_si`...).
    * **Đầu ra (Kết luận `KL`):** Là một kết luận tổng hợp (`KET_LUAN`) và một giải thích chi tiết (`GIAI_THICH`), theo sau là phần giải thích đầy đủ trên từng tiêu chí (tuổi, sức khỏe, văn hóa, trường hợp tạm hoãn/ miễn), kèm theo là trích luật.
    * **Bộ kiểm thử:** Sử dụng 15 kịch bản trong file `Cau_Truy_Van.docx` làm bộ dữ liệu chuẩn để đánh giá và gỡ lỗi hệ thống.

Ví dụ (Tình huống 15):
- Input: 20 tuổi, cận 9.0 diop, trình độ học vấn 12/12, đang học đại học.
- Output: 
    * Kết luận: KHÔNG ĐỦ ĐIỀU KIỆN GỌI NHẬP NGŨ.
    * Giải thích: Thuộc trường hợp tạm hoãn, Không đạt tiêu chuẩn về sức khỏe.
    * Chi tiết:
        * Tiêu chuẩn về Độ tuổi:
            * Căn cứ pháp lý: Điều 30, Luật Nghĩa vụ quân sự số 78/2015/QH13:\
            "Công dân đủ 18 tuổi được gọi nhập ngũ; độ tuổi gọi nhập ngũ từ đủ 18 tuổi đến hết 25 tuổi; công dân được đào tạo trình độ cao đẳng, đại học đã được tạm hoãn gọi nhập ngũ thì độ tuổi gọi nhập ngũ đến hết 27 tuổi.” 
            * Kết luận tiêu chuẩn: Đạt tiêu chuẩn về tuổi. Nằm trong độ tuổi gọi nhập ngũ (từ đủ 18 đến hết 25 tuổi).
        * Tiêu chuẩn về Sức khỏe: 
            * Căn cứ pháp lý: Điểm c, Khoản 3, Điều 4, Thông tư số 148/2018/TT-BQP (sửa đổi bởi Thông tư số 68/2025/TT-BQP):\
            "Không gọi nhập ngũ vào Quân đội những công dân mắc tật khúc xạ cận thị lớn hơn 1.5 diop trở lên, viễn thị các mức độ; chỉ số BMI nhỏ hơn 18.0 hoặc lớn hơn 29.9"
            * Kết luận tiêu chuẩn: Không đạt tiêu chuẩn về sức khỏe. Mắc tật khúc xạ (Cận thị > 1.5 diop hoặc Viễn thị) 
        * Tiêu chuẩn về Văn hóa:
            * Căn cứ pháp lý: Điểm a, Khoản 4, Điều 4, Thông tư số 148/2018/TT-BQP:\
            "Tuyển chọn và gọi nhập ngũ những công dân có trình độ văn hóa lớp 8 trở lên, lấy từ cao xuống thấp. Những địa phương có khó khăn không đảm bảo đủ chỉ tiêu giao quân thì báo cáo cấp có thẩm quyền xem xét, quyết định được tuyển chọn số công dân có trình độ văn hóa lớp 7."
            * Kết luận tiêu chuẩn: Đạt tiêu chuẩn về văn hóa. Trình độ văn hóa được tuyển từ lớp 8 trở lên .
        * Trường hợp tạm hoãn:
            * Căn cứ pháp lý: Điểm g, Khoản 1, Điều 41, Luật nghĩa vụ quân sự 2015:\
            "Đang học tại cơ sở giáo dục phổ thông; đang được đào tạo trình độ đại học hệ chính quy thuộc cơ sở giáo dục đại học, trình độ cao đẳng hệ chính quy thuộc cơ sở giáo dục nghề nghiệp trong thời gian một khóa đào tạo của một trình độ đào tạo.”
            * Kết luận tiêu chuẩn: Thuộc diện tạm hoãn. Đang học tại cơ sở giáo dục.

## Bước 2: Phân loại bài toán

* **Mục tiêu:** Định hướng lựa chọn phương pháp biểu diễn và suy diễn phù hợp.
* **Thực hiện:**
    * **Phân loại theo Chức năng:** **Chẩn đoán (Diagnosis)** và **Giải thích (Explanation)**. Hệ thống không chỉ đưa ra kết luận ("Không đủ điều kiện") mà còn phải giải thích *tại sao* ("Lý do: Thuộc trường hợp tạm hoãn, Không đạt tiêu chuẩn về sức khỏe").
    * **Phân loại theo Tính chất Tri thức:**
        * **Tất định (Deterministic):** Luật pháp là rõ ràng. Cùng một đầu vào luôn phải cho ra cùng một kết quả.
        * **Không đơn điệu (Non-monotonic):** Việc thêm thông tin mới có thể thay đổi kết luận (ví dụ: `tuoi: 26` $\rightarrow$ "Không đạt", nhưng thêm `duoc_tam_hoan_vi_hoc: True` $\rightarrow$ "Đạt").
        * **Đầy đủ (Complete) và Chắc chắn (Certain):** CSTT (`CSTT_v4.json`) đã bao quát 100% các quy tắc luật pháp cần thiết và các quy tắc này là tuyệt đối đúng.

## Bước 3: Mô hình hóa các bài toán

* **Mục tiêu:** Chuyển bài toán thành dạng hình thức `GT -> KL` (Giả thiết $\rightarrow$ Kết luận).
* **Thực hiện:**
    * **GT (Giả thiết):** Là tập 29 sự kiện đầu vào.
    * **KL (Kết luận):** Là các sự kiện mục tiêu `KET_LUAN` và `GIAI_THICH`.
    * **Mạng suy diễn:** Chúng ta xác định một mạng lưới suy diễn đa cấp:
        1.  `(Cấp 1)` GT $\rightarrow$ Luật Trung gian (`R_TUOI_*`, `R_SK_*`...) $\rightarrow$ Sự kiện trung gian (`TIEU_CHUAN_TUOI`, `DIEN_MIEN`...).
        2.  `(Cấp 2)` Sự kiện trung gian $\rightarrow$ Luật Thu thập (`R_FINAL_CHECK_*`) $\rightarrow$ Danh sách lý do (`LY_DO_TONG_HOP`).
        3.  `(Cấp 3)` Danh sách lý do $\rightarrow$ Luật Tổng hợp (`R_FINAL_COMPILE_*`) $\rightarrow$ KL (Kết luận).
    * **Tổng quát:** Giả thuyết (GT) $\rightarrow$ Sự kiện trung gian $\rightarrow$ các luật thu thập kiểm tra "R_FINAL" $\rightarrow$ Danh sách lý do $\rightarrow$ Luật tổng hợp F_FINAL_COMPILE $\rightarrow$ Kết luận (KL).

## Bước 4: Thiết kế thuật giải suy diễn

* **4.1. Lựa chọn Chiến lược:**
    * Chúng ta chọn chiến lược **Suy diễn tiến (Forward-Chaining)**.
    * **Lý do:** Bài toán là "data-driven" (điều khiển bằng dữ liệu). Chúng ta có nhiều `GT` và muốn biết chúng dẫn đến `KL` nào, mô phỏng chính xác quy trình chẩn đoán.

* **4.2. Mô tả Thuật toán:**
    * Thuật toán chính là **Thuật toán Tìm Bao Đóng (Closure Algorithm)**, được triển khai trong hàm `evaluate`.
    * (Mã giả được cung cấp riêng).

* **4.3. Xử lý Mâu thuẫn:**
    * Hệ thống không dùng cơ chế xử lý mâu thuẫn phức tạp. Thay vào đó, chúng ta **thiết kế CSTT để không có mâu thuẫn** (ví dụ: logic ghi đè `R_SK_1`/`R_SK_4` và logic thu thập lý do của `R_FINAL_*`).

* **4.4. Cơ chế Giải thích:**
    * BSD hỗ trợ giải thích bằng cách lưu lại `Solution_Trace` (danh sách các luật đã được kích hoạt).
    * Giao diện (Frontend) đọc `Solution_Trace`, lọc ra các luật trung gian (bỏ qua `R_FINAL_*`) và trình bày các trường `citation` (căn cứ) và `quote` (trích luật) cho người dùng.

## Bước 5: Cài đặt thử nghiệm

* **Lựa chọn Ngôn ngữ:** **Python** (vì khả năng xử lý JSON và hệ sinh thái thư viện FastAPI, Streamlit).
* **Cài đặt:**
    * `CSTT_v4.json`: Cơ sở Tri thức chứa **40 luật** (không phải 29) đã được chuẩn hóa.
    * `Bo_suy_dien_v4.py`: Chứa lớp `InferenceEngine` và các hàm hỗ trợ.
* **Các Tác vụ cơ bản được cài đặt trong `InferenceEngine`:**
    * **Nạp (Loading):** Hàm `__init__` (đọc và sắp xếp luật theo `priority`).
    * **So khớp (Matching):** Hàm `_check_condition` (xử lý `None`, `!=`, `IN`...) và `_evaluate_rule` (xử lý `pre_conditions`, `AND`/`OR`).
    * **Cập nhật & Suy diễn:** Hàm `evaluate` (vòng lặp `while`) và các hàm hỗ trợ hành động (action) đặc biệt như `_compile_final_result` và xử lý `Notes`.

## Bước 6: Nâng cao hiệu quả (Đánh giá & Gỡ lỗi)

* **Thực hiện:** Quá trình gỡ lỗi và cải tiến đã trải qua 4 phiên bản.
    * **Lần 1 (v1):** Phát hiện logic "ưu tiên" (`R_FINAL` cũ) bị sai, không đáp ứng yêu cầu giải thích Tình huống 15 (Hoãn + Không đạt SK).
    * **Điều chỉnh 1:** Thiết kế lại logic "Thu thập Lý do" (sử dụng `LY_DO_TONG_HOP`).
    * **Lần 2 (v2):** Phát hiện lỗi `priority` (các luật `CHECK` chạy trước luật tính toán).
    * **Điều chỉnh 2:** Sửa `priority` trong `CSTT_v2.json` (0 cho tính toán, -50 cho `CHECK`).
    * **Lần 3 (v3-v4):** Phát hiện lỗi `priority` lặp lại, lỗi logic `None` trong `_check_condition` và lỗi khởi tạo giá trị trong `evaluate`.
    * **Điều chỉnh 3-4:** Cập nhật `Bo_suy_dien_v4.py` và `CSTT_v4.json` lên phiên bản hoàn chỉnh.
* **Kết quả:** Hệ thống (`CSTT_v4.json` và `Bo_suy_dien_v4.py`) đã vượt qua các kịch bản kiểm thử phức tạp.
* **Demo:** `https://github.com/MinhHuy1507/military-service-expert-system`