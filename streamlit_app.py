import streamlit as st
import google.generativeai as genai

st.title("MY AI-CHATBOT Application")

# รับ input จากผู้ใช้
chat_input = st.chat_input("ลองแชทดูสิ")

    # ขอรับ Gemini API Key จากผู้ใช้
gemini_api_key = ""
gemini_api_key = st.text_input("Gemini API Key: ", placeholder="Type your API Key here...", type="password")

# Initialize session state สำหรับเก็บประวัติการแชท
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # เริ่มต้นด้วยลิสต์ว่าง

# เก็บข้อความผู้ใช้ลงใน chat_history
if chat_input:
    st.session_state.chat_history.append({"role": "user", "content": chat_input})

    # ขอรับ Gemini API Key จากผู้ใช้
    gemini_api_key = "AIzaSyBs863Dkizd9f4UsFxbWkCBY0Quu2Ik0a0"

    if gemini_api_key:
        # ตั้งค่า API Key
        genai.configure(api_key=gemini_api_key)

        try:
            # เรียกใช้โมเดล generative AI สำหรับด้านร้าย
            model1 = genai.GenerativeModel("gemini-pro")
            response1 = model1.generate_content(f"บทบาทของคุณคือกูรูที่วิเคราะห์ข้อดีข้อเสียของรถ คุณมีชื่อแบทแมน คุณจะแนะนำรุ่นรถ ที่จะตอบข้อดีและข้อเสีย อย่างละ 3 ข้อแบบสั้นๆได้ใจความ แต่ช่วยแนะนำตัวเอง 1 ประโยตและรอฉันถามก่อนน้ะ {chat_input}")

            # เรียกใช้โมเดล generative AI สำหรับด้านดี
            response2 = model1.generate_content(f"บทบาทของคุณคือพนักงานขายรถชื่ออัลเฟรด คุณจะแนะนำรุ่นรถ ที่จะตอบไม่เกิน 2 ประโยคและพูดแต่เรื่องความคุ้มค่าและราคาของรถ แต่ช่วยแนะนำตัวเอง 1 ประโยตและรอฉันถามก่อนน้ะ {chat_input}")

            if response1 and response1.text:
                bot_response1 = response1.text
                st.session_state.chat_history.append({"role": "assistant_bad", "content": bot_response1})

            if response2 and response2.text:
                bot_response2 = response2.text
                st.session_state.chat_history.append({"role": "assistant_good", "content": bot_response2})

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการเรียก API: {e}")

# แสดงประวัติการแชททั้งหมด
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.chat_message("user").write(chat["content"])
    elif chat["role"] == "assistant_bad":
        st.chat_message("assistant").write(f"นักวิเคราะห์ : {chat['content']}")
    elif chat["role"] == "assistant_good":
        st.chat_message("assistant").write(f"เซลล์ขายรถ : {chat['content']}")
