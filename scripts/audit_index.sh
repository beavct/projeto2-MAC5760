#!/bin/bash
# Script de Auditoria e Validação de Índices - Baseline vs TLS

# Bloco JavaScript que será executado dentro do MongoDB para validar cada tabela
JS_AUDIT="
  const colecoes = ['Users', 'Posts', 'Comments', 'Votes', 'PostLinks', 'Badges'];
  print('--------------------------------------------------');
  print('RESUMO DE ÍNDICES E INTEGRIDADE:');
  print('--------------------------------------------------');
  
  colecoes.forEach(coll => {
      if (!db.getCollectionNames().includes(coll)) {
          print('[-] ERRO: Coleção ' + coll + ' não existe neste banco!');
          return;
      }
      
      const idxs = db[coll].getIndexes();
      const validacao = db[coll].validate({full: true});
      
      print('=> Coleção: ' + coll);
      print('   Total de índices: ' + idxs.length);
      print('   Chaves criadas:');
      idxs.forEach(i => {
          print('     - Nome: ' + i.name + ' | Definição: ' + JSON.stringify(i.key));
      });
      
      print('   Status de Integridade: ' + (validacao.valid ? ' [OK] ÍNTEGRO' : ' [CORROMPIDO]'));
      if (validacao.errors && validacao.errors.length > 0) {
          print('     ⚠️ ERROS ENCONTRADOS: ' + JSON.stringify(validacao.errors));
      }
      print('--------------------------------------------------');
  });
"

echo "=================================================="
echo " AUDITANDO CLUSTER 1: BASELINE (Sem Criptografia)"
echo "=================================================="
docker exec -i mongo_base_1 mongosh "mongodb://mongo_base_1:27017,mongo_base_2:27017,mongo_base_3:27017/StackOverflow?replicaSet=rs_baseline" --eval "$JS_AUDIT"

echo -e "\n=================================================="
echo " AUDITANDO CLUSTER 2: TLS (Criptografado)"
echo "=================================================="
docker exec -i mongo_tls_1 mongosh "mongodb://mongo_tls_1:27017,mongo_tls_2:27017,mongo_tls_3:27017/StackOverflow?replicaSet=rs_tls" --tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames --eval "$JS_AUDIT"


















