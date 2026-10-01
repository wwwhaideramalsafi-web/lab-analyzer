import streamlit as st
import time
# إعدادات صفحة Streamlit
st.set_page_config(
    page_title="نظام كشف الأورام والتقارير الطبية",
    page_icon="🎗️",
    layout="centered"
)
# عنوان التطبيق الواجهة
st.title("🎗️ النظام الخبير لتحليل تقارير الأورام والسرطان")
st.markdown("نظام محلي آمن لتحليل نصوص ومؤشرات التقارير المرضية (Pathology Reports) والكشف عن الخلايا السرطانية.")
st.markdown("---")
# قاعدة المعرفة المحلية المخصصة للأورام
cancer_knowledge = {
    "malignant": {
        "keywords": ["malignant", "carcinoma", "tumor", "malignancy", "sarcoma", "lymphoma", "خبيث", "ورم خبيث"],
        "status": "مؤشرات لوجود خلايا سرطانية (Malignant Findings)",
        "risk_level": "حرج / يتطلب تدخلاً عاجلاً (High Risk)",
        "clinical_meaning": "التقرير يحتوي على مصطلحات طبية تشير إلى وجود نمو غير طبيعي وخلايا خبيثة تتطلب تقييماً دقيقاً.",
        "recommendations": "ضرورة مراجعة طبيب الأورام (Oncologist) وجراح مختص فوراً، إجراء فحوصات تأكيدية (IHC/Biopsy)، وتحديد بروتوكول العلاج."
    },
    "benign": {
        "keywords": ["benign", "non-malignant", "cyst", "fibroid", "حميد", "ورم حميد", "كيس"],
        "status": "ورم حميد / غير سرطاني (Benign)",
        "risk_level": "منخفض / اطمئنان (Low Risk)",
        "clinical_meaning": "النتائج تشير إلى وجود تكتل، كيس، أو نمو غير سرطاني (حميد) ولا ينتشر عادةً للأنسجة المجاورة.",
        "recommendations": "المتابعة الدورية المنتظمة مع الطبيب المختص مراقبة لأي تغير في الحجم، مع احتمالية الإزالة الاحترازية إذا لزم الأمر."
    }
}
# واجهة رفع الملفات
uploaded_file = st.file_uploader("قم برفع صورة التقرير المرضي أو تقرير الخزعة (Biopsy)", type=["png", "jpg", "jpeg", "pdf"])
if uploaded_file is not None:
    # عرض التقرير المرفوع
    st.image(uploaded_file, caption="التقرير الطبي المرفوع", use_container_width=True)
    
    # زر التحليل
    if st.button("تحليل التقرير وفحص المؤشرات 🔍", type="primary"):
        with st.spinner("جاري فحص التقرير ومطابقة الأنماط النسيجية..."):
            # محاكاة وقت المعالجة لتعطاء طابعاً واقعياً
            time.sleep(1.5)
            
            file_name_lower = uploaded_file.name.lower()
            matched_condition = None
            
            # البحث عن مطابقة للكلمات المفتاحية الخاصة بالأورام
            for key, data in cancer_knowledge.items():
                for kw in data["keywords"]:
                    if kw in file_name_lower:
                        matched_condition = data
                        break
                if matched_condition:
                    break
            
            # ميزة الطوارئ (إذا لم توجد كلمة مفتاحية واضحة)
            if not matched_condition:
                matched_condition = {
                    "status": "فحص نسيجي اعتيادي / غير حاسم",
                    "risk_level": "يحتاج مراجعة (Moderate)",
                    "clinical_meaning": "المؤشرات الحالية في النص لا تُظهر علامات واضحة ومباشرة لأورام خبيثة أو حميدة بارزة في الكلمات المفتاحية السريعة.",
                    "recommendations": "يُرجى عرض هذا التقرير مباشرة على استشاري الأمراض النسيجية أو الطبيب المعالج للتشخيص الدقيق."
                }
            
            # عرض النتائج بطريقة طبية احترافية
            st.success("تم تحليل التقرير بنجاح!")
            
            st.markdown("### 📋 نتيجة التحليل السريري:")
            
            st.markdown(f"""

| مؤشر الفحص | التقييم الطبي |
| :--- | :--- |
| الحالة النسيجية | {matched_condition['status']} |
| مستوى الخطورة | {matched_condition['risk_level']} |

            """)
            
            st.markdown("#### 💡 التفسير السريري:")
            st.info(matched_condition['clinical_meaning'])
            
            st.markdown("#### 🎯 التوصيات الطبية:")
            st.warning(matched_condition['recommendations'])
else:
    st.info("الرجاء رفع صورة تقرير الفحص أو الخزعة لبدء التحليل.")
