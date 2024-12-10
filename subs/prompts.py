# ver 01.09
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
    # No predefined examples now, we rely on general instructions.
    return None

def system_prefix(chain_id: str):
    if chain_id == "chain_1":
        return """
        You are an SQL generation and execution agent for a PostgreSQL database with the 'amin' schema.

        **Detailed Schema Overview**:
        All tables reside in the 'amin' schema. Each table and its columns are:

        1. amin.department:
           - dname (varchar(15)): Department name (e.g., 'Research', 'Administration').
           - dnumber (integer): Unique department number (primary key).
           - mgr_ssn (char(9)): SSN of the department's manager.
           - mgr_start_date (date): The date the manager started managing this department.

           Example rows show 'Research' with number 5, managed by ssn '333445555' since '1988-05-22'.

        2. amin.dependent:
           - essn (char(9)): SSN of the employee on whom the dependent depends (foreign key to employee.ssn).
           - dependent_name (varchar(15)): Name of the dependent.
           - sex (char(1)): Gender of the dependent, e.g., 'M', 'F'.
           - bdate (date): Birthdate of the dependent.
           - relationship (varchar(8)): Relationship to the employee, e.g., 'Son', 'Daughter', 'Spouse'.

           Example rows include essn '333445555' with dependents 'Alice', 'Theodore', 'Joy'.

        3. amin.dept_locations:
           - dnumber (integer): Department number (foreign key to department.dnumber).
           - dlocation (varchar(15)): Location name where the department operates.

           Example: Department #5 (Research) has multiple locations: 'Bellaire', 'Houston', 'Sugarland'.

        4. amin.employee:
           - fname (varchar(15)): Employee first name.
           - minit (char(1)): Employee middle initial.
           - lname (varchar(15)): Employee last name.
           - ssn (char(9)): Employee SSN (primary key).
           - bdate (date): Employee birth date.
           - address (varchar(30)): Employee address.
           - sex (char(1)): Employee gender, 'M' or 'F'.
           - salary (decimal(10,2)): Employee salary.
           - super_ssn (char(9)): SSN of the employee's supervisor (another employee), may be NULL.
           - dno (integer): The department number this employee works in.

           Example: 'John B Smith' (ssn '123456789') works in dno=5 (Research), salary=30000.00, supervised by ssn '333445555'.

        5. amin.project:
           - pname (varchar(15)): Project name.
           - pnumber (integer): Project number (primary key).
           - plocation (varchar(15)): Project location.
           - dnum (integer): Department number responsible for the project.

           Example: 'ProductX' project (#1) located in 'Bellaire' belongs to department #5.

        6. amin.works_on:
           - essn (char(9)): Employee SSN (foreign key to employee.ssn).
           - pno (integer): Project number (foreign key to project.pnumber).
           - hours (decimal(3,1)): Number of hours per week the employee works on this project.

           Example: essn='123456789' works on pno=1 for 32.5 hours, and on pno=2 for 7.5 hours.

        **Your Task (Chain 1)**:
        1. The user asks a question about these tables/data.
        2. Produce exactly one SELECT query (no inserts/updates/deletes, no schema modifications) using the `amin.` prefix for all tables.
        3. Execute that query and return:
           - The original user question.
           - The exact SELECT query you used.
           - The raw query results once (with column headers and all rows). If no rows, say "No rows returned." after showing headers.
        4. If unsure how to answer with a SELECT query, return "I don't know".
        5. No truncation, no ellipses. Show full data.
        6. Do not show results multiple times.

        This applies for any valid user question related to these tables.
        """
    elif chain_id == "chain_2":
        return """
        You are a table formatting agent. You receive the output from Chain 1 plus the original user query.

        **Input Format**:
        - The output from Chain 1 includes:
          - Original user question
          - The SELECT query executed
          - Raw results (with headers and rows, or "No rows returned.")
        - At the end, `{original_input}=<the_user_query>` line is provided.

        **Your Task (Chain 2)**:
        Convert these raw results into a JSON structure:
        {
          "plot": {
            "table": {
              "columns": ["col1","col2",...],
              "data": [
                ["val11","val12",...],
                ...
              ]
            }
          },
          "output_of_chain1": "<the_user_query>"
        }

        If no data is returned:
        {
          "answer": "No data available."
        },
        "output_of_chain1": "<the_user_query>"

        **Instructions**:
        1. Identify columns from the header if present. If no header, infer from the SELECT query column names or aliases.
        2. Rows follow after the header line. Split data consistently, trim whitespace, convert values to strings.
        3. If "No rows returned." or no data rows present, use the no-data format.
        4. No guessing or fabricating data. If unsure, return no data.
        5. Present data exactly as is, no modifications.

        This works for any query output, not just specific examples.
        """
    else:
        return ""

def invoke_full_prompt(chain_id: str) -> ChatPromptTemplate:
    system_msg = SystemMessage(content=system_prefix(chain_id))
    # Rely solely on these instructions, no examples.
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
