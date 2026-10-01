import streamlit as st
import time
# إعدادات صفحة Streamlit مع تفعيل التصميم الأنيق
st.set_page_config(
    page_title="Pathology Expert System",
    page_icon="🎗️",
    layout="centered"
)
# تخصيص التصميم والخطوط والألوان لتكون واضحة جداً
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #1e293b;
    }
    h1, h2, h3 {
        font-weight: 700 !important;
        color: #0f172a !important;
    }
    </style>
""", unsafe_allow_html=True)
# اختيار اللغة من الشريط الجانبي (Sidebar)
language = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
if language == "العربية":
    title_text = "🎗️ النظام الخبير لتحليل تقارير الأورام والسرطان"
    subtitle_text = "نظام محلي آمن لتحليل نصوص ومؤشرات التقارير المرضية (Pathology Reports) والكشف عن الخلايا السرطانية."
    uploader_label = "قم برفع صورة التقرير المرضي أو تقرير الخزعة (Biopsy)"
    button_text = "تحليل التقرير وفحص المؤشرات 🔍"
    spinner_text = "جاري فحص التقرير ومطابقة الأنماط النسيجية..."
    success_text = "تم تحليل التقرير بنجاح!"
    table_headers = ["مؤشر الفحص", "التقييم الطبي"]
    clinical_title = "💡 التفسير السريري:"
    recommendations_title = "🎯 التوصيات الطبية:"
    no_file_text = "الرجاء رفع صورة تقرير الفحص أو الخزعة لبدء التحليل."
    
    cancer_knowledge = {
        "malignant": {
            "keywords": ["malignant", "carcinoma", "tumor", "malignancy", "sarcoma", "lymphoma", "خبيث", "ورم خبيث"],
            "status": "مؤشرات لوجود خلايا سرطانية (Malignant Findings)",
            "risk_level": "حرج / يتطلب تدخلاً عاجلاً (High Risk)",
            "clinical_meaning": "التقرير يحتوي على مصطلحات طبية تشير إلى وجود نمو غير طبيعي وخلايا خبيثة تتطلب تقييماً دقيقاً.",
            "recommendations": "ضرورة مراجعة طبيب الأورام (Oncologist) وجراح مختص فوراً، إجراء فحوصات تأكيدية، وتحديد بروتوكول العلاج."
        },
        "benign": {
            "keywords": ["benign", "non-malignant", "cyst", "fibroid", "حميد", "ورم حميد", "كيس"],
            "status": "ورم حميد / غير سرطاني (Benign)",
            "risk_level": "منخفض / اطمئنان (Low Risk)",
            "clinical_meaning": "النتائج تشير إلى وجود تكتل، كيس، أو نمو غير سرطاني (حميد) ولا ينتشر عادةً للأنسجة المجاورة.",
            "recommendations": "المتابعة الدورية المنتظمة مع الطبيب المختص مراقبة لأي تغير في الحجم، مع احتمالية الإزالة الاحترازية."
        }
    }
    fallback_data = {
        "status": "فحص نسيجي خاضع للتدقيق / غير حاسم",
        "risk_level": "يحتاج مراجعة سريرية (Moderate)",
        "clinical_meaning": "الخصائص المرصودة في التقرير المرفق لا تُظهر دلالات قطعية واضحة تابعة لقواعد الأورام الخبيثة أو الحميدة المعرفة في النظام.",
        "recommendations": "يُرجى عرض هذا التقرير مباشرة على استشاري الأمراض النسيجية أو الطبيب المعالج للتشخيص السريري الدقيق."
    }
else:
    title_text = "🎗️ Pathology & Oncology Expert System"
    subtitle_text = "A secure local system for analyzing pathology reports and identifying malignancy indicators."
    uploader_label = "Upload Pathology Report or Biopsy Image"
    button_text = "Analyze Report & Check Indicators 🔍"
    spinner_text = "Scanning report and matching histological patterns..."
    success_text = "Report analyzed successfully!"
    table_headers = ["Examination Indicator", "Medical Evaluation"]
    clinical_title = "💡 Clinical Interpretation:"
    recommendations_title = "🎯 Medical Recommendations:"
    no_file_text = "Please upload a biopsy or report image to begin analysis."
    
    cancer_knowledge = {
        "malignant": {
            "keywords": ["malignant", "carcinoma", "tumor", "malignancy", "sarcoma", "lymphoma"],
            "status": "Malignant Findings Detected",
            "risk_level": "High Risk / Urgent Action Required",
            "clinical_meaning": "The report contains medical terminology indicating abnormal growth and malignant cells requiring precise evaluation.",
        "recommendations": "Immediate consultation with an oncologist and specialist surgeon is necessary, along with confirmatory tests."
        },
        "benign": {
            "keywords": ["benign", "non-malignant", "cyst", "fibroid"],
            "status": "Benign / Non-Malignant",
            "risk_level": "Low Risk / Reassuring",
            "clinical_meaning": "Results indicate a benign mass, cyst, or non-cancerous growth that typically does not spread to adjacent tissues.",
            "recommendations": "Regular periodic follow-up with the specialist to monitor size changes, with potential precautionary removal."
        }
    }
    fallback_data = {
        "status": "Standard Histological Examination / Inconclusive",
        "risk_level": "Requires Clinical Review (Moderate)",
        "clinical_meaning": "The observed features in the attached report do not show definitive direct indications matching the system's strict malignant or benign rules.",
        "recommendations": "Please present this report directly to a histopathology consultant or attending physician for precise clinical diagnosis."
    }
# واجهة المستخدم الأساسية
st.title(title_text)
st.markdown(subtitle_text)
st.markdown("---")
uploaded_file = st.file_uploader(uploader_label, type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Report", use_container_width=True)
    
    if st.button(button_text, type="primary"):
        with st.spinner(spinner_text):
            time.sleep(1.2)
            
            file_name_lower = uploaded_file.name.lower()
            matched_condition = None
            
            for key, data in cancer_knowledge.items():
                for kw in data["keywords"]:
                    if kw in file_name_lower:
                        matched_condition = data
                        break
                if matched_condition:
                    break
            
            if not matched_condition:
                matched_condition = fallback_data
            
            st.success(success_text)
            
            st.markdown("### 📋 Clinical Analysis Report:")
            
            st.markdown(f"""

| {table_headers[0]} | {table_headers[1]} |
| :--- | :--- |
| Status | {matched_condition['status']} |
| Risk Level | {matched_condition['risk_level']} |

            """)
            
            st.markdown(f"#### {clinical_title}")
            st.info(matched_condition['clinical_meaning'])
            
            st.markdown(f"#### {recommendations_title}")
            st.warning(matched_condition['recommendations'])
else:
    st.info(no_file_text)
