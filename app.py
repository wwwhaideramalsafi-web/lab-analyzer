from google import genai
import PIL.Image
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="مساعد التحليل الطبي الذكي", page_layout="centered"
)

# تصميم واجهة نظيفة وسريعة
st.title("مساعد التحليل الطبي التفاعلي 🩺")
st.markdown(
    "مرحباً بك! ارفع صورة التقرير الطبي وتحدث مع النظام للحصول على تحليل فوري وسريع."
)
st.markdown("---")

# جلب المفتاح بأمان
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    api_key = st.text_input(
        "أدخل مفتاح Gemini API Key:", type="password", autocomplete="off"
    )

if not api_key:
    st.warning("يرجى إدخال مفتاح الـ API للبدء.")
    st.stop()

# إنشاء العميل
client = genai.Client(api_key=api_key)

# الحفاظ على جلسة المحادثة النشطة داخل الذاكرة لتعمل مثل الشات الحقيقي
if "chat" not in st.session_state:
    # استخدام نموذج سريع جداً ومخصص للاستجابة الفورية
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

# رفع الصورة
uploaded_file = st.file_uploader(
    "ارفع صورة التقرير الطبي أو التحليل المختبري هنا",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    image = PIL.Image.open(uploaded_file)

    # تصغير الصورة لكي يتم إرسالها ومعالجتها في أجزاء من الثانية
    image.thumbnail((800, 800))
    st.image(
        image, caption="التقرير المرفوع (جاهز للمحادثة السريعة)", width=400
    )

    # خانة إدخال الرسالة مثل الشات الحقيقي
    user_query = st.text_input(
        "اكتب سؤالك أو طلبك عن التقرير (مثلاً: ما هي النتائج غير الطبيعية؟):"
    )

    if st.button("إرسال الرد 🚀") and user_query:
        with st.spinner("جاري الرد فوراً..."):
            try:
                # إرسال الصورة مع السؤال مباشرة داخل جلسة المحادثة السريعة
                response = st.session_state.chat.send_message(
                    [image, user_query]
                )
                st.success("الرد الفوري:")
                st.write(response.text)
            except Exception as e:
                st.error(
                    "حدث ضغط مؤقت في الشبكة، يرجى إعادة الإرسال فوراً."
                )

st.markdown("---")
st.caption(
    "تنبيه طبي: هذا النظام أداة مساعدة ولا يُغني عن استشارة الطبيب المختص."
)
