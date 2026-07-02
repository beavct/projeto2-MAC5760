#!/bin/bash
# Script: limpar_bancos.sh
# Apaga todas as coleções do banco StackOverflow nos dois nós (Baseline e TLS)

echo "Apagando coleções do Baseline (27017)..."
docker exec -it mongo_baseline mongosh "StackOverflow" --eval "db.dropDatabase()"

echo "Apagando coleções do TLS (27018)..."
docker exec -it mongo_tls mongosh --tls --tlsAllowInvalidCertificates "StackOverflow" --eval "db.dropDatabase()"

echo "Bancos limpos com sucesso!"