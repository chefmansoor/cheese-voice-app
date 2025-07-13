import streamlit as st
import openai
import base64
import json
import gspread
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval

# Page config
st.set_page_config(page_title="Cheese Inventory Voice App (Mic Fixed)", layout="centered")
st.title("🧀 Cheese Inventory Voice Assistant (Fixed Mic)")

# OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Sheet credentials
google_creds = json.loads(base64.b64decode(st.secrets["GOOGLE_CREDS_BASE64"]))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_info(google_creds, scopes=SCOPES)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).sheet1

# Session state defaults
if "location" not in st.session_state:
    st.session_state["location"] = ""
if "entry" not in st.session_state:
    st.session_state["entry"] = ""

# Location input
st.subheader("1. Set Your Location")
st.session_state["location"] = st.text_input("Enter Inventory Location (e.g. 'Back Walk-In')", value=st.session_state["location"])

# Voice input
st.subheader("2. Speak or Type Your Count")

# Mic transcription
transcript = streamlit_js_eval(js_expressions="speechRecognition", key="speech")
if transcript:
    st.session_state["entry"] = transcript

# Text fallback
entry = st.text_input("Say or type something like: 'Stilton Blue, 5.68 pounds'", value=st.session_state["entry"])
st.session_state["entry"] = entry

if st.button("Log Entry"):
    if st.session_state["entry"].strip() == "" or st.session_state["location"].strip() == "":
        st.error("Please provide both an entry and a location.")
    else:
        sheet.append_row([st.session_state["entry"], st.session_state["location"]])
        st.success("✅ Entry logged successfully!")
        st.session_state["entry"] = ""