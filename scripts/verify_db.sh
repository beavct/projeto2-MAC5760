#!/bin/bash
# Script: verificar_banco.sh
# Verifica o estado dos bancos de dados Baseline e TLS

echo "=========================================="
echo "DIAGNÓSTICO: BASELINE (27017)"
echo "=========================================="
docker exec -it mongo_baseline mongosh --eval "
  print('Bancos existentes: ' + db.getMongo().getDBNames());
  print('--- Conteúdo do StackOverflow ---');
  db.getSiblingDB('StackOverflow').getCollectionNames().forEach(function(col) {
    print('Coleção: ' + col + ' | Docs: ' + db.getSiblingDB('StackOverflow').getCollection(col).countDocuments());
  });
"

echo -e "\n=========================================="
echo "DIAGNÓSTICO: TLS (27018)"
echo "=========================================="
docker exec -it mongo_tls mongosh --tls --tlsAllowInvalidCertificates --eval "
  print('Bancos existentes: ' + db.getMongo().getDBNames());
  print('--- Conteúdo do StackOverflow ---');
  db.getSiblingDB('StackOverflow').getCollectionNames().forEach(function(col) {
    print('Coleção: ' + col + ' | Docs: ' + db.getSiblingDB('StackOverflow').getCollection(col).countDocuments());
  });
"