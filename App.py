import streamlit as st
import requests

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="SQL Helper Pro", page_icon="🗄️", layout="wide")

# ---------------------------
# Header
# ---------------------------
st.markdown("<h1 style='text-align: center;'>🗄️ SQL Helper Pro</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Turn plain English into SQL instantly — powered by Google Gemini</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------------------
# Sidebar Settings
# ---------------------------
st.sidebar.header("⚙️ Settings")

# Info box for users
st.sidebar.info(
    "⚠️ To use this app, you need your **own free Google Gemini API key**.\n\n"
    "👉 Get it here: [aistudio.google.com](https://aistudio.google.com)\n\n"
    "Copy the key and paste it below ⬇️"
)

# API Key Input
api_key = st.sidebar.text_input("🔑 Google Gemini API Key:", type="password")

# Database Type Selection
db_type = st.sidebar.radio(
    "📂 Select Database Type:",
    ["SQLite", "MySQL", "PostgreSQL"]
)

# ---------------------------
# Instructions
# ---------------------------
with st.expander("ℹ️ How to use this app", expanded=False):
    st.markdown("""
    1. Enter your **Google Gemini API key** in the sidebar.  
    2. Select your **database type** (SQLite, MySQL, PostgreSQL).  
    3. Write your request in plain English below.  
    4. Click **Generate SQL** and copy the result!  
    """)

# ---------------------------
# Main Input Area
# ---------------------------
question = st.text_area(
    "💬 Write your query in plain English:",
    placeholder="Example: Show the average salary of employees by department"
)

# ---------------------------
# Generate SQL
# ---------------------------
if st.button("✨ Generate SQL Query"):
    if not api_key:
        st.error("❌ Please enter your Google Gemini API key in the sidebar.")
    elif not question.strip():
        st.warning("⚠️ Please write a query request first.")
    else:
        # Gemini API Call
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": api_key}

        prompt = f"""
        You are an expert SQL assistant.
        Generate only the raw {db_type} SQL query for the following request.
        Do not include explanations or extra text. Only output SQL inside code block.

        Request: {question}
        """


        data = {"contents": [{"parts": [{"text": prompt}]}]}

        response = requests.post(url, headers=headers, params=params, json=data)

        if response.status_code == 200:
            result = response.json()
            try:
                sql_query = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                st.success(f"✅ Here’s your {db_type} SQL query:")
                st.code(sql_query, language="sql")

                # Download option
                st.download_button(
                    label="💾 Download SQL Query",
                    data=sql_query,
                    file_name="query.sql",
                    mime="text/plain"
                )

            except Exception:
                st.error("⚠️ Could not parse Gemini response. Full response:")
                st.json(result)
        else:
            st.error("API Error: " + response.text)
