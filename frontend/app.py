"""
FILE NAME: app.py
DESCRIPTION: Frontend User Interface for Military Service Recruitment and Consultation Expert System
VERSION: 2.0
AUTHOR: CS217 Knowledge-Based System Team

KEY FEATURES:
- Provides citizen information input interface through 5 tabs:
  1. Basic Information (age, height, weight, BMI, education level)
  2. Health Standards (health classification, myopia, hyperopia, HIV/AIDS, drug addiction)
  3. Deferment Cases (health, education, family, labor)
  4. Exemption Cases (martyr's children, wounded soldiers, classified work)
  5. Voluntary Enlistment
- Automatic BMI calculation from height and weight
- Sends data to Backend API for inference
- Displays consultation results with legal basis and law citations
- Color-coded results: Green (Qualified), Red (Not Qualified), Yellow (Deferred/Exempt)

TECHNOLOGIES:
- Streamlit: Web app framework
- Requests: API calls to Backend
- Custom CSS: Interface customization with light blue color (#5dade2)

CONNECTION:
- Backend API URL: Default localhost:8000, configurable via BACKEND_URL environment variable
- Endpoint: POST /consult with citizen information payload
"""

import streamlit as st
import requests
import json
import os

# Page configuration
st.set_page_config(
    page_title="Hệ chuyên gia hỗ trợ tuyển chọn và tư vấn Nghĩa vụ Quân sự",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URL của Backend API
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# CSS tùy chỉnh - Thiết lập giao diện với màu xanh biển nhạt
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        padding: 20px 0;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
    }
    
    /* Customize button colors to light blue (#5dade2) */
    button[kind="primary"],
    button[kind="primaryFormSubmit"],
    .stButton > button,
    [data-testid="stFormSubmitButton"] > button,
    div[data-testid="stFormSubmitButton"] button {
        background-color: #5dade2 !important;
        color: white !important;
        border: none !important;
    }
    
    button[kind="primary"]:hover,
    button[kind="primaryFormSubmit"]:hover,
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #3498db !important;
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3) !important;
    }
    
    /* Customize checkbox colors to light blue - Override default settings */
    .stCheckbox input[type="checkbox"]:checked,
    input[type="checkbox"]:checked,
    div[role="checkbox"][aria-checked="true"],
    div[data-baseweb="checkbox"][aria-checked="true"],
    span[data-baseweb="checkbox"] input:checked ~ div {
        background-color: #5dade2 !important;
        border-color: #5dade2 !important;
        accent-color: #5dade2 !important;
    }
    
    /* Override Streamlit default primary color (red/orange) */
    :root {
        --primary-color: #5dade2 !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>HỆ CHUYÊN GIA HỖ TRỢ TUYỂN CHỌN VÀ TƯ VẤN<br/>NGHĨA VỤ QUÂN SỰ</h1>", unsafe_allow_html=True)
st.markdown("---")

# Function to check Backend API connection
def check_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=2)
        return response.status_code == 200
    except:
        return False

if not check_backend():
    st.error("⚠️ Không thể kết nối đến Backend API.")
    st.stop()

# Initialize session state to store consultation results
if 'result' not in st.session_state:
    st.session_state.result = None

# Create input form with 5 functional tabs
with st.form("citizen_form"):
    st.subheader("📋 Nhập thông tin công dân")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ Thông tin Cơ bản",
        "2️⃣ Tiêu chuẩn Sức khỏe", 
        "3️⃣ Trường hợp Tạm hoãn",
        "4️⃣ Trường hợp Miễn",
        "5️⃣ Tình nguyện"
    ])
    
    # TAB 1: Basic Information (age, height, weight, BMI, education level)
    with tab1:
        st.markdown("###  Thông tin cơ bản")
        col1, col2 = st.columns(2)
        
        with col1:
            tuoi = st.number_input("Tuổi", 10, 35, 20)
            chieu_cao = st.number_input("Chiều cao (cm)", 140, 220, 170)
            can_nang = st.number_input("Cân nặng (kg)", 30, 150, 65)
            
            # Automatically calculate BMI from weight and height
            chi_so_BMI = can_nang / ((chieu_cao * 0.01) ** 2)
            
            st.metric(
                label="Chỉ số BMI",
                value=f"{chi_so_BMI:.2f}",
                delta_color="off",
                help="Chỉ số khối cơ thể (BMI) được tính bằng cân nặng (kg) chia cho bình phương chiều cao (m).\nSẽ được tính toán và hiển thị khi bạn nhấn 'Tư vấn'."
            )
            
        with col2:
            trinh_do_van_hoa = st.number_input(
                "Trình độ văn hóa (lớp/12)",
                min_value=0,
                max_value=12,
                value=12,
                step=1,
                help="Trình độ văn hóa tính theo hệ 12/12. Ví dụ: Lớp 5 → nhập 5, Lớp 12 → nhập 12. Dù tốt nghiệp Đại học hay Cao đẳng vẫn được tính là 12/12."
            )
            duoc_tam_hoan_vi_hoc = st.checkbox(
                "Từng được tạm hoãn vì học Đại học / Cao đẳng",
                help="Chọn mục này nếu bạn đã từng nhận giấy tạm hoãn gọi nhập ngũ trong thời gian theo học tại một cơ sở giáo dục Cao đẳng hoặc Đại học. Thông tin này rất quan trọng, vì nó xác định độ tuổi gọi nhập ngũ của bạn được kéo dài đến hết 27 tuổi (thay vì 25 tuổi)."
            )
            dia_phuong_kho_khan_giao_quan = st.checkbox(
                "Địa phương khó khăn trong việc giao quân",
                help="Theo quy định chung, công dân phải có trình độ văn hóa từ lớp 8 trở lên. Tuy nhiên, một số địa phương đặc biệt khó khăn không tuyển đủ chỉ tiêu sẽ được phép tuyển chọn công dân có trình độ lớp 7. Hãy chọn mục này nếu địa phương của bạn có thông báo áp dụng quy định này."
            )
            vung_dac_biet_kho_khan = st.checkbox(
                "Thuộc vùng đặc biệt khó khăn",
                help="Chọn mục này nếu bạn đang cư trú tại các xã thuộc vùng sâu, vùng xa, hoặc vùng có điều kiện kinh tế - xã hội (KTXH) đặc biệt khó khăn. Công dân ở các vùng này được ưu tiên xét tuyển với trình độ văn hóa từ cấp tiểu học (đã tốt nghiệp lớp 5)."
            )
            dan_toc_thieu_so_duoi_10000 = st.checkbox(
                "Thuộc dân tộc thiểu số dưới 10000 người",
                help="Chọn mục này nếu bạn thuộc các dân tộc thiểu số có số dân dưới 10.000 người (ví dụ: Ơ Đu, Brâu, Rơ Măm, Pu Péo, Si La...). Công dân thuộc nhóm này cũng được ưu tiên xét tuyển với trình độ văn hóa từ cấp tiểu học (đã tốt nghiệp lớp 5)."
            )


    # TAB 2: Health Standards (myopia, hyperopia, HIV/AIDS, drug addiction, BMI)
    with tab2:
        st.markdown("###  Tiêu chuẩn Sức khỏe")
        st.info("ℹ️ **Lưu ý:** Hệ thống sẽ tự động đánh giá sức khỏe dựa trên các tiêu chí cụ thể bên dưới.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Hidden field - system will auto-determine health classification
            # loai_suc_khoe is removed from user input, system evaluates based on criteria
            do_can_thi = st.number_input(
                "Độ cận thị (Diop)", 
                0.0, 20.0, 0.0, 0.25,
                help="Độ cận thị của mắt. Quy định: Cận thị > 1.5 diop sẽ không đạt tiêu chuẩn."
            )
            
        with col2:
            vien_thi = st.checkbox(
                "Bị viễn thị",
                help="Viễn thị ở mọi mức độ đều không đạt tiêu chuẩn."
            )
            nghien_ma_tuy = st.checkbox(
                "Nghiện ma túy",
                help="Công dân nghiện ma túy không được gọi nhập ngũ."
            )
            nhiem_HIV_AIDS = st.checkbox(
                "Nhiễm HIV/AIDS",
                help="Công dân nhiễm HIV/AIDS không được gọi nhập ngũ."
            )
    
    # TAB 3: Deferment Cases (health, education, family, labor)
    with tab3:
        st.markdown("###  Trường hợp Tạm hoãn")
        chua_du_suc_khoe = st.checkbox(
            "Chưa đủ sức khỏe phục vụ (theo kết luận của Hội đồng Khám sức khỏe)",
            value=False,
            help="Mặc định hệ thống coi là 'Đủ sức khỏe'. Chỉ TICK vào mục này nếu Hội đồng Khám sức khỏe kết luận bạn CHƯA ĐỦ sức khỏe phục vụ."
        )
        # Reversed logic: checkbox is "Not sufficient", API variable is "Sufficient" = NOT checkbox
        du_suc_khoe_phuc_vu = not chua_du_suc_khoe
        dang_hoc_giao_duc_pho_thong = st.checkbox("Đang học phổ thông")
        dang_hoc_dh_cd_chinh_quy = st.checkbox("Đang học Đại học / Cao đẳng")
        lao_dong_duy_nhat = st.checkbox(
            "Là lao động duy nhất",
            help="Chọn mục này nếu bạn là người lao động duy nhất, phải trực tiếp nuôi dưỡng thân nhân (như cha mẹ già, con nhỏ...) không còn khả năng lao động hoặc chưa đến tuổi lao động."
        )
        gia_dinh_thiet_hai_nang_khong_con_ld_khac = st.checkbox(
            "Gia đình thiệt hại nặng do thiên tai, không còn lao động khác",
            help="Chọn mục này nếu gia đình bạn bị thiệt hại nặng về người và tài sản do tai nạn, thiên tai, dịch bệnh nguy hiểm gây ra và được Ủy ban nhân dân cấp xã xác nhận là không còn người lao động nào khác."
        )
        co_anh_chi_em_dang_phuc_vu_tai_ngu = st.checkbox(
            "Có anh/chị/em đang phục vụ tại ngũ",
            help="Chọn mục này nếu bạn có anh, chị, hoặc em ruột đang là hạ sĩ quan, binh sĩ phục vụ tại ngũ (trong Quân đội) HOẶC đang thực hiện nghĩa vụ tham gia Công an nhân dân."
        )
        la_con_benh_binh_cd_61_80 = st.checkbox(
            "Con của bệnh binh, người nhiễm chất độc da cam suy giảm khả năng lao động (61% - 80%)",
            help="Là con của bệnh binh hoặc người nhiễm chất độc da cam có mức suy giảm khả năng lao động từ 61% đến 80%."
        )
        thuoc_dien_di_dan_3_nam_dau = st.checkbox(
            "Thuộc diện di dân trong 03 năm đầu",
            help="Thuộc diện di dân, giãn dân trong 03 năm đầu đến các xã đặc biệt khó khăn theo dự án phát triển kinh tế - xã hội của Nhà nước."
        )
        
        
    
    # TAB 4: Exemption Cases (martyr's children, wounded soldiers, classified work)
    with tab4:
        st.markdown("###  Trường hợp Miễn")
        la_con_cua_liet_si = st.checkbox(
            "Con liệt sĩ",
            help="Là con của liệt sĩ hy sinh vì sự nghiệp cách mạng."
        )
        la_con_cua_thuong_binh_hang_mot = st.checkbox(
            "Con thương binh hạng 1",
            help="Là con của thương binh hạng 1, bị thương trong chiến đấu và được xếp hạng cao nhất."
        )
        la_anh_hoac_em_trai_cua_liet_si = st.checkbox(
            "Anh/em của liệt sĩ",
            help="Là anh ruột hoặc em trai ruột của liệt sĩ."
        )
        la_mot_con_cua_thuong_binh_hang_hai = st.checkbox(
            "Con duy nhất của thương binh hạng 2",
            help="Pháp luật quy định 'Một con' của thương binh hạng 2 được miễn. Chọn mục này nếu bạn là người con (duy nhất) trong gia đình xin hưởng quyền miễn này."
        )
        la_mot_con_benh_binh_cd_81_tro_len = st.checkbox(
            "Con duy nhất của bệnh binh suy giảm khả năng lao động (81%+)",
            help="Pháp luật quy định 'Một con' của bệnh binh (suy giảm 81%+) được miễn. Chọn mục này nếu bạn là người con (duy nhất) trong gia đình xin hưởng quyền miễn này."
        )
        la_mot_con_cdac_cd_81_tro_len = st.checkbox(
            "Con duy nhất của người nhiễm chất độc da cam suy giảm khả năng lao động (81%+)",
            help="Pháp luật quy định 'Một con' của người nhiễm chất độc da cam (suy giảm 81%+) được miễn. Chọn mục này nếu bạn là người con (duy nhất) trong gia đình xin hưởng quyền miễn này."
        )
        lam_cong_tac_co_yeu_khong_phai_quan_nhan = st.checkbox(
            "Làm công tác cơ yếu (không phải quân nhân, CAND)",
            help="Đang làm công tác mật mã, cơ yếu mà không phải là quân nhân hoặc công an nhân dân."
        )
        thoi_gian_cong_tac_vung_dbkk_thang = st.number_input(
            "Số tháng công tác tại vùng đặc biệt khó khăn (Là cán bộ, công chức, viên chức, thanh niên xung phong)",
            min_value=0,
            value=0,
            step=1,
            help="Nếu bạn Là cán bộ, công chức, viên chức, thanh niên xung phong công tác tại vùng kinh tế - xã hội đặc biệt khó khăn, hãy nhập tổng số tháng đã công tác. Hệ thống sẽ tự động xét Tạm hoãn (dưới 24 tháng) hoặc Miễn (từ 24 tháng trở lên)."
        )

    
    # TAB 5: Voluntary Enlistment
    with tab5:
        st.markdown("###  Tình nguyện")
        tinh_nguyen_nhap_ngu = st.checkbox(
            "Tôi tình nguyện nhập ngũ",
            help="Khi bạn chọn mục này, bạn sẽ được xem xét ưu tiên trong quá trình tuyển chọn nghĩa vụ quân sự." \
            " Bạn vẫn phải đợi kết luận chính xác từ hội đồng tuyển chọn nghĩa vụ quân sự."\
            " Khi bạn chọn mục này, hệ thống sẽ mặc định là bạn đủ điều kiện tham gia nghĩa vụ quân sự."\
        )

    # Submit button to send data to Backend
    st.markdown("---")
    submitted = st.form_submit_button("🔍 Tư vấn", use_container_width=True, type="primary")

# Handle when user clicks the Consult button
if submitted:
    # Prepare data to send to Backend API
    payload = {
        "tuoi": tuoi,
        "duoc_tam_hoan_vi_hoc": duoc_tam_hoan_vi_hoc,
        # "loai_suc_khoe" removed - system auto-determines based on health criteria
        "do_can_thi": do_can_thi,
        "vien_thi": vien_thi,
        "nghien_ma_tuy": nghien_ma_tuy,
        "nhiem_HIV_AIDS": nhiem_HIV_AIDS,
        "chi_so_BMI": chi_so_BMI,
        "trinh_do_van_hoa": trinh_do_van_hoa,
        "dia_phuong_kho_khan_giao_quan": dia_phuong_kho_khan_giao_quan,
        "vung_dac_biet_kho_khan": vung_dac_biet_kho_khan,
        "dan_toc_thieu_so_duoi_10000": dan_toc_thieu_so_duoi_10000,
        "du_suc_khoe_phuc_vu": du_suc_khoe_phuc_vu,
        "lao_dong_duy_nhat": lao_dong_duy_nhat,
        "gia_dinh_thiet_hai_nang_khong_con_ld_khac": gia_dinh_thiet_hai_nang_khong_con_ld_khac,
        "la_con_benh_binh_cd_61_80": la_con_benh_binh_cd_61_80,
        "co_anh_chi_em_dang_phuc_vu_tai_ngu": co_anh_chi_em_dang_phuc_vu_tai_ngu,
        "thuoc_dien_di_dan_3_nam_dau": thuoc_dien_di_dan_3_nam_dau,
        "dang_hoc_giao_duc_pho_thong": dang_hoc_giao_duc_pho_thong,
        "dang_hoc_dh_cd_chinh_quy": dang_hoc_dh_cd_chinh_quy,
        "la_con_cua_liet_si": la_con_cua_liet_si,
        "la_con_cua_thuong_binh_hang_mot": la_con_cua_thuong_binh_hang_mot,
        "la_anh_hoac_em_trai_cua_liet_si": la_anh_hoac_em_trai_cua_liet_si,
        "la_mot_con_cua_thuong_binh_hang_hai": la_mot_con_cua_thuong_binh_hang_hai,
        "la_mot_con_benh_binh_cd_81_tro_len": la_mot_con_benh_binh_cd_81_tro_len,
        "la_mot_con_cdac_cd_81_tro_len": la_mot_con_cdac_cd_81_tro_len,
        "lam_cong_tac_co_yeu_khong_phai_quan_nhan": lam_cong_tac_co_yeu_khong_phai_quan_nhan,
        "thoi_gian_cong_tac_vung_dbkk_thang": thoi_gian_cong_tac_vung_dbkk_thang,
        "tinh_nguyen_nhap_ngu": tinh_nguyen_nhap_ngu
    }
    try:
        response = requests.post(f"{BACKEND_URL}/consult", json=payload)
        if response.status_code == 200:
            st.session_state.result = response.json()
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")

# Display consultation results
if st.session_state.result:
    result = st.session_state.result
    ket_luan = result.get("ket_luan", "")
    
    # Determine display color based on conclusion
    if "ĐỦ ĐIỀU KIỆN" in ket_luan and "KHÔNG" not in ket_luan:
        box_class, icon = "success-box", "✅"
    elif "KHÔNG ĐỦ ĐIỀU KIỆN" in ket_luan:
        box_class, icon = "danger-box", "❌"
    else:
        box_class, icon = "warning-box", "⚠️"
    
    st.markdown(f"""
        <div class='result-box {box_class}'>
            <h2>{icon} KẾT LUẬN</h2>
            <h3>{ket_luan}</h3>
            <p><strong>Giải thích:</strong> {result.get("giai_thich", "")}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Display detailed legal basis and law citations
    if "trace" in result:
        with st.expander("📖 Chi tiết", expanded=True):
            rules_by_category = {
                "TUOI": [], "SUC_KHOE": [], "VAN_HOA": [],
                "TAM_HOAN": [], "MIEN": [], "TINH_NGUYEN": []
            }
            
            # Iterate through rules and categorize by ID
            for rule in result["trace"]:
                rule_id = rule.get("id", "")
                if "R_TUOI" in rule_id:
                    rules_by_category["TUOI"].append(rule)
                elif "R_SK" in rule_id:
                    rules_by_category["SUC_KHOE"].append(rule)
                elif "R_VH" in rule_id:
                    rules_by_category["VAN_HOA"].append(rule)
                elif "R_TAM_HOAN" in rule_id:
                    rules_by_category["TAM_HOAN"].append(rule)
                elif "R_MIEN" in rule_id:
                    rules_by_category["MIEN"].append(rule)
            
            for title, rules in [("Tuổi", rules_by_category["TUOI"]),
                                ("Sức khỏe", rules_by_category["SUC_KHOE"]),
                                ("Văn hóa", rules_by_category["VAN_HOA"]),
                                ("Miễn", rules_by_category["MIEN"]),
                                ("Tạm hoãn", rules_by_category["TAM_HOAN"])]:
                if rules:
                    st.markdown(f"#### {title}")
                    for rule in rules:
                        # Display legal basis of the rule
                        citation = rule.get('citation', 'Không có thông tin')
                        st.markdown(f"**📜 Căn cứ pháp lý:** {citation}")
                        
                        # Display law citation with readable formatting
                        quote = rule.get('quote', 'Không có trích dẫn')
                        # Convert newline characters and format points a), b), c)
                        quote_formatted = quote.replace("\\n", "\n")
                        import re
                        quote_formatted = re.sub(r'([.;])\s*([a-z]\))', r'\1\n\n\2', quote_formatted)
                        st.info(f"💬 **Trích dẫn:**\n\n{quote_formatted}")
                        
                        # Extract detailed conclusion from actions (LY_DO_*_DETAIL)
                        ket_luan_chi_tiet = ""
                        for action in rule.get('actions', []):
                            if action.get('fact', '').endswith('_DETAIL'):
                                ket_luan_chi_tiet = action.get('value', '')
                                break
                        
                        # If no _DETAIL found, use description as conclusion
                        if not ket_luan_chi_tiet:
                            ket_luan_chi_tiet = rule.get('description', '')
                        
                        # Display conclusion with corresponding color (Red/Green/Yellow)
                        if ket_luan_chi_tiet.startswith("Không"):
                            st.error(f"❌ **Kết luận:** {ket_luan_chi_tiet}")
                        elif ket_luan_chi_tiet.startswith("Đạt"):
                            st.success(f"✅ **Kết luận:** {ket_luan_chi_tiet}")
                        else:
                            st.warning(f"⚠️ **Kết luận:** {ket_luan_chi_tiet}")
                        
                    st.markdown("---")
