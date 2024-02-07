#!/usr/bin/env bash

# Stop and destroy the containers
docker rm -f neo4j health_app

# 
# sed -i '' '/^URI=/d' .env.dev
