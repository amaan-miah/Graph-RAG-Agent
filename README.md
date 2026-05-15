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
3. Copy the connection URI (looks like `neo4j+s://xxxxx.databases.neo4j.io`).
4. The Movies sample is loaded by `load_sample.py` below — you do not need to manually run `:play movies`.

### 2. Kimchi

1. Sign up at [kimchi.dev](https://kimchi.dev).
2. Grab your API key (starts with `castai_v1_`).
3. Note: the OpenAI-compatible base URL is `https://llm.cast.ai/openai/v1` (Kimchi is hosted on CAST AI's LLM hub).
4. Available models include `kimi-k2.6`, `kimi-k2.5`, `minimax-m2.7`, `minimax-m2.5`, `qwen3-coder-next-fp8`, `nemotron-3-super-fp4`, `smollm2-360m`, `smollm2-135m`.

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
python load_sample.py   # populates Aura with the Movies dataset
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
| `agent.py` | The whole agent — Neo4j 2-hop search + Kimchi LLM call. |
| `load_sample.py` | One-shot loader for the canonical Neo4j Movies sample. |
| `requirements.txt` | Python deps. |
| `.env.example` | Template for credentials. Copy to `.env`. |
| `.gitignore` | Keeps `.env` out of git. |
| `tessl.json`, `.tessl/`, `.mcp.json` | Tessl `neo4j-cypher-skill` so coding agents write correct Cypher. |

## Why this matters in 30 seconds

> I built a knowledge-graph RAG agent. Instead of storing documents as flat chunks, the data lives as a connected graph in Neo4j. When you ask a question, the agent traverses relationships — so it doesn't just find relevant nodes, it finds what's connected to them. Traditional RAG misses those connections. Graph RAG doesn't. I used Kimchi for free LLM inference and a Tessl skill to make sure the Cypher queries worked first time.
