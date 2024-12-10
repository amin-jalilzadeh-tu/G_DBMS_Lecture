# ver 01.01
import os  # Add this line!
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import OpenAIEmbeddings

def get_examples_for_chain(chain):
    if chain == "chain_1":
        examples = [
            {
                "input": "Which projects are handled by the Research department?",
                "query": "SELECT p.pname FROM project p JOIN department d ON p.dnum = d.dnumber WHERE d.dname = 'Research';"
            },
            {
                "input": "List all departments and their managers.",
                "query": "SELECT dname, dnumber, mgr_ssn, mgr_start_date FROM department;"
            }
        ]
        return examples
    else:
        return None

def system_prefix(input):
    if input == "chain_1":
        system_prefix = """
        You are an agent designed to interact with a SQL PostgreSQL database.
        Given a question, produce a correct SQL query.
        - Return only SELECT queries.
        - If unsure, return "I don't know".
        """
        return system_prefix
    elif input == "chain_2":
        system_prefix = """
        Format the output as instructed:
        If drawing a table:
        {
          "plot": {
            "table": {
              "columns": ["col1","col2",...],
              "data": [["val1","val2",...],...]
            }
          },
          "output_of_chain1": "{original_input}"
        }

        If creating a bar chart:
        {
          "plot": {
            "bar": {
              "columns": ["X","Y","Z",...],
              "data": [valX, valY, valZ,...]
            }
          },
          "output_of_chain1": "{original_input}"
        }

        If creating a line chart:
        {
          "plot": {
            "line": {
              "columns": ["X","Y","Z",...],
              "data": [valX, valY, valZ,...]
            }
          },
          "output_of_chain1": "{original_input}"
        }

        If just answer (no plot):
        {
          "answer":"answer"
        },
        "output_of_chain1":"{original_input}"

        If unknown:
        {
          "answer":"I do not know."
        },
        "output_of_chain1":"{original_input}"
        """
        return system_prefix
    elif input == "chain_python_coder":
        return (
            "You are an expert in generating Python plotting scripts using matplotlib. "
            "You will be given a user query and dataset. Output only syntactically valid Python code, nothing else. "
            "Requirements:\n"
            "- No markdown, no explanations, no code fences, only Python code.\n"
            "- Import matplotlib.pyplot as plt.\n"
            "- Use `fig, ax = plt.subplots()`.\n"
            "- Plot the given data. If bar chart, use ax.bar(...), if line, use ax.plot(...).\n"
            "- Always define `fig`.\n"
            "- Do not call plt.show().\n"
            "- Handle None values by treating them as 0.\n"
            "- The code must be ready to exec() without modification.\n"
        )
    else:
        return None

def example_selector(chain_id: str) -> SemanticSimilarityExampleSelector:
    examples = get_examples_for_chain(chain_id)
    return SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"]),
        FAISS,
        k=5,
        input_keys=["input"],
    )

def few_shot_prompt(chain_id: str) -> FewShotPromptTemplate:
    return FewShotPromptTemplate(
        example_selector=example_selector(chain_id),
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix(chain_id),
        suffix="",
    )

def invoke_full_prompt(chain_id: str) -> ChatPromptTemplate:
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=few_shot_prompt(chain_id)
    )
    full_prompt = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    return full_prompt

def python_plotter_prompt_sys():
    return (
        "You are an expert in generating Python plotting scripts using matplotlib. "
        "The code must be valid Python only, no markdown. "
        "Define fig, ax = plt.subplots(). Do not show the plot. "
        "Only produce code."
    )

def python_plotter_prompt_user(user_query, plot_data):
    return (
        f'User query: "{user_query}"\n'
        f"Data:\n{plot_data}\n\n"
        "Generate only Python code following the instructions."
    )

def agent_plot_and_response_v2(user_query: str, plot_data: str) -> str:
    from langchain_openai import ChatOpenAI
    from langchain.schema import SystemMessage, HumanMessage

    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
    system_msg = SystemMessage(content=system_prefix("chain_python_coder"))
    user_msg = HumanMessage(content=python_plotter_prompt_user(user_query, plot_data))
    response = llm([system_msg, user_msg])
    return response.content.strip()
