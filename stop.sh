#!/usr/bin/env bash

# Stop and destroy the containers
docker rm -f neo4j health_app_backend

# 
# sed -i '' '/^URI=/d' .env.dev
