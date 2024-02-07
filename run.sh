#!/usr/bin/env bash

# Run neo4j database
# -p7687:7687
docker run \
    --name neo4j \
    -p7474:7474  \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --env NEO4J_AUTH=neo4j/password \
    --env NEO4J_server_https_advertised__address="localhost:7473" \
	--env NEO4J_server_http_advertised__address="localhost:7474" \
	--env NEO4J_server_bolt_advertised__address="localhost:7687" \
    neo4j:latest

sleep 5

# echo "NEO4J_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' neo4j)" >> .env.dev
# sed -i '' 's/^URI=.*/URI='"$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' neo4j)"'/' .env
NEO4J_IP=$(docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' neo4j)
echo $NEO4J_IP
if grep -q "^NEO4J_IP=" .env.dev; then
    sed -i '' 's|^NEO4J_IP=.*|NEO4J_IP='"$NEO4J_IP"'|' .env.dev
else
    echo "NEO4J_IP=$NEO4J_IP" >> .env.dev
fi

# Run the backend app
docker build -t health_app_image .
docker run \
    --name health_app \
    -d \
    -p8000:8000 \
    --env-file .env.dev \
    health_app_image
