import streamlit as st
from datetime import date
from travel import create_ticket_agent
import os 
from dotenv import load_dotenv
load_dotenv()

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="AI Ticket Booking Assistant",
    layout="centered"
)

st.title("✈️ AI Ticket Booking Assistant")
st.caption("Find the fastest and cheapest flights using real-time data")

# ---- LOAD KEYS ----
if not st.secrets:
    load_dotenv()

openai_api_key = (
    st.secrets["OPENAI_API_KEY"]
    if "OPENAI_API_KEY" in st.secrets
    else os.getenv("OPENAI_API_KEY")
)

Google_API = (
    st.secrets["SERPER_API"]
    if "SERPER_API" in st.secrets
    else os.getenv("SERPER_API")
)

if not openai_api_key or not Google_API:
    st.error("API keys not found. Please configure secrets.")
    st.stop()
# openai_api_key= os.environ.get('OPENAI_API_KEY')
# Google_API = os.environ.get('SERPER_API')

# ---- CREATE AGENT (ONCE) ----
agent_executor = create_ticket_agent(
    openai_api_key=openai_api_key,
    Google_API=Google_API
)

# ================= UI =================

st.subheader("📍 Trip Details")
col1, col2 = st.columns(2)

with col1:
    source = st.text_input("From", placeholder="Kochi")

with col2:
    destination = st.text_input("To", placeholder="Bengaluru")

st.subheader("📅 Date & Time")
col3, col4 = st.columns(2)

with col3:
    travel_date = st.date_input("Travel Date", min_value=date.today())

with col4:
    time_slot = st.selectbox(
        "Preferred Time",
        ["Morning (7–10 AM)", "Afternoon", "Evening", "Night"]
    )

st.subheader("💰 Budget")
budget = st.number_input("Budget (₹)", min_value=1000, step=500)

st.divider()

# ---- SEARCH BUTTON ----
if st.button("🔍 Search Flights", use_container_width=True):
    if not source or not destination:
        st.error("Please enter both source and destination.")
    else:
        query = (
            f"{source} to {destination} on {travel_date}, "
            f"{time_slot}, budget ₹{budget}, flight"
        )

        with st.spinner("Searching best flight options..."):
            response = agent_executor.invoke({"input": query})

        st.success("Best available flight found!")

        st.subheader("🧾 Flight Details")
        st.markdown(response["output"])

st.divider()
st.caption("Powered by OpenAI • Google Serper • LangChain")