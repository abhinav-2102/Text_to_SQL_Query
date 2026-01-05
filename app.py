from dotenv import load_dotenv
load_dotenv()  # load all the env variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genAi
from google.api_core.exceptions import ResourceExhausted

# Configure the API key
# Try to get it from environment (local), otherwise from streamlit secrets (cloud)
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    try:
        # Fallback for Streamlit Cloud
        api_key = st.secrets["GOOGLE_API_KEY"]
    except FileNotFoundError:
        st.error("API Key not found. Please set GOOGLE_API_KEY in your .env file (local) or Streamlit Secrets (cloud).")
        st.stop()

genAi.configure(api_key=api_key)

def get_gemini_response(question, prompt):
    try:
        # 1. List all models available to your API key
        available_models = []
        for m in genAi.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # DEBUG: Print found models to the Streamlit UI so we can see what's happening
        if not available_models:
            return "Error: API Key is valid, but no text-generation models were found. (Check API permissions)"
        
        # 2. Priority selection: Try to find 'flash' first, then 'pro', then '1.0'
        chosen_model = None
        for model in available_models:
            if 'gemini-1.5-flash' in model:
                chosen_model = model
                break
        
        if not chosen_model:
            for model in available_models:
                if 'gemini-pro' in model:
                    chosen_model = model
                    break
        
        # 3. Fallback: If preferences aren't found, just pick the first valid one
        if not chosen_model:
            chosen_model = available_models[0]

        # Display the chosen model (Optional debugging info)
        # st.write(f"Debug: Using model -> {chosen_model}") 

        # 4. Generate Content
        model = genAi.GenerativeModel(chosen_model)
        response = model.generate_content([prompt, question])
        return response.text

    except Exception as e:
        return f"Error using model {chosen_model if 'chosen_model' in locals() else 'Unknown'}: {e}"

# Function to load google gemini model
#def get_gemini_response(question, prompt):
    # Hardcoding the model is faster and more reliable than listing them every time
    #try:
        #model = genAi.GenerativeModel('gemini-pro')
        #response = model.generate_content([prompt, question])
        #return response.text
    #except Exception as e:
        #return f"Error generating content: {e}"

# Function to retrieve query from the sql db
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    # Clean the SQL just in case the LLM adds markdown backticks
    clean_sql = sql.replace("```sql", "").replace("```", "").strip()
    
    try:
        cur.execute(clean_sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        st.error(f"SQL Error: {e}")
        return []

# Define your prompt
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name STUDENT and has the following columns - NAME, BRANCH, SECTION, and MARKS.

For example:
Example 1 - How many entries of records are present?
The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the students studying in Data Science Class?
The SQL command will be something like this: SELECT * FROM STUDENT WHERE BRANCH="Data Science";

also the sql code should not have ``` in the beginning or in the end and no word sql in output.
"""

st.set_page_config(page_title="I can retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

# Sidebar schema display
st.sidebar.title("Sample Database")
st.sidebar.caption("Schema Overview")

try:
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(STUDENT)")
    columns = cur.fetchall()
    conn.close()

    if columns:
        schema_data = [{"Column Name": col[1], "Data Type": col[2]} for col in columns]
        st.sidebar.table(schema_data)
    else:
        st.sidebar.warning("Table 'STUDENT' not found. Please run sql.py first.")

except Exception as e:
    st.sidebar.error(f"Could not load database schema: {e}")

question = st.text_input("Input Prompt: ", key="input")
submit = st.button("Enter")

if submit:
    if not api_key:
        st.error("API Key missing. Please check your .env file.")
    else:
        with st.spinner("Talking to Gemini..."):
            response = get_gemini_response(question, prompt)
            
            if response.startswith("Error:"):
                st.error(response)
            else:
                st.write(f"Generated SQL: `{response}`")
                
                data = read_sql_query(response, "student.db")
                
                st.subheader("The response is:")
                if not data:
                    st.warning("No data found or SQL query failed.")
                for row in data:
                    st.write(row)





