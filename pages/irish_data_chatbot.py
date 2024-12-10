# ver 01.01
import streamlit as st
from subs.agent import generate_sql_and_table
from subs.post_processing import post_process_chain_response
from subs.visualisation import write_response

def irish_data_chatbot():
    query = st.text_area(
        label="Please ask your SQL-related question 👇🏻 -- tables are provided from assignemnt 2",
        placeholder="Example: Count the number of employees in each department."
    ).strip()

    if "button_pressed" not in st.session_state:
        st.session_state["button_pressed"] = False

    if st.button("Submit"):
        st.session_state["button_pressed"] = True

    if st.session_state["button_pressed"] and query:
        with st.spinner("Processing your request... Please wait."):
            chain_id_sql = "chain_1"
            chain_id_response_table = "chain_2"
            sql_output, table_output = generate_sql_and_table(
                chain_id_sql, chain_id_response_table, query
            )
            st.session_state["button_pressed"] = False

            if sql_output:
                st.write(sql_output)
            else:
                st.write("Sorry, I cannot answer the question. Try rephrasing your query.")

            if table_output:
                # Process and display the table response
                response_dict = post_process_chain_response(table_output)
                write_response(response_dict)
            else:
                st.write("No table generated for this query.")
    else:
        st.write("Please enter a query and press Submit.")
