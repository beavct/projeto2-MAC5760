#!/bin/bash
# Script: importar_ambos.sh
# Importa os dados da pasta 'db_data' para os dois nós do MongoDB (Baseline e TLS)

echo "Iniciando importação de dados..."

# O diretório que contém os arquivos é o db_data
DIR="db_data"

for f in "$DIR"/*.csv; do
    colecao=$(basename "$f" .csv)
    echo "--- Processando: $colecao ---"
    
    # 1. Importar no Baseline (porta 27017, sem TLS)
    echo "Enviando para Baseline (27017)..."
    docker run --rm -v "$(pwd)/$DIR:/data" mongo:latest mongoimport \
        --host host.docker.internal --port 27017 \
        --db StackOverflow --collection "$colecao" --type csv --headerline --file "/data/$(basename "$f")"

    # 2. Importar no TLS (porta 27018, com TLS)
    echo "Enviando para TLS (27018)..."
    docker run --rm -v "$(pwd)/$DIR:/data" mongo:latest mongoimport \
        --ssl \
        --sslAllowInvalidCertificates \
        --host host.docker.internal --port 27018 \
        --db StackOverflow --collection "$colecao" --type csv --headerline --file "/data/$(basename "$f")"

    if [ $? -eq 0 ]; then
        echo "Sucesso: $colecao importado nos dois nós."
    else
        echo "Atenção: Houve um erro na importação de $colecao."
    fi
done

echo "Processo de importação finalizado com sucesso."