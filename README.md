# 💰 Fintech LLM Analyst — Text-to-SQL with BigQuery

An AI-powered financial analyst that translates plain-English questions into BigQuery SQL, runs the query against real transaction data, and explains the results back in plain English.

**Part of a 5-project LLM Engineering series** · [P1 Chatbot](https://github.com/richardy-lobo-sapan/llm-chatbot-memory) · [P2 RAG](https://github.com/richardy-lobo-sapan/rag-document-qa) · [P3 Agent](https://github.com/richardy-lobo-sapan/ai-agent-tools) · [P4 API](https://github.com/richardy-lobo-sapan/llm-api-production) · **P5 ← You are here**

🔗 **[Live Demo](https://fintech-llm-analyst.streamlit.app)**

---

## What it does

Ask a question in plain English. Get a real answer backed by actual data.

```
You:  "Which merchant category had the highest transaction volume last quarter?"
App:  [generates SQL] → [runs on BigQuery] → [explains the result]
      "Food & Beverage led with 42,318 transactions, followed by..."
```

The LLM handles the translation layer. BigQuery handles the data. The user sees neither — just the answer.

---

## Architecture

```
User question (natural language)
        ↓
   LangChain prompt
        ↓
  Groq (Llama 3.1) — SQL generation
        ↓
   BigQuery — query execution
        ↓
  Groq (Llama 3.1) — result explanation
        ↓
  Streamlit — rendered answer
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Groq API · Llama 3.1 70B |
| Orchestration | LangChain |
| Database | Google BigQuery |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |
| Auth (local) | Service account JSON |
| Auth (cloud) | Streamlit secrets + manual row conversion |

---

## Key Features

- **Natural language → SQL** — no need to know SQL syntax
- **Live BigQuery execution** — queries run against real transaction data, not mocked results
- **Result explanation** — the LLM doesn't just return raw data, it explains what the numbers mean
- **Dual auth** — works locally with a service account JSON, works on Streamlit Cloud via secrets
- **SQL display** — shows the generated query so users can verify and learn

---

## Project Structure

```
fintech-llm-analyst/
├── app.py                  # Streamlit app entry point
├── llm_chain.py            # LangChain chain — question → SQL → explanation
├── bigquery_client.py      # BigQuery connection + query execution
├── prompts.py              # Prompt templates for SQL generation and explanation
├── utils.py                # Row conversion, formatting helpers
├── .env.example            # Environment variable template
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A Google Cloud project with BigQuery enabled
- A service account with BigQuery Data Viewer + Job User roles
- Groq API key (free tier works fine)

### Installation

```bash
git clone https://github.com/richardy-lobo-sapan/fintech-llm-analyst.git
cd fintech-llm-analyst
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file (never commit this):

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
BIGQUERY_PROJECT_ID=your_project_id
BIGQUERY_DATASET_ID=your_dataset_id
```

### Run locally

```bash
streamlit run app.py
```

---

## Deployment (Streamlit Cloud)

1. Push to GitHub (never commit `.env` or your service account JSON)
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) → New app
3. In **Secrets**, add:

```toml
GROQ_API_KEY = "your_groq_api_key"
BIGQUERY_PROJECT_ID = "your_project_id"
BIGQUERY_DATASET_ID = "your_dataset_id"

[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "..."
client_email = "..."
# ... rest of your service account fields
```

> ⚠️ **Gotcha:** `BigQueryClient.to_dataframe()` silently fails on Streamlit Cloud due to `pyarrow` dependency issues. Use manual row conversion instead:
> ```python
> rows = client.query(sql).result()
> data = [dict(row) for row in rows]
> ```

---

## What I Learned

**The LLM is the easy layer.** Most of the engineering work was in the data plumbing — getting BigQuery to authenticate correctly on Streamlit Cloud (service account credentials via secrets, not a JSON file), handling the `pyarrow` incompatibility on the cloud environment, and iterating on the prompt to prevent SQL hallucination (the model would sometimes generate columns that didn't exist).

**Prompt engineering for SQL is different.** You need to give the model the schema upfront, be explicit about table names and column types, and add guardrails to prevent it from making up column names. The prompt does more structural work than in a typical conversational LLM setup.

**LLMs are most useful sitting on top of real data systems, not replacing them.** The model is the interface. BigQuery is the product.

---

## Related Projects

| Project | What it adds |
|---|---|
| [P1 · Aria](https://github.com/richardy-lobo-sapan/llm-chatbot-memory) | Conversation memory, session state |
| [P2 · DocChat](https://github.com/richardy-lobo-sapan/rag-document-qa) | RAG, vector retrieval, ChromaDB |
| [P3 · AI Agent](https://github.com/richardy-lobo-sapan/ai-agent-tools) | Tool use, LangGraph, ReAct loop |
| [P4 · LLM API](https://github.com/richardy-lobo-sapan/llm-api-production) | Production API, Langfuse tracing, Railway |
| **P5 · Fintech LLM Analyst** | **Text-to-SQL, BigQuery, domain application** |

---

## Author

**Richardy Lobo' Sapan** · [LinkedIn](https://www.linkedin.com/in/richardylobosapan/) · [Portfolio](https://richardy-lobo-sapan.github.io)
