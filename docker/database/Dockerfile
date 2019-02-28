# Dockerfile for the Neo4j database

FROM neo4j:3.4.8
LABEL Name=pgdb-database Version=0.1

# Credentials
ENV NEO4J_PASSWD pgdb
ENV NEO4J_AUTH neo4j/${NEO4J_PASSWD}

# Copy the database dump to the container
COPY neo4j.human.mouse.400.dump /var/lib/neo4j/import/

# Run
CMD neo4j-admin set-initial-password ${NEO4J_PASSWD} || true && \
    neo4j-admin load --from=/var/lib/neo4j/import/neo4j.human.mouse.400.dump --database=graph.db --force && \
    neo4j console
