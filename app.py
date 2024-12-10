# ver 01.01
import streamlit as st
import os
from dotenv import load_dotenv

from pages.service_overview import overview_txt
from pages.irish_data_chatbot import irish_data_chatbot
from subs.styles import get_no_sidebar_style

load_dotenv(override=True)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
print("OPENAI_API_KEY from env:", OPENAI_API_KEY)

if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY not found. Please set it in .env")
    st.stop()

st.set_page_config(
    page_title="SQL Query and Data Analysis Chatbot ",
    page_icon="🏭",
)
st.title("SQL Query and Data Analysis Chatbot 💬 ")

st.markdown("Use the sidebar to navigate between pages.")

def page0():
    overview_txt()

def page1():
    irish_data_chatbot()

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a page:", ("Service Overview", "Data Chatbot")
)

if page == "Data Chatbot":
    page1()
elif page == "Service Overview":
    page0()

no_sidebar_style = get_no_sidebar_style()
st.markdown(no_sidebar_style, unsafe_allow_html=True)
