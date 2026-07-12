#!/bin/bash
# Script para criação massiva de índices otimizados nos clusters Baseline e TLS

echo "Preparando a lista de índices..."

# Bloco com todos os comandos de índice para evitar abrir e fechar a conexão múltiplas vezes
INDEX_COMMANDS="
  print('Criando índices em Users...');
  db.Users.createIndex({ Id: 1 });
  db.Users.createIndex({ Location: 1 });
  db.Users.createIndex({ Reputation: 1 });

  print('Criando índices em Posts...');
  db.Posts.createIndex({ Id: 1 });
  db.Posts.createIndex({ OwnerUserId: 1 });
  db.Posts.createIndex({ ViewCount: -1 });
  db.Posts.createIndex({ Score: -1 });
  db.Posts.createIndex({ AcceptedAnswerId: 1 });
  db.Posts.createIndex({ PostTypeId: 1, Score: -1 });
  db.Posts.createIndex({ PostTypeId: 1, ViewCount: -1 });

  print('Criando índices em Comments...');
  db.Comments.createIndex({ PostId: 1 });
  db.Comments.createIndex({ UserId: 1 });
  db.Comments.createIndex({ CreationDate: 1 });
  db.Comments.createIndex({ Score: 1 });

  print('Criando índices em Votes e PostLinks...');
  db.Votes.createIndex({ PostId: 1 });
  db.PostLinks.createIndex({ PostId: 1 });
  db.PostLinks.createIndex({ RelatedPostId: 1 });

  print('Criando índices em Badges...');
  db.Badges.createIndex({ UserId: 1 });
  db.Badges.createIndex({ Name: 1 });
  db.Badges.createIndex({ Date: 1 });

  print('=== TODOS OS ÍNDICES FORAM CRIADOS COM SUCESSO! ===');
"

echo "========================================="
echo "Aplicando índices no cluster BASELINE..."
echo "========================================="
docker exec -it mongo_base_1 mongosh "mongodb://mongo_base_1:27017,mongo_base_2:27017,mongo_base_3:27017/StackOverflow?replicaSet=rs_baseline" --eval "$INDEX_COMMANDS"

echo -e "\n========================================="
echo "Aplicando índices no cluster TLS..."
echo "========================================="
#docker exec -it mongo_tls_1 mongosh "mongodb://mongo_tls_1:27017,mongo_tls_2:27017,mongo_tls_3:27017/StackOverflow?replicaSet=rs_tls" --tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames --eval "$INDEX_COMMANDS"