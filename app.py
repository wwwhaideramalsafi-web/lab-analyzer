import streamlit as st
from google import genai
import PIL.Image

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="محلل التقارير الطبية الذكي", layout="centered")

st.title("محلل التقارير الطبية الذكي 🩺")
st.markdown("---")

# جلب المفتاح بأمان من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    api_key = st.text_input("أدخل مفتاح Gemini API Key:", type="password", autocomplete="off")

if not api_key:
    st.error("يرجى إضافة مفتاح GEMINI_API_KEY في إعدادات Streamlit Secrets أو إدخاله أعلاه.")
    st.stop()

# تهيئة العميل
client = genai.Client(api_key=api_key)

# خيارات لغة التحليل ونوع التقرير
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("لغة التحليل / Output Language", ["العربية", "English"])
with col2:
    report_type = st.selectbox("نوع التقرير", ["تحليل عام", "فحص دم CBC", "أشعة / مفراس", "وظائف كبد/كلى"])

# رفع الصورة
uploaded_file = st.file_uploader("ارفع صورة التقرير الطبي أو التحليل المختبري", type=["jpg", "jpeg", "png"])

# ملاحظات إضافية اختيارية
user_custom_prompt = st.text_input("ملاحظات أو أسئلة إضافية (اختياري):", placeholder="مثلاً: ركز على الهيموجلوبين والنتائج غير الطبيعية")

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    
    # تصغير أبعاد الصورة لضمان السرعة الفائقة وعدم تعليق المعالجة
    image.thumbnail((800, 800))
    st.image(image, caption="التقرير المرفوع", use_container_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner("جاري قراءة وتحليل النتائج بواسطة الذكاء الاصطناعي..."):
            prompt = f"قم بتحليل هذا التقرير الطبي ({report_type}) باللغة ({lang}). استخرج الأرقام والقيم غير الطبيعية واعرض النتائج في جدول واضح مع ملخص وتوصيات بسيطة."
            if user_custom_prompt:
                prompt += f" ملاحظات إضافية من المستخدم: {user_custom_prompt}"

            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[image, prompt]
                )
                st.success("تم التحليل بنجاح!")
                st.write(response.text)
            except Exception as e:
                st.error("حدث ضغط مؤقت في السيرفر، يرجى إعادة المحاولة بعد ثوانٍ.")

st.markdown("---")
st.warning("تنبيه طبي: هذا التطبيق يستعين بالذكاء الاصطناعي للمساعدة في فهم وتلخيص نتائج التقارير الطبية فقط، ولا يعتبر بديلاً عن الاستشارة الطبية أو التشخيص المباشر من قبل الطبيب المختص.")
