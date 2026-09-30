import streamlit as st
from google import genai
import PIL.Image

st.set_page_config(page_title="محلل التقارير الطبية", layout="centered")

st.title("محلل التقارير الطبية الذكي 🩺")
st.markdown("---")

# جلب المفتاح
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password")

if not api_key:
    st.warning("يرجى إدخال مفتاح الـ API.")
    st.stop()

# التهيئة بالطريقة الصحيحة للـ SDK الجديد
client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("ارفع صورة التقرير الطبي", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="التقرير المرفوع", use_container_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner("جاري التحليل..."):
            try:
                # الاستدعاء الصحيح للنموذج وإرسال المدخلات كقائمة (List)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, "قم بتحليل هذا التقرير الطبي بدقة واستخرج النتائج في جدول."]
                )
                st.success("تم التحليل بنجاح!")
                st.write(response.text)
            except Exception as e:
                # لنطبع الخطأ البرمجي الحقيقي بدلاً من رسالة "ضغط سيرفر" لنعرف السبب بدقة
                st.error(f"حدث خطأ في التنفيذ: {e}")
