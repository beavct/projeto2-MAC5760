import subprocess
import time
import statistics
import csv
import re
import os

# Configurações do Experimento
MAPA_QUERIES = {
    "AGRUPAMENTO": 6,
}
REPETICOES = 20
LOG_FILE = "resultados_mestrado.csv"
ARQUIVO_QUERIES = "./consultas/queries.js"

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
                #if "TIPO 2" in stripped: current_type = "JUNCAO"; current_idx = None; buffer = []; continue
                #if "TIPO 3" in stripped: current_type = "SUBCONSULTA"; current_idx = None; buffer = []; continue
                #if "TIPO 4" in stripped: current_type = "BUSCA"; current_idx = None; buffer = []; continue
                #if "TIPO 5" in stripped: current_type = "INSERCAO"; current_idx = None; buffer = []; continue
                #if "TIPO 6" in stripped: current_type = "MODIFICACAO"; current_idx = None; buffer = []; continue
                
            match = re.match(r"^//\s*(\d+)\.", stripped)
            if match and current_type:
                if current_idx is not None and buffer:
                    query_str = " ".join(buffer).strip()
                    if query_str.endswith(','): query_str = query_str[:-1]
                    queries[current_type][current_idx] = query_str
                
                current_idx = int(match.group(1))
                buffer = []
                continue

            if current_type and current_idx and not stripped.startswith("//"):
                buffer.append(stripped)

        if current_type and current_idx and buffer:
            query_str = " ".join(buffer).strip()
            if query_str.endswith(','): query_str = query_str[:-1]
            queries[current_type][current_idx] = query_str

    return queries

QUERIES_CARREGADAS = carregar_queries(ARQUIVO_QUERIES)

def rodar_query_distribuida(tipo, index, container, uri, flags_extras=""):
    """
    Injeta a query diretamente no mongosh dentro do container via Docker Exec (STDIN).
    Isso garante que o script python rode de fora, mas a consulta execute nativamente na rede do cluster.
    """
    query_text = QUERIES_CARREGADAS[tipo].get(index)
    if not query_text:
        print(f"  [ERRO] Query {index} do tipo {tipo} não encontrada no parser!")
        return 0
    
    # Monta o comando de execução interativa (-i) do Docker
    cmd = f'docker exec -i {container} mongosh "{uri}" {flags_extras} --quiet'
    
    start = time.perf_counter()
    # Passa o texto da query via input (simulando digitação no terminal interno)
    subprocess.run(cmd, shell=True, input=query_text, text=True, capture_output=True)
    end = time.perf_counter()
    
    return end - start

def executar_benchmark():
    # URIs formatadas para a arquitetura de Replica Set no Docker
    URI_BASELINE = "mongodb://mongo_base_1:27017,mongo_base_2:27017,mongo_base_3:27017/StackOverflow?replicaSet=rs_baseline"
    URI_TLS = "mongodb://mongo_tls_1:27017,mongo_tls_2:27017,mongo_tls_3:27017/StackOverflow?replicaSet=rs_tls"
    FLAGS_TLS = "--tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames"

    with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Tipo', 'Query_Index', 'Cenario', 'P50', 'P95', 'P99', 'Vazao_ops_sec'])

        for tipo, qtd in MAPA_QUERIES.items():
            print(f"\n========================================")
            print(f"INICIANDO BATERIA: {tipo}")
            print(f"========================================")
            
            for i in range(1, qtd + 1):
                tempos_b, tempos_t = [], []
                print(f"  -> Rodando Query {i}/{qtd} (20 repetições)...")
                
                # 1. Warm-up (Garante cache do SO, cache do WiredTiger e estabelecimento da rota Docker)
                rodar_query_distribuida(tipo, i, "mongo_base_1", URI_BASELINE)
                rodar_query_distribuida(tipo, i, "mongo_tls_1", URI_TLS, FLAGS_TLS)

                # 2. Medições Oficiais
                for _ in range(REPETICOES):
                    # Executa no cluster Baseline
                    tempos_b.append(rodar_query_distribuida(tipo, i, "mongo_base_1", URI_BASELINE))
                    
                    # Executa no cluster TLS
                    tempos_t.append(rodar_query_distribuida(tipo, i, "mongo_tls_1", URI_TLS, FLAGS_TLS))
                
                # 3. Cálculo e Gravação no CSV
                if sum(tempos_b) > 0 and sum(tempos_t) > 0:
                    met_b = calcular_metricas(tempos_b)
                    met_t = calcular_metricas(tempos_t)
                    
                    writer.writerow([tipo, i, 'Baseline', met_b['p50'], met_b['p95'], met_b['p99'], met_b['vazao']])
                    writer.writerow([tipo, i, 'TLS', met_t['p50'], met_t['p95'], met_t['p99'], met_t['vazao']])
                    
                    print(f"     [OK] Baseline p50: {met_b['p50']:.4f}s | TLS p50: {met_t['p50']:.4f}s")
    
    print(f"\nBENCHMARK CONCLUÍDO COM RIGOR! Resultados salvos e prontos para tabulação em: {LOG_FILE}")

def calcular_metricas(tempos):
    tempos.sort()
    vazao = len(tempos) / sum(tempos) if sum(tempos) > 0 else 0
    return {
        "p50": round(statistics.median(tempos), 6),
        "p95": round(tempos[int(len(tempos) * 0.95)], 6),
        "p99": round(tempos[int(len(tempos) * 0.99)], 6),
        "vazao": round(vazao, 4)
    }

if __name__ == "__main__":
    executar_benchmark()
