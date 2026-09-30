import streamlit as st
import google.generativeai as genai
import PIL.Image

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="Medical Report Analyzer", layout="centered")

st.title("Medical Report Analyzer 🩺")
st.markdown("---")

# جلب المفتاح بأمان من الـ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter Gemini API Key:", type="password", autocomplete="off")

if not api_key:
    st.error("Please provide the API key to proceed.")
    st.stop()

# تهيئة النموذج بالإصدار المطلوب 3.8-flash
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-3.8-flash')

# واجهة رفع التقرير الطبي
uploaded_file = st.file_uploader("Upload Medical Report Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="Uploaded Report", use_container_width=True)

    if st.button("Analyze Report 🚀"):
        with st.spinner("Processing and analyzing the report..."):
            try:
                prompt = (
                    "Please analyze this medical report thoroughly in English. "
                    "Extract all medical values, test names, and findings, and present them in a clear, "
                    "professional medical table, followed by a brief clinical summary and recommendations in English."
                )
                
                response = model.generate_content([image, prompt])
                st.success("Analysis completed successfully!")
                
                if response and hasattr(response, 'text'):
                    safe_text = response.text.encode('utf-8', errors='ignore').decode('utf-8')
                    st.markdown(safe_text)
                else:
                    st.warning("Received an empty response from the model.")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.warning("Medical Disclaimer: هذا التطبيق هو أداة مساعدة للذكاء الاصطناعي ولا يُغني عن التشخيص الطبي المهني.")
