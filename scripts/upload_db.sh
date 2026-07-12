#!/bin/bash
# Importa dados de dentro da rede virtual (mongo_net) direto para os Replica Sets

echo "Iniciando importação de dados no Cluster..."

DIR="db_data"

for f in "$DIR"/*.csv; do
    colecao=$(basename "$f" .csv)
    echo "--- Processando: $colecao ---"
    
    # 1. Importar no Baseline (Comunicação Intra-Rede)
    #echo "Enviando para o Cluster Baseline..."
    #docker run --rm --network projeto_seguranca_mongo_net -v "$(pwd)/$DIR:/data" mongo:latest mongoimport \
    #    --uri "mongodb://mongo_base_1:27017,mongo_base_2:27017,mongo_base_3:27017/StackOverflow?replicaSet=rs_baseline" \
    #    --collection "$colecao" --type csv --headerline --file "/data/$(basename "$f")"

    # 2. Importar no TLS (Forçando o bypass de certificado via flags SSL externas)
    echo "Enviando para o Cluster TLS..."
    docker run --rm --network projeto_seguranca_mongo_net -v "$(pwd)/$DIR:/data" mongo:latest mongoimport \
        --host "rs_tls/mongo_tls_1:27017,mongo_tls_2:27017,mongo_tls_3:27017" \
        --ssl \
        --sslAllowInvalidCertificates \
        --sslAllowInvalidHostnames \
        --db StackOverflow \
        --collection "$colecao" --type csv --headerline --file "/data/$(basename "$f")"

    if [ $? -eq 0 ]; then
        echo "Sucesso: $colecao importado nos clusters."
    else
        echo "Atenção: Houve um erro na importação de $colecao."
    fi
done

echo "Processo de importação finalizado com sucesso."
