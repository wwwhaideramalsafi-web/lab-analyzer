# -*- coding: utf-8 -*-
import streamlit as st
from google import genai
import PIL.Image

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="محلل التقارير الطبية الذكي", layout="centered")

st.title("محلل التقارير الطبية الذكي 🩺")
st.markdown("---")

# جلب المفتاح بأمان
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password", autocomplete="off")

if not api_key:
    st.error("يرجى إضافة مفتاح الـ API للبدء.")
    st.stop()

# تهيئة العميل
client = genai.Client(api_key=api_key)

# واجهة المستخدم بالعربية
uploaded_file = st.file_uploader("ارفع صورة التقرير الطبي أو التحليل", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="التقرير المرفوع", use_container_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner("جاري قراءة وتحليل التقرير..."):
            try:
                # البرومبت بالإنجليزية لضمان تحليل دقيق باللغة الإنجليزية بالكامل
                prompt = (
                    "Please analyze this medical report thoroughly in English. "
                    "Extract the values and findings, and present them in a clear, professional medical table, "
                    "followed by a brief summary and recommendations in English."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                st.success("تم التحليل بنجاح!")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ في التنفيذ: {e}")

st.markdown("---")
st.warning("تنبيه طبي: هذا التطبيق أداة مساعدة ولا يُغني عن التشخيص الطبي المباشر من قبل الطبيب المختص.")
