import streamlit as st
from openai import OpenAI
import PIL.Image
import base64
from io import BytesIO

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="Medical Report Analyzer", layout="centered")

st.title("Medical Report Analyzer 🩺")
st.markdown("---")

# جلب مفتاح OpenAI بأمان من الـ Secrets أو إدخاله يدوياً
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter OpenAI API Key:", type="password", autocomplete="off")

if not api_key:
    st.error("Please provide the OpenAI API key to proceed.")
    st.stop()

# تهيئة عميل OpenAI
client = OpenAI(api_key=api_key)

# واجهة رفع التقرير الطبي
uploaded_file = st.file_uploader("Upload Medical Report Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="Uploaded Report", use_container_width=True)

    if st.button("Analyze Report 🚀"):
        with st.spinner("Processing and analyzing the report with ChatGPT..."):
            try:
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text", 
                                    "text": "Please analyze this medical report thoroughly in English. Extract all medical values, test names, and findings, and present them in a clear, professional medical table, followed by a brief clinical summary and recommendations in English."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{img_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000
                )
                
                st.success("Analysis completed successfully!")
                
                if response.choices and response.choices[0].message.content:
                    st.markdown(response.choices[0].message.content)
                else:
                    st.warning("Received an empty response from the model.")
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.warning("Medical Disclaimer: هذا التطبيق هو أداة مساعدة للذكاء الاصطناعي ولا يُغني عن التشخيص الطبي المهني.")
