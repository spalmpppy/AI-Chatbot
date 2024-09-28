import streamlit as st
import google.generativeai as genai

# Initialize session state variables
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Car Seller & Guru Gen-AI Application")

# User input for chat
chat_input = st.chat_input("ลองแชทดูสิ")

# Input for Gemini API Key
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Process chat input and API call
if chat_input:
    st.session_state.chat_history.append({"role": "user", "content": chat_input})

    # Configure the API Key if it's provided
    if gemini_api_key and st.session_state.gemini_api_key != gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        st.session_state.gemini_api_key = gemini_api_key

    try:
        # Generating responses from the generative model
        model1 = genai.GenerativeModel("gemini-pro")
        response1 = model1.generate_content(f"บทบาทของคุณคือกูรูที่วิเคราะห์ข้อดีข้อเสียของรถ คุณมีชื่อแบทแมน คุณจะแนะนำรุ่นรถ ที่จะตอบข้อดีและข้อเสีย อย่างละ 3 ข้อแบบสั้นๆได้ใจความ แต่ช่วยแนะนำตัวเอง 1 ประโยตและรอฉันถามก่อนน้ะ {chat_input}")
        
        response2 = model1.generate_content(f"บทบาทของคุณคือพนักงานขายรถชื่ออัลเฟรด คุณจะแนะนำรุ่นรถ ที่จะตอบไม่เกิน 2 ประโยคและพูดแต่เรื่องความคุ้มค่าและราคาของรถ แต่ช่วยแนะนำตัวเอง 1 ประโยตและรอฉันถามก่อนน้ะ {chat_input}")

        # Append responses to chat history if they exist
        if response1 and response1.text:
            st.session_state.chat_history.append({"role": "assistant_bad", "content": response1.text})

        if response2 and response2.text:
            st.session_state.chat_history.append({"role": "assistant_good", "content": response2.text})

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเรียก API: {str(e)}")

# Display chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    elif chat["role"] == "assistant_bad":
        st.chat_message("assistant").write(f"นักวิเคราะห์ : {chat['content']}")
    elif chat["role"] == "assistant_good":
        st.chat_message("assistant").write(f"เซลล์ขายรถ : {chat['content']}")
