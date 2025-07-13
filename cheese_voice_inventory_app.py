# cheese_voice_inventory_app.py

import streamlit as st
import datetime
import base64
import json
import openai
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Cheese Voice Inventory", layout="centered")
st.title("🧀 Cheese Inventory Voice Logger")

# Load OpenAI key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Google Sheet Setup
google_creds = json.loads(base64.b64decode(st.secrets["GOOGLE_CREDS_BASE64"]).decode("utf-8"))
credentials = Credentials.from_service_account_info(google_creds)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key(st.secrets["GOOGLE_SHEET_ID"]).sheet1

# Location memory
if "location" not in st.session_state:
    st.session_state["location"] = ""

st.text_input("📍 Set Location", key="location")

# Audio input
audio = st.audio_recorder("🎙️ Record Item", pause_threshold=1.0)

if audio:
    st.write("✅ Audio received. Transcribing...")

    # Transcribe with Whisper (placeholder simulation)
    transcript = "Stilton Blue, five point six eight pounds"  # This should come from Whisper API
    st.write(f"📝 Transcript: {transcript}")

    # GPT parse (placeholder simulated logic)
    product = "Stilton Blue"
    quantity = "5.68"
    unit = "pounds"

    if st.button("Log Entry"):
        now = datetime.datetime.now().isoformat()
        sheet.append_row([now, product, quantity, unit, st.session_state["location"]])
        st.success(f"✅ Logged: {product} - {quantity} {unit} @ {st.session_state['location']}")
