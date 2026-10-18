
import streamlit as st
from google import genai

st.set_page_config(
    page_title="UzbekAI",
    page_icon="🤖"
)

st.title("🇺🇿 UzbekAI")
st.subheader("Sening aqlli yordamching!")

st.write("Salom! Men UzbekAI. Savolingni yoz!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("UzbekAI'ga xabar yoz...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            client = genai.Client(api_key=api_key)

            history = []
            for message in st.session_state.messages[:-1]:
                role = "user" if message["role"] == "user" else "model"
                history.append({
                    "role": role,
                    "parts": [{"text": message["content"]}]
                })

            chat = client.chats.create(
                model="gemini-2.5-flash",
                history=history
            )

            response = chat.send_message(prompt)
            answer = response.text or "Javob olinmadi."

        except Exception as e:
            answer = (
                "AI bilan bog‘lanishda xatolik yuz berdi. "
                "Secrets nomi, API kaliti va model mavjudligini tekshir."
            )
            st.error("Xatolik: " + str(e))

        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
