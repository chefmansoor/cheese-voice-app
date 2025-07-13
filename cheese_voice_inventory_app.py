
import streamlit as st
import openai
import base64
import json
import gspread
from google.oauth2.service_account import Credentials

# Set page config
st.set_page_config(page_title="Cheese Inventory Voice App", layout="centered")

st.title("🧀 Cheese Inventory Voice Assistant")

# API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Sheet Setup with SCOPES added
google_creds = json.loads(base64.b64decode(st.secrets["GOOGLE_CREDS_BASE64"]))
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_info(google_creds, scopes=SCOPES)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).sheet1

# Session state
if "location" not in st.session_state:
    st.session_state["location"] = ""

# UI
st.subheader("1. Set Your Location")
st.session_state["location"] = st.text_input("Enter Inventory Location (e.g. 'Back Walk-In')", value=st.session_state["location"])

st.subheader("2. Say or Type a Cheese Count")
entry = st.text_input("Example: 'Stilton Blue, 5.68 pounds'")

if st.button("Log Entry"):
    if entry.strip() == "" or st.session_state["location"].strip() == "":
        st.error("Please provide both an entry and a location.")
    else:
        sheet.append_row([entry, st.session_state["location"]])
        st.success("Entry logged successfully!")
