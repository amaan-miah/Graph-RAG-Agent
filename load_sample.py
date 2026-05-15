"""One-shot loader for Neo4j's canonical Movies sample dataset.

Aura free instances don't always come pre-loaded — run this once after
setting up .env to populate the graph.
"""

import os
import re
import urllib.request

from dotenv import load_dotenv
from neo4j import GraphDatabase

MOVIES_CYPHER_URL = (
    "https://raw.githubusercontent.com/"
    "neo4j-graph-examples/movies/main/scripts/movies.cypher"
)


def main() -> None:
    load_dotenv()
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.getenv("NEO4J_USER", "neo4j"), os.environ["NEO4J_PASSWORD"]),
    )

    print(f"Fetching {MOVIES_CYPHER_URL}")
    with urllib.request.urlopen(MOVIES_CYPHER_URL) as resp:
        script = resp.read().decode()

    script = re.sub(r"//[^\n]*", "", script)
    statements = [s.strip() for s in script.split(";") if s.strip()]
    print(f"Executing {len(statements)} statements...")

    with driver.session() as session:
        for stmt in statements:
            session.run(stmt)

    with driver.session() as session:
        counts = session.run(
            "MATCH (n) RETURN labels(n)[0] AS label, count(*) AS n ORDER BY n DESC"
        ).data()
    for c in counts:
        print(f"  {c['label']}: {c['n']}")
    print("Load complete.")
    driver.close()


if __name__ == "__main__":
    main()
