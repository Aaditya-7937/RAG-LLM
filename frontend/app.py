# frontend/app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Knowledge Base Chat", layout="wide")
st.title("🤖 Knowledge Base Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.sidebar.header("Upload your documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        files = {"file": (file.name, file.getvalue())}
        try:
            response = requests.post(f"{API_URL}/upload", files=files)
            if response.ok:
                st.sidebar.success(f"Uploaded {file.name}")
            else:
                st.sidebar.error(f"Failed: {file.name}")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

user_input = st.text_input("Ask a question about your documents:")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        MAX_HISTORY = 10
        history_to_send = st.session_state.messages[-MAX_HISTORY:]
        response = requests.post(f"{API_URL}/query", json={"query": user_input, "history": history_to_send })
        if response.ok:
            answer = response.json().get("answer", "No answer returned")
            st.session_state.messages.append({"role": "bot", "content": answer})
        else:
            st.session_state.messages.append({"role": "bot", "content": "❌ Backend failed"})
    except Exception as e:
        st.session_state.messages.append({"role": "bot", "content": f"Error: {e}"})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'''
            <div style="
                background-color: #DCF8C6; 
                color: #000; 
                padding: 12px; 
                border-radius: 12px; 
                margin: 5px; 
                max-width: 75%;
                float: right;
                clear: both;
                font-family: 'Arial', sans-serif;
                font-size: 16px;
            ">{msg["content"]}</div>
            ''',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'''
            <div style="
                background-color: #1E1E1E; 
                color: #FFFFFF; 
                padding: 12px; 
                border-radius: 12px; 
                margin: 5px; 
                max-width: 75%;
                float: left;
                clear: both;
                font-family: 'Arial', sans-serif;
                font-size: 16px;
            ">{msg["content"]}</div>
            ''',
            unsafe_allow_html=True
        )

# Force clearing floats
st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)
