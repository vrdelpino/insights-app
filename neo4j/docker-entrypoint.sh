#!/bin/bash
set -e

# Function to check if Neo4j is ready
wait_for_neo4j() {
    echo "Waiting for Neo4j to be ready..."
    while ! curl -s http://localhost:7474 > /dev/null; do
        sleep 1
    done
    echo "Neo4j is ready!"
}

# Start Neo4j in the background using the original entrypoint
echo "Starting Neo4j..."
/startup/docker-entrypoint.sh neo4j &

# Wait for Neo4j to be ready
wait_for_neo4j

# Run the seed script
echo "Running seed script..."
/docker-entrypoint-initdb.d/run-seed.sh

# Keep the container running
wait 