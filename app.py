import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="Enterprise AI Operations Assistant", page_icon="🤖")
st.title("🤖 Enterprise AI Operations Assistant")
st.caption(
    "Multi-agent business automation demo — Inventory, Sales & Support agents "
    "coordinated by a Manager Agent."
)

if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

prompt = st.chat_input("e.g. Check stock for 100 laptops and prepare a quotation")
if prompt:
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Coordinating agents..."):
            try:
                resp = requests.post(
                    BACKEND_URL, json={"user": "Raj", "message": prompt}, timeout=180
                )
                resp.raise_for_status()
                answer = resp.json()["response"]
            except Exception as e:
                answer = f"Error contacting backend: {e}"
            st.markdown(answer)
    st.session_state.history.append(("assistant", answer))
