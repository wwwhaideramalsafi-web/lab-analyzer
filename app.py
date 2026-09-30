import streamlit as st
from google import genai
import PIL.Image

st.set_page_config(page_title="Medical Report Analyzer", layout="centered")

st.title("Medical Report Analyzer")
st.markdown("---")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter Gemini API Key:", type="password", autocomplete="off")

if not api_key:
    st.error("Please provide the API key to proceed.")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("Upload Medical Report Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)
    image.thumbnail((800, 800))
    st.image(image, caption="Uploaded Report", use_container_width=True)

    if st.button("Analyze Report"):
        with st.spinner("Processing and analyzing the report..."):
            try:
                prompt = (
                    "Please analyze this medical report thoroughly in English. "
                    "Extract the values and findings, and present them in a clear, professional medical table, "
                    "followed by a brief summary and recommendations in English."
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[image, prompt]
                )
                st.success("Analysis completed successfully!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

st.markdown("---")
st.warning("Medical Disclaimer: This application is an AI assistant tool and does not replace professional medical diagnosis.")
