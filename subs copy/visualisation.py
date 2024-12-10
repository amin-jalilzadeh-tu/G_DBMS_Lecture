# ver 01.01
import pandas as pd
import streamlit as st

def write_response(response_dict: dict):
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame({"columns": data["columns"], "values": data["data"]})
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame({"columns": data["columns"], "values": data["data"]})
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)
