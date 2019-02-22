# Dockerfile for the Neo4j database

FROM neo4j:3.4.8

LABEL Name=pgdb-database Version=0.1
EXPOSE 7474

WORKDIR /pgdb-database

# Copy the database dump to the container
COPY neo4j.human.mouse.400.dump /pgdb-database

# Load the database dump
RUN neo4j-admin load --from=/pgdb-database/neo4j.human.mouse.400.dump --database=graph.db --force
