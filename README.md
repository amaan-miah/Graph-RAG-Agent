# Graph RAG Agent

A Knowledge-Graph RAG agent built on **Neo4j + Kimchi + Tessl**.

Traditional RAG chunks documents and looks up the most similar chunks. Graph RAG stores data as a **connected graph** and traverses relationships — so it retrieves not just relevant nodes, but everything those nodes are connected to. That's context flat-chunk RAG can't see.

## How it works

1. User asks a question.
2. Agent runs a fulltext search over the Neo4j graph (Movies sample dataset on Aura).
3. For each match, it expands one hop to gather connected nodes and the relationship types.
4. The resulting subgraph is serialized as `(source)-[relationship]->(target)` triples and passed to a Kimchi-hosted LLM.
5. The LLM answers grounded **only** in those triples.

## Stack

- **Neo4j Aura** — managed graph database, free tier, pre-loaded Movies dataset.
- **Kimchi** — free OpenAI-compatible LLM inference.
- **Tessl** — `neo4j-cypher` skill installed so coding agents write correct Cypher first try.

## Setup

### 1. Neo4j Aura

1. Sign up at [console.neo4j.io](https://console.neo4j.io).
2. Create a free instance. **Save the generated password** — you only see it once.
3. Click *Open* and run `:play movies` in the browser to load the sample dataset (if not already loaded).
4. Copy the connection URI (looks like `neo4j+s://xxxxx.databases.neo4j.io`).

### 2. Kimchi

1. Sign up at [kimchi.dev](https://kimchi.dev).
2. Grab your API key.

### 3. Tessl skill (optional but recommended)

```bash
npx tessl install neo4j-cypher
```

This gives any coding agent in this repo proper Neo4j/Cypher knowledge so generated queries work first try.

### 4. Local install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your Neo4j URI/password and Kimchi key
```

## Run

One-shot:

```bash
python agent.py "Who directed The Matrix and what other movies did they make?"
```

Interactive:

```bash
python agent.py
```

## Example questions

- *Who directed The Matrix and what other movies did they make?*
- *What actors worked with Tom Hanks?*
- *Tell me about Keanu Reeves' filmography in this dataset.*

## Files

| File | Purpose |
|---|---|
| `agent.py` | The whole agent — Neo4j search + Kimchi LLM call. |
| `requirements.txt` | Python deps. |
| `.env.example` | Template for credentials. Copy to `.env`. |
| `.gitignore` | Keeps `.env` out of git. |

## Why this matters in 30 seconds

> I built a knowledge-graph RAG agent. Instead of storing documents as flat chunks, the data lives as a connected graph in Neo4j. When you ask a question, the agent traverses relationships — so it doesn't just find relevant nodes, it finds what's connected to them. Traditional RAG misses those connections. Graph RAG doesn't. I used Kimchi for free LLM inference and a Tessl skill to make sure the Cypher queries worked first time.
