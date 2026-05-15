"""Knowledge Graph RAG Agent — Neo4j + Kimchi.

Asks a question, retrieves connected context from a Neo4j graph, and lets an
LLM answer grounded in that subgraph. Built for the Movies sample dataset that
ships with Neo4j Aura.
"""

import os
import sys
import textwrap

from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.exceptions import ClientError
from openai import OpenAI

load_dotenv()

NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ["NEO4J_PASSWORD"]

KIMCHI_API_KEY = os.environ["KIMCHI_API_KEY"]
KIMCHI_BASE_URL = os.getenv("KIMCHI_BASE_URL", "https://api.kimchi.dev/v1")
KIMCHI_MODEL = os.getenv("KIMCHI_MODEL", "gpt-4o-mini")

FULLTEXT_INDEX = "movieSearch"

client = OpenAI(api_key=KIMCHI_API_KEY, base_url=KIMCHI_BASE_URL)
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def ensure_fulltext_index() -> None:
    """Create the fulltext index on the Movies sample if it doesn't exist yet."""
    with driver.session() as session:
        session.run(
            f"""
            CREATE FULLTEXT INDEX {FULLTEXT_INDEX} IF NOT EXISTS
            FOR (n:Movie|Person)
            ON EACH [n.title, n.tagline, n.name]
            """
        )


def search_graph(query: str) -> list[dict]:
    """Find matching nodes via fulltext, then expand one hop to get relationships."""
    cypher = f"""
        CALL db.index.fulltext.queryNodes('{FULLTEXT_INDEX}', $query)
        YIELD node, score
        MATCH (node)-[r]-(connected)
        RETURN
            coalesce(node.title, node.name)        AS source,
            labels(node)[0]                        AS source_type,
            node.tagline                           AS tagline,
            type(r)                                AS relationship,
            coalesce(connected.title, connected.name) AS target,
            labels(connected)[0]                   AS target_type,
            score
        ORDER BY score DESC
        LIMIT 25
    """
    with driver.session() as session:
        result = session.run(cypher, query=query)
        return [dict(record) for record in result]


def format_context(rows: list[dict]) -> str:
    if not rows:
        return "(no matching nodes found in the graph)"
    lines = []
    for r in rows:
        lines.append(
            f"- ({r['source_type']}: {r['source']}) "
            f"-[{r['relationship']}]-> "
            f"({r['target_type']}: {r['target']})"
            + (f"   // tagline: {r['tagline']}" if r.get("tagline") else "")
        )
    return "\n".join(lines)


SYSTEM_PROMPT = textwrap.dedent(
    """
    You answer questions using ONLY the provided knowledge-graph context.
    The context is a list of (source)-[relationship]->(target) triples from a Neo4j graph.
    Cite the specific relationships you used. If the context is insufficient, say so plainly
    instead of guessing.
    """
).strip()


def answer_question(question: str) -> str:
    rows = search_graph(question)
    context = format_context(rows)
    response = client.chat.completions.create(
        model=KIMCHI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Graph context:\n{context}\n\nQuestion: {question}",
            },
        ],
    )
    return response.choices[0].message.content


def main() -> None:
    try:
        ensure_fulltext_index()
    except ClientError as e:
        print(f"[warn] could not create fulltext index: {e}", file=sys.stderr)

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        print(answer_question(question))
        return

    print("Graph RAG Agent — ask a question (Ctrl-C to quit)")
    while True:
        try:
            question = input("\n? ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not question:
            continue
        print()
        print(answer_question(question))


if __name__ == "__main__":
    try:
        main()
    finally:
        driver.close()
