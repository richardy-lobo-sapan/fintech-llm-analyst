# app.py
# This is the Streamlit UI — the frontend the user interacts with.
# It has ONE job: take user input, call llm.py and bigquery_client.py,
# and display the results. It doesn't know HOW SQL is generated or
# HOW BigQuery is queried — it just wires everything together.

import streamlit as st
from llm import generate_sql
from bigquery_client import run_query

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Olist LLM Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Olist LLM Analyst")
st.markdown("Ask questions about the Olist e-commerce dataset in plain English.")

# ─── EXAMPLE QUESTIONS ──────────────────────────────────────────────────────
# These help users understand what they can ask
st.markdown("**Example questions:**")
examples = [
    "What are the top 5 cities by total revenue?",
    "How many orders were delivered vs canceled?",
    "What is the average delivery days per state?",
    "Which payment type is most popular?",
    "What is the total revenue per month in 2018?",
]
for ex in examples:
    st.markdown(f"- {ex}")

st.divider()

# ─── INPUT ──────────────────────────────────────────────────────────────────
question = st.text_input(
    label="Your question",
    placeholder="e.g. What are the top 10 states by number of orders?",
)

run_button = st.button("Ask", type="primary")

# ─── MAIN LOGIC ─────────────────────────────────────────────────────────────
# This only runs when the user clicks the Ask button
if run_button and question:

    # Step 1: Generate SQL from the question
    with st.spinner("Generating SQL..."):
        try:
            sql = generate_sql(question)
        except Exception as e:
            st.error(f"Failed to generate SQL: {e}")
            st.stop()   # stops execution here if SQL generation fails

    # Step 2: Show the generated SQL so user can see and learn from it
    st.markdown("**Generated SQL:**")
    st.code(sql, language="sql")

    # Step 3: Run the SQL on BigQuery
    with st.spinner("Running query on BigQuery..."):
        try:
            df = run_query(sql)
        except Exception as e:
            st.error(f"BigQuery error: {e}")
            st.stop()

    # Step 4: Display results
    st.markdown(f"**Results** ({len(df)} rows):")
    st.dataframe(df, use_container_width=True)

elif run_button and not question:
    st.warning("Please enter a question first.")