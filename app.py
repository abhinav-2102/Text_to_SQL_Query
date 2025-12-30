import streamlit as st
import sqlite3
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Configure Gemini using Streamlit Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("GOOGLE_API_KEY not found. Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Gemini response function
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content([prompt, question])
        return response.text
    except ResourceExhausted:
        return "Error: API quota exceeded."
    except Exception as e:
        return f"Error: {e}"

# SQL execution
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    clean_sql = sql.replace("```sql", "").replace("```", "").strip()

    try:
        cur.execute(clean_sql)
        rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        st.error(f"SQL Error: {e}")
        return []

# Prompt
prompt = """
You are an expert in converting English questions to SQL queries.
Database: STUDENT(NAME, BRANCH, SECTION, MARKS)

Rules:
- Return ONLY SQL
- No backticks
- No explanations
"""

st.set_page_config(page_title="Text to SQL using Gemini")
st.header("Gemini SQL Query App")

question = st.text_input("Ask a question:")
submit = st.button("Generate SQL")

if submit:
    with st.spinner("Talking to Gemini..."):
        response = get_gemini_response(question, prompt)

        if response.startswith("Error"):
            st.error(response)
        else:
            st.code(response, language="sql")
            data = read_sql_query(response, "student.db")

            if data:
                st.subheader("Result")
                for row in data:
                    st.write(row)
            else:
                st.warning("No results returned.")
