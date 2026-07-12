#!/bin/bash
# Verifica o estado dos bancos de dados nos clusters Baseline e TLS

echo "=========================================="
echo "DIAGNÓSTICO: BASELINE (Nó: mongo_base_1)"
echo "=========================================="
docker exec -it mongo_base_1 mongosh --eval "
  print('Bancos existentes: ' + db.getMongo().getDBNames());
  print('--- Conteúdo do StackOverflow ---');
  db.getSiblingDB('StackOverflow').getCollectionNames().forEach(function(col) {
    print('Coleção: ' + col + ' | Docs: ' + db.getSiblingDB('StackOverflow').getCollection(col).countDocuments());
  });
"

echo -e "\n=========================================="
echo "DIAGNÓSTICO: TLS (Nó: mongo_tls_1)"
echo "=========================================="
docker exec -it mongo_tls_1 mongosh --tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames --eval "
  print('Bancos existentes: ' + db.getMongo().getDBNames());
  print('--- Conteúdo do StackOverflow ---');
  db.getSiblingDB('StackOverflow').getCollectionNames().forEach(function(col) {
    print('Coleção: ' + col + ' | Docs: ' + db.getSiblingDB('StackOverflow').getCollection(col).countDocuments());
  });
"