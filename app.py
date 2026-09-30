import streamlit as st
from google import genai
import PIL.Image

st.set_page_config(page_title="محلل التقارير الطبية", layout="centered")

st.title("محلل التقارير الطبية الذكي 🩺")
st.markdown("---")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("يرجى إضافة مفتاح GEMINI_API_KEY في إعدادات Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("ارفع صورة التقرير الطبي أو التحليل", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="التقرير المرفوع", use_container_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner("جاري قراءة وتحليل التقرير..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, "قم بتحليل هذا التقرير الطبي واستخرج النتائج في جدول واضح."]
                )
                st.success("تم التحليل بنجاح!")
                st.write(response.text)
            except Exception as e:
                st.error("حدث خطأ في الاتصال، يرجى المحاولة مرة أخرى.")
