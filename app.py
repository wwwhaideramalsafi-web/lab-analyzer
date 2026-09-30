import time
from google import genai
import PIL.Image
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="محلل التقارير الطبية الذكي", page_layout="centered"
)

st.title("محلل التقارير الطبية الذكي 🩺")
st.markdown("---")

# جلب المفتاح بأمان من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input(
        "أدخل مفتاح Gemini API Key:", type="password", autocomplete="off"
    )

if not api_key:
    st.warning("يرجى إدخال مفتاح الـ API للبدء.")
    st.stop()

# إنشاء العميل
client = genai.Client(api_key=api_key)

# خيارات لغة التحليل
lang = st.selectbox("لغة التحليل / Output Language", ["العربية", "English"])

# رفع الصورة
uploaded_file = st.file_uploader(
    "ارفع صورة التقرير الطبي أو التحليل", type=["jpg", "jpeg", "png"]
)

user_custom_prompt = st.text_input(
    "ملاحظات أو أسئلة إضافية (اختياري):", placeholder="مثلاً: ركز على الهيموجلوبين"
)

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)

    # تصغير الصورة لضمان السرعة الفائقة وعدم تعليق المعالجة
    image.thumbnail((800, 800))
    st.image(image, caption="التقرير المرفوع", use_container_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner("جاري قراءة وتحليل التقرير الطبي..."):
            prompt = f"قم بتحليل هذا التقرير الطبي باللغة ({lang}). استخرج النتائج والأرقام في جدول واضح مع ملخص وتوصيات بسيطة."
            if user_custom_prompt:
                prompt += f" ملاحظات إضافية: {user_custom_prompt}"

            try:
                # استخدام النموذج السريع والمستقر
                response = client.models.generate_content(
                    model="gemini-2.5-flash", contents=[image, prompt]
                )
                st.success("تم التحليل بنجاح!")
                st.write(response.text)
            except Exception as e:
                st.error(
                    "حدث ضغط مؤقت في السيرفر، يرجى إعادة المحاولة بعد ثوانٍ."
                )

st.markdown("---")
st.caption(
    "تنبيه طبي: هذا النظام أداة مساعدة ولا يُغني عن استشارة الطبيب المختص."
)
