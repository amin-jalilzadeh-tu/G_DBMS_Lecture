# ver 01.01
import os
import streamlit as st
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

def connect_to_db(cloud=True):
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        st.error("No DATABASE_URL found. Please set it in .env.")
        st.stop()

    engine = create_engine(DATABASE_URL)
    db = SQLDatabase(engine)
    st.write("🫡 Connecting to the PostgreSQL database...")
    return db
