FROM neo4j:5.18

# Install required tools
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy seed files
COPY run-seed.sh /docker-entrypoint-initdb.d/
COPY seed.cypher /var/lib/neo4j/import/

# Make seed script executable
RUN chmod +x /docker-entrypoint-initdb.d/run-seed.sh

# Create a custom entrypoint script
COPY docker-entrypoint.sh /startup/custom-entrypoint.sh
RUN chmod +x /startup/custom-entrypoint.sh

ENTRYPOINT ["/startup/custom-entrypoint.sh"]
CMD ["neo4j"]
