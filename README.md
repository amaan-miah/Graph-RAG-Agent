# GraphMind

A knowledge graph RAG agent built at Hack Night London hosted by Tessl, May 2026.

## What it does

Instead of storing documents as flat chunks and searching by embedding similarity, GraphMind stores data as a connected graph in Neo4j. When you ask a question, the agent traverses relationships — finding not just relevant nodes but everything connected to them. Richer context than traditional vector search without increased latency.

## Demo

Built and demoed to judges at Hack Night London (Tessl, King's Cross) via video submission, May 2026.

## Stack

- **Graph database:** Neo4j (Aura free tier)
- **LLM inference:** Kimchi — OpenAI-compatible endpoint pointing at open-source models, zero API cost
- **Query correctness:** Tessl skills (Neo4j Cypher skill) — ensures generated Cypher queries work first time
- **Language:** Python

## Architectural decisions

**Neo4j over a vector database**
Vector search finds semantically similar chunks but loses relationship information. A graph database preserves relationships explicitly. Ask "Who directed The Matrix?" and Neo4j returns the director, their other films, and their collaborators — not just the movie node.

**Kimchi for LLM inference**
Same OpenAI-compatible interface as Claude or GPT-4. Points at open-source models (GLM 5, Kimi K2.5) with no usage limits and no API cost. Ideal for rapid prototyping and hackathon environments where you want to iterate without burning credits.

**Tessl skills for Cypher correctness**
LLMs frequently generate outdated or incorrect Cypher (Neo4j's query language). Installing the Neo4j Cypher Tessl skill gives the coding agent accurate, up-to-date knowledge of the query syntax, reducing debugging time significantly.

## What I would do next

- Add evaluation harness to measure retrieval quality across query types
- Add LangSmith or Langfuse observability to trace agent decisions
- Replace hardcoded dataset with a configurable document ingestion pipeline
- Add Terraform for reproducible infrastructure deployment

## Built by

Amaan Miah — [github.com/amaan-miah](https://github.com/amaan-miah) — [amaan-miah.github.io](https://amaan-miah.github.io)
