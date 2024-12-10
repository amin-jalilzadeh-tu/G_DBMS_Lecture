# ver 01.01
import os
import streamlit as st
from dotenv import load_dotenv
from subs.db_connections import connect_to_db
from subs.prompts import invoke_full_prompt, agent_table_response_v2

load_dotenv(override=True)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def sql_agent(prompt):
    from langchain_community.agent_toolkits import create_sql_agent
    from langchain_openai import ChatOpenAI

    db = connect_to_db(cloud=True)
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, openai_api_key=OPENAI_API_KEY)
    agent = create_sql_agent(
        llm=llm,
        db=db,
        prompt=prompt,
        verbose=True,
        agent_type="openai-tools",
    )
    return agent

def generate_sql_and_table(chain_id_sql: str, chain_id_response_table: str, user_query: str) -> tuple:
    """
    Executes:
    1) SQL chain: converts user query into SQL and gets raw results.
    2) Table chain: converts raw results into a table JSON.

    Returns (sql_output, table_output).
    """
    prompt_for_sql = invoke_full_prompt(chain_id=chain_id_sql)
    chain_sql = sql_agent(prompt=prompt_for_sql)
    sql_output = chain_sql.run(user_query)

    st.write("✅ Data fetched, now preparing the table...")

    table_output = agent_table_response_v2(user_query=user_query, sql_data=sql_output)
    return sql_output, table_output
