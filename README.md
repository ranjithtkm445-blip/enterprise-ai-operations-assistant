---
title: Enterprise AI Operations Assistant
emoji: 🤖
colorFrom: indigo
colorTo: blue
sdk: gradio
sdk_version: 6.20.0
app_file: app.py
pinned: false
---

# Enterprise AI Operations Assistant

A multi-agent business automation demo built with **CrewAI** + **Groq** (llama-3.3-70b).

A hierarchical **Manager Agent** receives a user request, delegates to **Inventory**, **Sales**,
and **Customer Support** specialist agents as needed, then combines their outputs into one
structured response.

## Try these queries

- Check stock for 100 laptops and prepare a quotation with 5% discount.
- Do we have 500 hard disks in stock?
- What is our refund policy for bulk orders?
- What is the warranty on monitors?

## How it works

```
User Query
    ↓
Manager Agent (Groq LLM)
    ↓ delegates
┌───────────────┬──────────────┬──────────────────┐
Inventory Agent  Sales Agent   Support Agent
(SQL lookup)    (Quotation)   (RAG / policy docs)
    ↓               ↓               ↓
SQLite DB       SQLite DB      ChromaDB
    └───────────────┴───────────────┘
                    ↓
           Merged Final Response
```

Every number comes from the **SQLite database** — the LLM never invents figures.
Policy answers come from **ChromaDB** vector search over company documents.

## Stack

| Layer | Technology |
|---|---|
| Agents | CrewAI (hierarchical process) |
| LLM | Groq — llama-3.3-70b-versatile |
| Structured data | SQLite + SQLAlchemy |
| RAG | ChromaDB over local policy docs |
| UI | Gradio |

## Setup (local)

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
cp .env.example .env         # add your GROQ_API_KEY
python app.py
```

## Hugging Face Spaces

Add your `GROQ_API_KEY` as a **Secret** in Space Settings → Variables and secrets.
