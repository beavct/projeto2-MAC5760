import pandas as pd
import mysql.connector
import psycopg2
import os

# Configurações 
DB_TYPE = 'postgres' # 'mysql' ou 'postgres'
DB_CONFIG = {"host": "localhost", "database": "StackOverflow", "user": "postgres", "password": "123"}
TABELAS = ["Posts", "Users", "Badges", "Comments", "Votes", "PostLinks", "PostTypes"]

def exportar_amostra():
    # Cria diretório para os CSVs
    if not os.path.exists("db_data"):
        os.makedirs("db_data")

    for tabela in TABELAS:
        print(f"Exportando 500000 linhas de: {tabela}...")
        
        # Conectar no banco
        if DB_TYPE == 'postgres':
            conn = psycopg2.connect(**DB_CONFIG)
            query = f'SELECT * FROM "{tabela}" LIMIT 500000'
        else:
            conn = mysql.connector.connect(**DB_CONFIG)
            query = f'SELECT * FROM {tabela} LIMIT 500000'
            
        # Extrair dados para Pandas DataFrame
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Salvar CSV individual (para conferência)
        df.to_csv(f"amostra_csv/{tabela}.csv", index=False)
    
    print("Exportação concluída! Os arquivos estão na pasta 'amostra_csv'.")

if __name__ == "__main__":
    exportar_amostra()