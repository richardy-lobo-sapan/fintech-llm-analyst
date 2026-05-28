# llm.py
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from schema.olist import SCHEMA_CONTEXT
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
    )

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
{schema}

Given the schema above, write a BigQuery SQL query that answers the user's question.
Return ONLY the SQL query. No explanation, no markdown, no backticks.
Just the raw SQL query starting with SELECT.
"""),
    ("human", "{question}")
])

def generate_sql(question: str) -> str:
    llm = get_llm()
    chain = PROMPT | llm | StrOutputParser()
    sql = chain.invoke({
        "schema": SCHEMA_CONTEXT,
        "question": question
    })
    sql = sql.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql