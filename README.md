# MAC0426/MAC5760 - Projeto 2

Repositório de código do Projeto 2 da disciplina MAC0426/MAC5760 — Overhead de operações criptográficas em bancos de dados distribuídos (Artigo).

À medida que sistemas distribuídos passam a armazenar volumes crescentes de dados sensíveis, técnicas criptográficas tornam-se indispensáveis para garantir confidencialidade e integridade. No entanto, essas técnicas introduzem custos de desempenho que se tornam ainda mais relevantes em ambientes distribuídos, nos quais a comunicação entre nós já representa um gargalo natural. Nosso projeto tem como objetivo investigar o impacto de operações criptográficas sobre o desempenho de bancos de dados distribuídos, combinando uma revisão da literatura existente com experimentos práticos. Pretendemos configurar um banco de dados distribuído e medir métricas como latência e vazão sob diferentes cenários, com e sem criptografia em repouso e em trânsito, a fim de quantificar o overhead introduzido e discutir os trade-offs entre segurança e desempenho.


> **Grupo:**
> - Beatriz Viana Costa, 13673214
> - Lys Katherine Park Kang, 17040581
> - Raphaella Brandão Jacques, 17040730
> - Stephanie Maria Braga, 18009336

---

## Sumário

1. [Pré-requisitos](#1-pré-requisitos)
2. [Como executar os experimentos](#2-como-executar-os-experimentos)
3. [Estrutura do repositório](#3-estrutura-do-repositório)

---

<a name="1-pré-requisitos"></a>
## 1. Pré-requisitos

Para instanciar o ambiente e executar a bateria de testes automatizados, certifique-se de possuir as seguintes ferramentas instaladas no sistema hospedeiro (Host/WSL):

* **Docker** (v20.10+ ou superior)
* **Docker Compose** (v2.0+ ou superior)
* **Python 3.8+** com os seguintes pacotes instalados:

```bash
pip install pandas matplotlib seaborn numpy
```


<a name="2-como-executar-os-experimentos"></a>
## 2. Como executar os experimentos  

O procedimento experimental foi blindado para isolar o custo criptográfico dentro de uma rede virtual em contêineres, eliminando ruídos de DNS do sistema operacional e mitigando gargalos de I/O em disco por meio de indexação estrutural. Siga os passos na ordem estrita abaixo:

Passo 1: Inicializar os Clusters Distribuídos
Levante os dois cenários isolados de Replica Set (Baseline e TLS) em segundo plano:

```bash
docker compose up -d
```

Verifique se os 6 contêineres (mongo_base_1 a 3 e mongo_tls_1 a 3) estão operando em perfeita conciliação.

Passo 2: Configuração dos Clusters e Criação dos Índices B-Tree
Acesse o nó primário de cada cluster para inicializar os conjuntos de réplicas e aplicar a estratégia exaustiva de indexação nas coleções do banco StackOverflow.

Para o cluster Baseline:

```bash
docker exec -it mongo_base_1 mongosh --eval "rs.initiate({_id:'rs_baseline',members:[{_id:0,host:'mongo_base_1:27017'},{_id:1,host:'mongo_base_2:27017'},{_id:2,host:'mongo_base_3:27017'}]})"
```

Para o cluster TLS:

```bash
docker exec -it mongo_tls_1 mongosh --tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames --eval "rs.initiate({_id:'rs_tls',members:[{_id:0,host:'mongo_tls_1:27017'},{_id:1,host:'mongo_tls_2:27017'},{_id:2,host:'mongo_tls_3:27017'}]})"
```

Em seguida, execute o script de criação de índices no banco para erradicar Collection Scans:

```bash
docker exec -i mongo_base_1 mongosh "mongodb://mongo_base_1:27017/StackOverflow?replicaSet=rs_baseline" < criar_indices.js

docker exec -i mongo_tls_1 mongosh "mongodb://mongo_tls_1:27017/StackOverflow?replicaSet=rs_tls" --tls --tlsAllowInvalidCertificates --tlsAllowInvalidHostnames < criar_indices.js
```

Passo 3: Executar a Automação do Benchmark
Rode o script coordenador em Python. Ele injetará o fluxo heterogêneo de 30 consultas do arquivo queries.js diretamente na entrada padrão (STDIN) do motor interno dos contêineres, realizando 1 rodada de warm-up e 20 repetições oficiais cronometradas por consulta:

```bash
python3 automation.py
```

Os resultados agregados (Latência p50, percentis de cauda p95/p99 e Throughput) serão compilados de forma higienizada no arquivo resultados.csv.