# ver 01.01
import streamlit as st

def overview_txt():
    st.markdown(
        """
        ## Service Overview
        This application allows you to query a PostgreSQL database using natural language,
        and returns results as a table.

        ### How to Use
        - Go to the "Data Chatbot" page.
        - Ask a question about the dataset.
        - Hit "Submit" to see results displayed as a table.

        **Data Schema**: Includes tables such as department, employee, project, works_on, dependent, dept_locations.
        """
    )
