import subprocess
import time
import statistics
import csv
import re
import os

# Configurações do Experimento
MAPA_QUERIES = {
    "AGRUPAMENTO": 6, 
    "JUNCAO": 7, 
    "SUBCONSULTA": 5, 
    "BUSCA": 2, 
    "INSERCAO": 5, 
    "MODIFICACAO": 5
}
REPETICOES = 20
LOG_FILE = "resultados.csv"
ARQUIVO_QUERIES = "./consultas/queries.js"
TEMP_FILE = "temp_query.js"

def carregar_queries(filepath):
    queries = {k: {} for k in MAPA_QUERIES.keys()}
    current_type = None
    current_idx = None
    buffer = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith("// --- TIPO"):
                if current_type and current_idx and buffer:
                    query_str = " ".join(buffer).strip()
                    if query_str.endswith(','): query_str = query_str[:-1]
                    queries[current_type][current_idx] = query_str
                
                if "TIPO 1" in stripped: current_type = "AGRUPAMENTO"; current_idx = None; buffer = []; continue
                if "TIPO 2" in stripped: current_type = "JUNCAO"; current_idx = None; buffer = []; continue
                if "TIPO 3" in stripped: current_type = "SUBCONSULTA"; current_idx = None; buffer = []; continue
                if "TIPO 4" in stripped: current_type = "BUSCA"; current_idx = None; buffer = []; continue
                if "TIPO 5" in stripped: current_type = "INSERCAO"; current_idx = None; buffer = []; continue
                if "TIPO 6" in stripped: current_type = "MODIFICACAO"; current_idx = None; buffer = []; continue

            # Detecta o início de uma nova query (ex: "// 1.", "// 2.")
            match = re.match(r"^//\s*(\d+)\.", stripped)
            if match and current_type:
                if current_idx is not None and buffer:
                    # Salva a query anterior acumulada no buffer
                    query_str = " ".join(buffer).strip()
                    # Remove vírgulas residuais no final da string se houver
                    if query_str.endswith(','): query_str = query_str[:-1]
                    queries[current_type][current_idx] = query_str
                
                current_idx = int(match.group(1))
                buffer = []
                continue

            # Acumula as linhas da query ativa
            if current_type and current_idx and not stripped.startswith("//"):
                buffer.append(stripped)

        # Salva a última query pendente após o fim do arquivo
        if current_type and current_idx and buffer:
            query_str = " ".join(buffer).strip()
            if query_str.endswith(','): query_str = query_str[:-1]
            queries[current_type][current_idx] = query_str

    return queries

# Carrega as queries uma única vez na inicialização
QUERIES_CARREGADAS = carregar_queries(ARQUIVO_QUERIES)

def rodar_query_mongo(tipo, index, conn_string):
    """Salva a query num arquivo temporário e executa via mongosh."""
    query_text = QUERIES_CARREGADAS[tipo].get(index)
    if not query_text:
        print(f"  [ERRO] Query {index} do tipo {tipo} não encontrada no parser!")
        return 0
    
    # Grava a query em um .js temporário (Evita quebra de aspas no terminal)
    with open(TEMP_FILE, "w", encoding='utf-8') as f:
        f.write(query_text)

    # Executa o arquivo temporário diretamente pelo mongosh
    cmd = f'mongosh "{conn_string}" --quiet {TEMP_FILE}'
    
    start = time.perf_counter()
    subprocess.run(cmd, shell=True, capture_output=True)
    end = time.perf_counter()
    
    return end - start

def executar_benchmark():
    with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tipo', 'Query_Index', 'Cenario', 'P50', 'P95', 'P99', 'Vazao_ops_sec'])

        for tipo, qtd in MAPA_QUERIES.items():
            print(f"\n========================================")
            print(f"INICIANDO BATERIA: {tipo}")
            print(f"========================================")
            
            for i in range(1, qtd + 1):
                tempos_b, tempos_t = [], []
                print(f"  -> Rodando Query {i}/{qtd}...")
                
                # URIs com o banco especificado para evitar que execute no banco 'test'
                conn_baseline = "mongodb://localhost:27017/StackOverflow"
                conn_tls = "mongodb://localhost:27018/StackOverflow?tls=true&tlsAllowInvalidCertificates=true"

                # 1. Warm-up (Garante que os dados vão para o cache do SO e motor WiredTiger)
                rodar_query_mongo(tipo, i, conn_baseline)
                rodar_query_mongo(tipo, i, conn_tls)

                # 2. Medições Oficiais
                for _ in range(REPETICOES):
                    tempos_b.append(rodar_query_mongo(tipo, i, conn_baseline))
                    tempos_t.append(rodar_query_mongo(tipo, i, conn_tls))
                
                # 3. Cálculo e Log
                if sum(tempos_b) > 0 and sum(tempos_t) > 0:
                    met_b = calcular_metricas(tempos_b)
                    met_t = calcular_metricas(tempos_t)
                    
                    writer.writerow([tipo, i, 'Baseline', met_b['p50'], met_b['p95'], met_b['p99'], met_b['vazao']])
                    writer.writerow([tipo, i, 'TLS', met_t['p50'], met_t['p95'], met_t['p99'], met_t['vazao']])
    
    # Cleanup do arquivo temporário
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)
    print("\nBENCHMARK CONCLUÍDO! Resultados salvos em:", LOG_FILE)

def calcular_metricas(tempos):
    tempos.sort()
    vazao = len(tempos) / sum(tempos) if sum(tempos) > 0 else 0
    return {
        "p50": statistics.median(tempos),
        "p95": tempos[int(len(tempos) * 0.95)],
        "p99": tempos[int(len(tempos) * 0.99)],
        "vazao": round(vazao, 4)
    }

if __name__ == "__main__":
    executar_benchmark()