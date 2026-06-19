from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

try:
    driver.verify_connectivity()
    print("Connected to Neo4j successfully!")

except Exception as e:
    print(f"Connection failed: {e}")

finally:
    driver.close()