# ver 01.01
from langchain_community.agent_toolkits import create_sql_agent
from subs.db_connections import connect_to_db
from dotenv import load_dotenv
import os
from subs.prompts import invoke_full_prompt, agent_plot_and_response_v2
import streamlit as st

load_dotenv(override=True)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def init_llm(api_key: str):
    # Not used directly here since we call create_sql_agent with llm param elsewhere if needed.
    pass

def sql_agent(prompt):
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

def generate_sql_and_plot(chain_id_sql: str, chain_id_response_plot: str, user_query: str) -> tuple:
    # 1. Get the prompt for SQL
    prompt_for_sql = invoke_full_prompt(chain_id=chain_id_sql)
    chain_sql = sql_agent(prompt=prompt_for_sql)
    sql_output = chain_sql.run(user_query)

    st.write("✅ Data fetched, now preparing the figure...")

    # 2. Generate plotting code from sql_output
    plot_output = agent_plot_and_response_v2(
        user_query=user_query, plot_data=sql_output
    )

    return sql_output, plot_output
