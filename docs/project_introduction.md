# HỆ CHUYÊN GIA HỖ TRỢ TUYỂN CHỌN VÀ TƯ VẤN NGHĨA VỤ QUÂN SỰ

## CHƯƠNG I: MỞ ĐẦU

### 1. Giới thiệu tổng quan
Đề tài này trình bày kế hoạch phát triển một hệ chuyên gia dựa trên tri thức (*knowledge-based expert system*) với mục tiêu tự động hóa quá trình đánh giá và tư vấn các điều kiện tham gia nghĩa vụ quân sự tại Việt Nam. Hệ thống được thiết kế để hoạt động như một công cụ hỗ trợ đắc lực, cung cấp cho công dân và cán bộ tuyển quân những kết luận rõ ràng, nhất quán và có căn cứ pháp lý vững chắc, dựa trên các quy định hiện hành.

### 2. Bối cảnh và Lý do chọn đề tài
Nghĩa vụ quân sự là một trách nhiệm hiến định quan trọng. Tuy nhiên, quy trình tuyển chọn công dân nhập ngũ hiện nay là một quy trình hành chính phức tạp, đa giai đoạn, được quy định chặt chẽ bởi Luật Nghĩa vụ quân sự và các văn bản hướng dẫn liên quan. Quy trình này đòi hỏi sự đối chiếu thông tin cá nhân của công dân với một hệ thống tiêu chuẩn đa dạng về độ tuổi, sức khỏe, trình độ học vấn và hoàn cảnh gia đình.

Thực tiễn triển khai đang đối mặt với những thách thức sau:
* **Khối lượng công việc lớn:** Quy trình thủ công tạo áp lực lên bộ máy hành chính.
* **Tính nhất quán:** Sự phụ thuộc vào kinh nghiệm cá nhân của cán bộ tại từng địa phương có thể dẫn đến thiếu nhất quán trong việc áp dụng quy định.
* **Rào cản thông tin:** Công dân gặp khó khăn trong việc tiếp cận và tự diễn giải hệ thống văn bản pháp luật phức tạp, dẫn đến những hiểu lầm không đáng có về quyền và nghĩa vụ.

Dự án này ra đời trong bối cảnh chuyển đổi số trong hành chính công, ứng dụng AI để tối ưu hóa dịch vụ và tăng cường tính minh bạch.

### 3. Mục tiêu của đề tài
**Mục tiêu tổng quát:**
Thiết kế và phát triển hệ chuyên gia dựa trên luật có khả năng cung cấp các đánh giá về điều kiện nhập ngũ chính xác, minh bạch và có khả năng giải thích, góp phần nâng cao hiệu quả công tác tư vấn nghĩa vụ quân sự.

**Mục tiêu cụ thể:**
* Xác định rõ miền tri thức, nguồn tri thức và phạm vi đề tài.
* Thu thập, phân tích và phân loại tri thức từ các văn bản quy phạm pháp luật.
* Thiết kế các bài toán mẫu và kịch bản tư vấn mà hệ thống sẽ thực hiện.

### 4. Phạm vi và Đối tượng sử dụng
**Đối tượng sử dụng:**
* **Hội đồng Nghĩa vụ quân sự:** Sử dụng như công cụ sàng lọc sơ bộ được tiêu chuẩn hóa, giúp giảm tải công việc hành chính và giảm thiểu sai sót chủ quan.
* **Công dân:** Sử dụng như kênh thông tin minh bạch, giúp hiểu rõ nghĩa vụ và điều kiện của bản thân thông qua các giải thích có căn cứ pháp lý.

**Phạm vi chức năng:**
Hệ thống tập trung vào tư vấn và đánh giá điều kiện nhập ngũ cho công dân nam trong độ tuổi quy định dựa trên: độ tuổi, sức khỏe, trình độ học vấn, hoàn cảnh gia đình. Hệ thống **không** mở rộng sang tư vấn quy trình huấn luyện sau nhập ngũ.

### 5. Phương pháp thực hiện
* **Nghiên cứu văn bản:** Phân tích sâu Luật NVQS và các Thông tư của Bộ Quốc phòng.
* **Tra cứu tài liệu chuyên môn:** Sử dụng các từ khóa kỹ thuật (*expert system, rule-based system*) và chuyên môn (*luật nghĩa vụ quân sự, suy diễn tiến*) trên các cơ sở dữ liệu uy tín như IEEE Xplore, Google Scholar và Cổng thông tin điện tử Chính phủ.

---

## CHƯƠNG II: PHÂN TÍCH ỨNG DỤNG

### 1. Miền tri thức (Knowledge Domain)
Miền tri thức của hệ thống là lĩnh vực tuyển chọn và thực hiện nghĩa vụ quân sự tại Việt Nam. Tri thức được xây dựng dựa trên các tiêu chuẩn tuyển chọn, tạm hoãn và miễn nghĩa vụ (độ tuổi, sức khỏe, văn hóa, chính trị).

**Nguồn tri thức chính:**
* Luật Nghĩa vụ quân sự 2015 (số 78/2015/QH13).
* Thông tư 148/2018/TT-BQP.
* Thông tư 105/2023/TT-BQP (quy định về sức khỏe).
* Thông tư 68/2025/TT-BQP (sửa đổi, bổ sung).

### 2. Yêu cầu và Chức năng hệ thống
Hệ thống cần đảm bảo các chức năng cốt lõi sau:

* **Đưa ra kết luận:** Xác định công dân có thuộc diện gọi nhập ngũ hay không dựa trên thông tin đầu vào (tuổi, sức khỏe, học vấn, gia cảnh...).
* **Tra cứu tiêu chuẩn:** Cung cấp thông tin về các tiêu chuẩn hiện hành (Tuổi 18-27, Sức khỏe loại 1-3, Văn hóa, Chính trị...).
* **Cơ chế giải thích:** Cung cấp giải thích chi tiết, dễ hiểu kèm theo trích dẫn điều luật cụ thể cho từng kết luận.

**Ví dụ kịch bản tư vấn:**
> **Tình huống:** Nam 20 tuổi, đang học đại học, cận thị -9.0 diop hai mắt.
>
> **Hệ thống trả lời:**
> * *Tiêu chuẩn Độ tuổi:* **Đạt** (20 tuổi nằm trong độ tuổi quy định - Căn cứ Điều 30 Luật NVQS).
> * *Trường hợp Tạm hoãn:* **Thuộc diện tạm hoãn** (Đang học đại học - Căn cứ Điểm g, Khoản 1, Điều 41 Luật NVQS).
> * *Tiêu chuẩn Sức khỏe:* **Không đạt** (Cận thị > 1.5 diop - Căn cứ Thông tư 148 & 68/BQP).
>
> **KẾT LUẬN:** KHÔNG ĐỦ ĐIỀU KIỆN nhập ngũ.
> **Lý do:** Thuộc trường hợp tạm hoãn và không đủ tiêu chuẩn về sức khỏe.

### 3. Đặc trưng của Hệ cơ sở tri thức
Dự án mang các đặc trưng kỹ thuật và ứng dụng sau:

* **Lập luận Pháp lý Dựa trên Luật (Rule-Based Legal Reasoning):** Các quy định pháp luật được mô hình hóa thành các luật suy diễn hình thức dạng “IF-THEN”, đảm bảo tính chính xác và tuân thủ pháp luật.
* **Ứng dụng AI trong Hành chính công:** Giải quyết bài toán minh bạch hóa và tự động hóa dịch vụ công.
* **Tính hướng dẫn và giải thích (Explainability):** Hệ thống không chỉ đưa ra kết quả "Đạt/Không đạt" mà còn cung cấp lý do, giúp người dùng hiểu rõ bản chất vấn đề.
* **Tính ổn định:** Do luật pháp về nghĩa vụ quân sự có tính ổn định cao, ít thay đổi đột ngột, hệ thống có khả năng duy trì giá trị sử dụng dài hạn và dễ dàng cập nhật qua các bản sửa đổi luật.