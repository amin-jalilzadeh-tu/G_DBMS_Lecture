# SQL Query and Data Analysis Chatbot 💬

The source code can be found here: [DataInsightChatbot](https://github.com/SaM-92/DataInsightChatbot/tree/main).

This version has been modified to create a chatbot based on the tables from **Assignment 2**.

## Setup Instructions

1. **Create a `.env` file.**

2. **Add your OpenAI API key and database connection details:**
    ```env
    OPENAI_API_KEY=sk-proj-.......apRr
    DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/name_of_your_database
    ```

3. **Modify prompts** in the `subs/prompts.py` file as needed.

4. **Install the necessary libraries** from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the project** in the terminal with:
    ```bash
    streamlit run app.py
    ```

## Additional Information

- **`lecture.ipynb`** includes code relevant to PYSQL, Pandas, and GeoPandas.

![Real-time Data Scraping Diagram](/images/overview.gif)
