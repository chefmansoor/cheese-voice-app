# cheese_voice_inventory_app.py

import streamlit as st
import datetime

st.set_page_config(page_title="Cheese Voice Inventory", layout="centered")
st.title("🧀 Cheese Inventory Logger")

if "location" not in st.session_state:
    st.session_state.location = ""

st.text_input("Set Location", key="location")

item = st.text_input("Enter item name")
quantity = st.text_input("Enter quantity")
unit = st.selectbox("Unit", ["", "each", "pounds", "cases", "logs", "wheels"])

if st.button("Log Entry"):
    timestamp = datetime.datetime.now().isoformat()
    st.success(f"✅ Logged: {item}, {quantity} {unit}, Location: {st.session_state.location}, Time: {timestamp}")
    # Placeholder: Add code to write to Google Sheets here
