import streamlit as st
import openai
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

# Set page config
st.set_page_config(page_title="Cheese Inventory Voice App", layout="centered")

st.title("🧀 Cheese Inventory Voice Assistant (with Mic)")

# API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Sheet Setup with SCOPES
google_creds = json.loads(base64.b64decode(st.secrets["GOOGLE_CREDS_BASE64"]))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_info(google_creds, scopes=SCOPES)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).sheet1

# Session state
if "location" not in st.session_state:
    st.session_state["location"] = ""

if "entry" not in st.session_state:
    st.session_state["entry"] = ""

# JavaScript for mic input using Web Speech API
st.subheader("🎙️ Speak or Type Your Cheese Count")

st.components.v1.html(
    """
    <script>
    const streamlitInput = window.parent.document.querySelector('input[type="text"]');
    if (!window.recognition) {
        const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        window.recognition = recognition;

        const micBtn = document.createElement('button');
        micBtn.innerText = '🎤 Start Listening';
        micBtn.style.margin = '10px 0';
        micBtn.style.padding = '0.5em 1em';
        micBtn.style.fontSize = '16px';
        micBtn.onclick = () => {
            recognition.start();
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            streamlitInput.value = transcript;
            streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        };

        const container = window.parent.document.querySelector('section.main');
        container.prepend(micBtn);
    }
    </script>
    """,
    height=0
)

st.subheader("1. Set Your Location")
st.session_state["location"] = st.text_input("Enter Inventory Location (e.g. 'Back Walk-In')", value=st.session_state["location"])

st.subheader("2. Your Count")
st.session_state["entry"] = st.text_input("Say or type something like: 'Stilton Blue, 5.68 pounds'", value=st.session_state["entry"])

if st.button("Log Entry"):
    if st.session_state["entry"].strip() == "" or st.session_state["location"].strip() == "":
        st.error("Please provide both an entry and a location.")
    else:
        sheet.append_row([st.session_state["entry"], st.session_state["location"]])
        st.success("✅ Entry logged successfully!")
        st.session_state["entry"] = ""
