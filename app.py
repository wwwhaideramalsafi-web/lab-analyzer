import time
from google import genai
import PIL.Image
import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="محلل التقارير الطبية", layout="centered")

# منع أزرار التعبئة التلقائية والمربعات الصفراء
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

# اختيار اللغة ونوع التقرير
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("لغة التحليل / Output Language", ["العربية", "English"])
with col2:
    report_type = st.selectbox(
        "نوع التقرير", ["تحليل عام", "فحص دم CBC", "أشعة / مفراس", "وظائف كبد/كلى"]
    )

# جلب المفتاح من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input(
        "أدخل مفتاح Gemini API Key:", type="password", autocomplete="off"
    )

if not api_key:
    st.warning("يرجى التأكد من إضافة مفتاح الـ API في Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# خانة رفع الصورة
uploaded_file = st.file_uploader(
    "رفع صورة التقرير الطبي أو التحليل المختبري", type=["jpg", "jpeg", "png"]
)

user_custom_prompt = st.text_input(
    "أي ملاحظات أو أسئلة إضافية؟ (اختياري)",
    placeholder="مثلاً: ركز على النتائج غير الطبيعية...",
)

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    max_size = (1024, 1024)
    image.thumbnail(max_size)

    st.image(image, caption="التقرير المرفوع", use_container_width=True)

    if st.button("تحليل التقرير 🚀"):
        with st.spinner(
            "جاري قراءة وتحليل النتائج بذكاء واستقرار تام..."
        ):
            prompt = f"قم بتحليل هذا التقرير الطبي ({report_type}) باللغة ({lang}). استخرج الأرقام والقيم غير الطبيعية واعرض النتائج في جدول واضح مع ملخص بسيط."
            if user_custom_prompt:
                prompt += f" ملاحظات إضافية من المستخدم: {user_custom_prompt}"

            # قائمة النماذج للاستخدام بالتناوب التلقائي لضمان عدم توقف العرض
            models_to_try = ["gemini-3.8-flash", "gemini-2.5-flash"]
            success = False
            response = None

            for model_name in models_to_try:
                if success:
                    break
                for attempt in range(2):  # محاولتان لكل نموذج
                    try:
                        response = client.models.generate_content(
                            model=model_name, contents=[image, prompt]
                        )
                        success = True
                        break
                    except Exception as e:
                        time.sleep(1)  # انتظار قصير جداً والمحاولة مرة أخرى

            if success and response:
                st.success("تم التحليل بنجاح!")
                st.write(response.text)
            else:
                st.error(
                    "السيرفر يشهد ضغطاً حالياً، يرجى الانتظار ثوانٍ قليلة وإعادة الضغط."
                )

st.markdown("---")
st.warning(
    "تنبيه طبي: هذا التطبيق يستعين بالذكاء الاصطناعي للمساعدة في فهم وتلخيص نتائج التقارير الطبية فقط، ولا يعتبر بديلاً عن الاستشارة الطبية أو التشخيص المباشر من قبل الطبيب المختص."
)
