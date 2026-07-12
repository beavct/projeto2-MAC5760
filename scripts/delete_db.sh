#!/bin/bash
# Apaga todas as coleções do banco StackOverflow nos dois nós primários

echo "Apagando coleções do Baseline (mongo_base_1)..."
docker exec -it mongo_base_1 mongosh "StackOverflow" --eval "db.dropDatabase()"

echo "Apagando coleções do TLS (mongo_tls_1)..."
docker exec -it mongo_tls_1 mongosh --tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames "StackOverflow" --eval "db.dropDatabase()"

echo "Bancos limpos com sucesso!"