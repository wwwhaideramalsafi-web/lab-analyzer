import time
from google import genai
import PIL.Image
import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محلل التقارير الطبية", layout="centered")

# كود CSS لمنع إظهار أيقونات التعبئة التلقائية والمربعات الصفراء من المتصفح
st.markdown(
    """
    <style>
    input[autocomplete="off"] {
        background-color: transparent !important;
    }
    ::-webkit-credentials-auto-fill-button {
        visibility: hidden !important;
        pointer-events: none !important;
        position: absolute !important;
        right: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("محلل التقارير الطبية الذكي 🩺")
st.markdown("---")

# اختيار اللغة وطوع التقرير
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("لغة التحليل / Output Language", ["العربية", "English"])
with col2:
    report_type = st.selectbox(
        "نوع التقرير", ["تحليل عام", "فحص دم CBC", "أشعة / مفراس", "وظائف كبد/كلى"]
    )

# جلب المفتاح تلقائياً من Secrets لمنع ظهور خانات إدخال السر
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error(
        "لم يتم العثور على API Key في Streamlit Secrets. يرجى إضافته في الإعدادات."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# رفع الصورة
uploaded_file = st.file_uploader(
    "رفع صورة التقرير الطبي أو التحليل المختبري", type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)

    # تصغير حجم أبعاد الصورة لتسريع المعالجة بشكل كبير
    max_size = (1024, 1024)
    image.thumbnail(max_size)

    st.image(image, caption="التقرير المرفوع", use_column_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner("جاري قراءة وتحليل النتائج بواسطة الذكاء الاصطناعي..."):
            prompt = f"قم بتحليل هذا التقرير الطبي ({report_type}) باللغة ({lang}). استخرج الأرقام والقيم غير الطبيعية واعرض النتائج في جدول واضح، واكتب ملخصاً بسيطاً وتنبيهات هامة."

            # محاولة الاتصال مع إعادة المحاولة التلقائية عند الضغط
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash", contents=[image, prompt]
                    )
                    st.success("تم التحليل بنجاح!")
                    st.write(response.text)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(2)
                    else:
                        st.error(
                            "السيرفر يشهد ضغطاً مؤقتاً حالياً، يرجى إعادة الضغط بعد ثوانٍ قليلة."
                        )

st.markdown("---")
st.warning(
    "تنبيه طبي: هذا التطبيق يستعين بالذكاء الاصطناعي للمساعدة في فهم وتلخيص نتائج التقارير الطبية فقط، ولا يعتبر بديلاً عن الاستشارة الطبية أو التشخيص المباشر من قبل الطبيب المختص."
)
