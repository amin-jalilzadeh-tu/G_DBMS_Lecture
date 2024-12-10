# ver 01.08
import os
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate
)
from langchain_openai import OpenAIEmbeddings
from langchain.schema import SystemMessage, HumanMessage

def get_examples_for_chain(chain):
    # We will not provide specific examples now, returning None for generalization.
    return None

def system_prefix(chain_id: str):
    if chain_id == "chain_1":
        return """
        You are an SQL generation and execution agent interacting with a PostgreSQL database that uses the 'amin' schema.

        **Schema Overview**:
        - amin.department(dname, dnumber, mgr_ssn, mgr_start_date)
        - amin.dependent(essn, dependent_name, sex, bdate, relationship)
        - amin.dept_locations(dnumber, dlocation)
        - amin.employee(fname, minit, lname, ssn, bdate, address, sex, salary, super_ssn, dno)
        - amin.project(pname, pnumber, plocation, dnum)
        - amin.works_on(essn, pno, hours)

        **Your Task (Chain 1)**:
        1. The user will ask a question about the data in these tables.
        2. Produce exactly one SELECT query (no inserts, updates, deletes, creates, or drops) using `amin.` prefix for all tables.
        3. Execute that SELECT query.
        4. Output the following in your final answer:
           - The original user question.
           - The exact SELECT query you ran.
           - The raw query results once (with column headers if available, and all returned rows). If no rows are returned, say "No rows returned." after showing headers.
        5. If unsure how to produce a correct SELECT query or answer the question, return exactly "I don't know" as the entire answer.
        6. No modifications to the database are allowed. Only SELECT.
        7. Do not summarize or truncate the output. No ellipses. Show all data fully.
        8. Do not show results multiple times. Only once.

        These rules apply to any question the user asks related to the given tables.
        """
    elif chain_id == "chain_2":
        return """
        You are a table formatting agent. You receive the raw output from Chain 1 plus the original user query at the end.

        **Input Format**:
        - The output from Chain 1 will contain:
          - The user's original question.
          - The SELECT query used.
          - The raw results (column headers and rows, or "No rows returned." if empty).
        - At the end of this output, you'll see `{original_input}=<the_user_query>` indicating the user's original query.

        **Your Task (Chain 2)**:
        Convert these raw results into a JSON structure or "No data available." based on whether any rows exist.

        Desired output when data is available:
        {
          "plot": {
            "table": {
              "columns": ["col1","col2",...],
              "data": [
                ["val11","val12",...],
                ["val21","val22",...],
                ...
              ]
            }
          },
          "output_of_chain1": "<the_user_query>"
        }

        If no data:
        {
          "answer": "No data available."
        },
        "output_of_chain1":"<the_user_query>"

        **Instructions**:
        1. Identify columns from the header line if present. If no header line, infer columns from the SELECT query.
        2. Each subsequent line after the header is a row. Split by consistent spacing or delimiter, trim whitespace, and convert all values to strings.
        3. If "No rows returned." or no data rows appear, return the no-data format above.
        4. No guessing or fabricating data. If unsure, return no-data format.
        5. Present the data exactly as shown.

        This applies to any query output, not just a specific example.
        """
    else:
        return ""

def invoke_full_prompt(chain_id: str) -> ChatPromptTemplate:
    system_msg = SystemMessage(content=system_prefix(chain_id))
    # For general queries, no example-based few-shots:
    # The instructions alone must guide the model.
    # We'll rely solely on the system message and the user input.
    return ChatPromptTemplate.from_messages([
        system_msg,
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

def agent_table_response_v2(user_query: str, sql_data: str) -> str:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
    system_message = SystemMessage(content=system_prefix("chain_2"))

    user_content = sql_data.strip() + "\n\n{original_input}=" + user_query
    user_message = HumanMessage(content=user_content)

    response = llm([system_message, user_message])
    return response.content.strip()
