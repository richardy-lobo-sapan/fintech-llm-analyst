# Fintech LLM Analyst

> 🚧 **Work in Progress** — Currently in active development.

A natural language analytics tool for fintech/e-commerce data. Ask questions in plain English, get SQL-powered answers from real data.

---

## What It Does

```
You type:  "What are the top 5 product categories by revenue?"
              ↓
LLM generates SQL query
              ↓
BigQuery runs it against Olist e-commerce data
              ↓
You get a formatted answer + the SQL used
```

---

## Planned Stack

- **Google Gemini** — LLM for understanding questions and writing SQL
- **BigQuery** — Runs SQL against Olist dbt mart tables
- **LangChain** — Text-to-SQL chain
- **Streamlit** — Web UI for asking questions
- **dbt** — Data transformation layer (already built)

---

## Data Source

Built on top of the [Olist Analytics dbt + BigQuery](https://github.com/richardy-lobo-sapan/olist-analytics-dbt) project — a star schema data pipeline covering 100K+ e-commerce orders from Brazil's largest marketplace.

---

## Status

- [x] Data pipeline built (dbt + BigQuery)
- [ ] Text-to-SQL chain
- [ ] BigQuery integration
- [ ] Streamlit UI
- [ ] Deployment

---

## Author

**Richardy Lobo' Sapan**
- GitHub: [@richardy-lobo-sapan](https://github.com/richardy-lobo-sapan)
- LinkedIn: [richardylobosapan](https://www.linkedin.com/in/richardylobosapan/)
