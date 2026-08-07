"""
Neo4j Graph Migration
=====================

Copies the complete graph from a local Neo4j Docker instance
to a Neo4j Aura database.

Features
--------
- Copies all nodes
- Copies all labels
- Copies all node properties
- Copies all relationships
- Copies all relationship properties
- Batch processing
- Progress logging
- Verification

Author: Sujina
"""

from __future__ import annotations

import logging

from neo4j import Driver, GraphDatabase

# ============================================================
# Configuration
# ============================================================

SOURCE_URI = "bolt://localhost:7687"
SOURCE_USERNAME = "neo4j"
SOURCE_PASSWORD = "password"

DEST_URI = "neo4j+s://af5f94ff.databases.neo4j.io"
DEST_USERNAME = "af5f94ff"
DEST_PASSWORD = "BDWNMmPaKq1zNmt-BxCWfI-xM7LECR577vOarnecr9U"

BATCH_SIZE = 500


# ============================================================
# Logging
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# Neo4j Migrator
# ============================================================

class Neo4jMigrator:
    """
    Migrates an entire Neo4j graph from one database to another.
    """

    def __init__(self):

        self.source_driver: Driver = GraphDatabase.driver(
            SOURCE_URI,
            auth=(
                SOURCE_USERNAME,
                SOURCE_PASSWORD,
            ),
        )

        self.dest_driver: Driver = GraphDatabase.driver(
            DEST_URI,
            auth=(
                DEST_USERNAME,
                DEST_PASSWORD,
            ),
        )

        # old node id -> new node id
        self.node_mapping: dict[int, int] = {}

    # =========================================================

    def close(self):

        self.source_driver.close()
        self.dest_driver.close()

    # =========================================================

    def test_connections(self):

        logger.info("Testing database connections...")

        with self.source_driver.session() as session:
            session.run("RETURN 1").single()

        logger.info("✓ Source database connected.")

        with self.dest_driver.session() as session:
            session.run("RETURN 1").single()

        logger.info("✓ Destination database connected.")

    # =========================================================

    def clear_destination(self):

        logger.info("Clearing destination database...")

        with self.dest_driver.session() as session:

            session.run("""
                MATCH (n)
                DETACH DELETE n
            """)

        logger.info("✓ Destination cleared.")

    # =========================================================

    def count_source(self):

        with self.source_driver.session() as session:

            nodes = session.run("""
                MATCH (n)
                RETURN count(n) AS count
            """).single()["count"]

            relationships = session.run("""
                MATCH ()-[r]->()
                RETURN count(r) AS count
            """).single()["count"]

        logger.info("Source Nodes          : %s", nodes)
        logger.info("Source Relationships  : %s", relationships)

        return nodes, relationships

    # =========================================================

    def count_destination(self):

        with self.dest_driver.session() as session:

            nodes = session.run("""
                MATCH (n)
                RETURN count(n) AS count
            """).single()["count"]

            relationships = session.run("""
                MATCH ()-[r]->()
                RETURN count(r) AS count
            """).single()["count"]

        logger.info("Destination Nodes         : %s", nodes)
        logger.info("Destination Relationships : %s", relationships)

        return nodes, relationships

    # =========================================================

       # =========================================================

    def migrate_nodes(self):
        """
        Copy all nodes from the source database to
        the destination database while preserving
        labels and properties.

        Stores the mapping:
            source_node_id -> destination_node_id
        """

        logger.info("")
        logger.info("=" * 70)
        logger.info("Starting Node Migration")
        logger.info("=" * 70)

        with (
            self.source_driver.session() as source,
            self.dest_driver.session() as dest,
        ):

            records = source.run(
                """
                MATCH (n)
                RETURN
                    id(n) AS id,
                    labels(n) AS labels,
                    properties(n) AS props
                ORDER BY id(n)
                """
            )

            count = 0

            for record in records:

                source_id = record["id"]
                labels = record["labels"]
                props = record["props"]

                # ---------------------------------------------
                # Build CREATE statement dynamically
                # ---------------------------------------------

                if labels:
                    label_string = ":" + ":".join(labels)
                else:
                    label_string = ""

                query = f"""
                CREATE (n{label_string})
                SET n += $props
                RETURN id(n) AS id
                """

                result = dest.run(
                    query,
                    props=props,
                ).single()

                destination_id = result["id"]

                self.node_mapping[source_id] = destination_id

                count += 1

                if count % BATCH_SIZE == 0:

                    logger.info(
                        "Nodes migrated : %s",
                        count,
                    )

            logger.info("")
            logger.info("✓ Total Nodes Migrated : %s", count)
            logger.info(
                "✓ Mapping Entries      : %s",
                len(self.node_mapping),
            )

            logger.info("=" * 70)
                # =========================================================

    def print_node_summary(self):

        logger.info("")
        logger.info("Node Mapping Summary")

        logger.info(
            "Mapped Nodes : %s",
            len(self.node_mapping),
        )

        if self.node_mapping:

            first = next(iter(self.node_mapping.items()))

            logger.info(
                "Example Mapping : %s -> %s",
                first[0],
                first[1],
            )

        # =========================================================

    def migrate_relationships(self):
        """
        Copy all relationships from the source database
        to the destination database.

        Uses the node mapping created during node migration
        to reconnect relationships correctly.
        """

        logger.info("")
        logger.info("=" * 70)
        logger.info("Starting Relationship Migration")
        logger.info("=" * 70)

        with (
            self.source_driver.session() as source,
            self.dest_driver.session() as dest,
        ):

            records = source.run(
                """
                MATCH (a)-[r]->(b)
                RETURN
                    id(a) AS start_id,
                    id(b) AS end_id,
                    type(r) AS rel_type,
                    properties(r) AS props
                """
            )

            count = 0

            for record in records:

                old_start = record["start_id"]
                old_end = record["end_id"]

                rel_type = record["rel_type"]
                props = record["props"]

                # Skip relationships if a mapped node is missing
                if (
                    old_start not in self.node_mapping
                    or old_end not in self.node_mapping
                ):
                    logger.warning(
                        "Skipping relationship because node mapping is missing."
                    )
                    continue

                new_start = self.node_mapping[old_start]
                new_end = self.node_mapping[old_end]

                query = f"""
                MATCH (a)
                WHERE id(a)=$start_id

                MATCH (b)
                WHERE id(b)=$end_id

                CREATE (a)-[r:{rel_type}]->(b)

                SET r += $props

                RETURN id(r)
                """

                dest.run(
                    query,
                    start_id=new_start,
                    end_id=new_end,
                    props=props,
                )

                count += 1

                if count % BATCH_SIZE == 0:

                    logger.info(
                        "Relationships migrated : %s",
                        count,
                    )

            logger.info("")
            logger.info(
                "✓ Total Relationships Migrated : %s",
                count,
            )

            logger.info("=" * 70)
                # =========================================================

    def print_relationship_summary(self):

        with self.dest_driver.session() as session:

            result = session.run(
                """
                MATCH ()-[r]->()
                RETURN
                    type(r) AS relationship,
                    count(r) AS total
                ORDER BY total DESC
                """
            )

            logger.info("")
            logger.info("Relationship Summary")
            logger.info("-" * 40)

            for record in result:

                logger.info(
                    "%-30s %6d",
                    record["relationship"],
                    record["total"],
                )

    # =========================================================

    def verify(self):

        source_nodes, source_relationships = self.count_source()

        dest_nodes, dest_relationships = self.count_destination()

        print()

        if (
            source_nodes == dest_nodes
            and source_relationships == dest_relationships
        ):
            logger.info("✓ Migration verified successfully.")
        else:
            logger.error("✗ Verification failed.")
            logger.error(
                "Source (%s, %s) Destination (%s, %s)",
                source_nodes,
                source_relationships,
                dest_nodes,
                dest_relationships,
            )
# ============================================================
# Main
# ============================================================

import time


def main():

    start_time = time.time()

    logger.info("")
    logger.info("=" * 70)
    logger.info("Neo4j Graph Migration")
    logger.info("=" * 70)

    migrator = Neo4jMigrator()

    try:

        # ----------------------------------------------------
        # Test Connections
        # ----------------------------------------------------
        migrator.test_connections()

        # ----------------------------------------------------
        # Source Statistics
        # ----------------------------------------------------
        logger.info("")
        logger.info("Source Database Statistics")
        migrator.count_source()

        # ----------------------------------------------------
        # Clear Destination
        # ----------------------------------------------------
        migrator.clear_destination()

        # ----------------------------------------------------
        # Copy Nodes
        # ----------------------------------------------------
        migrator.migrate_nodes()

        # ----------------------------------------------------
        # Copy Relationships
        # ----------------------------------------------------
        migrator.migrate_relationships()

        # ----------------------------------------------------
        # Verification
        # ----------------------------------------------------
        logger.info("")
        logger.info("=" * 70)
        logger.info("Verification")
        logger.info("=" * 70)

        migrator.verify()

        logger.info("")
        migrator.print_node_summary()

        logger.info("")
        migrator.print_relationship_summary()

    except Exception:

        logger.exception("Migration failed.")
        raise 

    finally:

        migrator.close()

    elapsed = time.time() - start_time

    logger.info("")
    logger.info("=" * 70)
    logger.info("Migration Completed Successfully")
    logger.info("=" * 70)

    logger.info("Execution Time : %.2f seconds", elapsed)


# ============================================================

if __name__ == "__main__":
    main()