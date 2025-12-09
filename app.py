from dotenv import load_dotenv
load_dotenv() ##load all the env variables

import streamlit as st
import os
import sqlite3 
import google.generativeai as genAi
from google.api_core.exceptions import ResourceExhausted
# Configure the API key
api_key = os.getenv("GOOGLE_API_KEY")
genAi.configure(api_key=api_key)

# --- NEW FUNCTION: Automatically find a working model ---
def get_available_model():
    """Finds the first available text generation model for your key."""
    try:
        for m in genAi.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return m.name
                return m.name
    except Exception as e:
        return None
    return None

# Function to load google gemini model
def get_gemini_response(question, prompt):
    model_name = get_available_model()
    
    if not model_name:
        return "Error: No suitable model found. Please enable 'Google Generative Language API' in your Cloud Console."

    model = genAi.GenerativeModel(model_name)
    response = model.generate_content([prompt, question])
    return response.text

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

# --- NEW FEATURE: Sidebar Schema Display ---
st.sidebar.title("Sample Database")
st.sidebar.caption("Schema Overview")

try:
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()
    # "PRAGMA table_info" is the SQLite command to get column details
    cur.execute("PRAGMA table_info(STUDENT)")
    columns = cur.fetchall()
    conn.close()

    if columns:
        # Create a clean list of dictionaries for display
        schema_data = [{"Column Name": col[1], "Data Type": col[2]} for col in columns]
        st.sidebar.table(schema_data)
    else:
        st.sidebar.warning("Table 'STUDENT' not found. Please run sql.py first.")

except Exception as e:
    st.sidebar.error(f"Could not load database schema: {e}")
# -------------------------------------------

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

