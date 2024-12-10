# ver 01.01
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import os
import streamlit as st

def connect_to_db(cloud=True):
    # Set your DATABASE_URL using provided credentials
    # Assuming schema 'amin' is set as default in the database or accessible directly.
    DATABASE_URL = "postgresql://postgres:mypassword@leda.geodan.nl:5432/research"
    engine = create_engine(DATABASE_URL)

    db = SQLDatabase(engine)
    st.write("🫡 Connecting to the PostgreSQL database...")
    return db


