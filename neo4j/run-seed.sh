#!/bin/bash

echo "Neo4j is up. Seeding data..."

# Extract username and password from NEO4J_AUTH environment variable
IFS='/' read -r username password <<< "$NEO4J_AUTH"

# Use the extracted credentials
cypher-shell -u "$username" -p "$password" -f /var/lib/neo4j/import/seed.cypher
