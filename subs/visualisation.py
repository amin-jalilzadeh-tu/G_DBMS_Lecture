# ver 01.01
import pandas as pd
import streamlit as st

def write_response(response_dict: dict):
    """
    Writes the response as a table if present.
    """
    if "plot" in response_dict and "table" in response_dict["plot"]:
        table_info = response_dict["plot"]["table"]
        df = pd.DataFrame(table_info["data"], columns=table_info["columns"])
        st.table(df)
    elif "answer" in response_dict:
        st.write(response_dict["answer"])
    else:
        st.write("No data to display.")
