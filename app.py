import streamlit as st
from google import genai
from PIL import Image

# إعدادات الصفحة
st.set_page_config(
    page_title="محلل التقارير والتحاليل الطبية", 
    page_icon="🔬", 
    layout="centered"
)

st.title("🔬 برنامج قراءة وتحليل التقارير الطبية")

st.markdown("---")

# خيارات اللغة ونوع التقرير
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("لغة التحليل / Output Language", ["العربية", "English"])
with col2:
    report_type = st.selectbox(
        "نوع التقرير الطبي:",
        [
            "تحاليل دم وكيمياء (CBC, Biochemistry, Hormones)",
            "تحليل نسيجي وباثولوجي (Histopathology / Cytology)",
            "تقرير أشعة أو سونار (X-Ray, Ultrasound, MRI, CT)",
            "تقرير طبي عام / آخر"
        ]
    )

api_key = st.text_input("أدخل مفتاح Gemini API Key الخاص بك:", type="password")
uploaded_file = st.file_uploader("ارفع صورة التقرير الطبي أو التحليل المختبري:", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="التقرير المرفوع", use_container_width=True)

if st.button("تحليل التقرير 🚀", use_container_width=True):
    if not api_key:
        st.error("يرجى إدخال مفتاح Gemini API Key أولاً!")
    elif not uploaded_file:
        st.error("يرجى رفع صورة التحليل أولاً!")
    else:
        with st.spinner("جاري قراءة وتحليل النتائج بواسطة الذكاء الاصطناعي..."):
            try:
                client = genai.Client(api_key=api_key)
                
                # توجيهات الموديل بحسب اللغة
                if lang == "العربية":
                    prompt = f"""
                    أنت خبير واستشاري في قراءة وتفسير الفحوصات والتقارير الطبية.
                    نوع التقرير المرفق: {report_type}.
                    
                    يرجى قراءة الصورة المرفقة بعناية وتجهيز الإجابة باللغة العربية كالتالي:
                    1. جدول يوضح: (اسم التحليل / الاختبار، النتيجة Result، المدى الطبيعي Reference Range، والحالة سواء كانت طبيعية أو مرتفعة أو منخفضة).
                    2. ملخص وشرح طبي بسيط يوضح أهم النتائج وما يعنيه التقرير بشكل واصل ومفهوم.
                    3. إذا كان هناك مصطلحات معقدة أو باثولوجية، يرجى تبسيطها.
                    """
                else:
                    prompt = f"""
                    You are an expert medical reports analyst.
                    Report Type: {report_type}.
                    
                    Please read the attached medical report image carefully and structure the response in English:
                    1. A Markdown Table containing: (Test Name, Result, Reference Range, Status: Normal/High/Low).
                    2. A concise medical summary explaining the main findings in clear, easy-to-understand language.
                    3. Explanation of any complex medical or pathological terms present.
                    """

                response = client.models.generate_content(
                 model='gemini-3.8-flash',
                    contents=[image, prompt]
                )
                
                st.success("تم التحليل بنجاح!")
                st.markdown(response.text)
                
                # زر تنزيل التقرير
                st.download_button(
                    label="💾 تنزيل التقرير كملف نصي",
                    data=response.text,
                    file_name="medical_report_analysis.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"حدث خطأ أثناء التحليل: {e}")

st.markdown("---")
st.warning("⚠️ تنبيه طبي: هذا التطبيق يستعين بالذكاء الاصطناعي للمساعدة في فهم وتلخيص نتائج التقارير الطبية فقط، ولا يعتبر بديلاً عن الاستشارة الطبية أو التشخيص المباشر من قبل الطبيب المختص.")
