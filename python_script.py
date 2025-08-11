# Imports necessários
import pandas as pd
from sqlalchemy import create_engine
import urllib
from datetime import datetime, timedelta
import paramiko
import os
import logging
import io
import re

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Iniciando execução do script toFornecedor.py")

# Obter a data de ontem
data_ontem = datetime.now() - timedelta(days=1)
data_formatada = data_ontem.strftime("%d%m%Y")

# Configurações de conexão com banco de dados
server = os.getenv("DB_SERVER")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
driver = "{ODBC Driver 17 for SQL Server}"

# String de conexão para SQLAlchemy
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
params = urllib.parse.quote_plus(conn_str)
engine_str = f'mssql+pyodbc:///?odbc_connect={params}'

# Criando engine do SQLAlchemy
engine = create_engine(engine_str)

# Consulta SQL simplificada para dados de vendas
query_vendas = """
-- Consulta fictícia simplificada para dados de vendas do dia anterior
SELECT 
    p.id AS SKU,
    p.nome AS 'MODELO FORNECEDOR',
    p.cor_id AS 'COR FORNECEDOR',
    c.nome AS COR,
    p.tamanho AS TAMANHO,
    FORMAT(CAST(GETDATE()-1 AS DATE), 'yyyyMMdd') AS 'DATA VENDA',
    f.cnpj AS 'CNPJ FILIAL',
    v.quantidade AS 'QUANTIDADE VENDIDA',
    v.preco_unitario AS 'VALOR VENDA'
FROM (
    -- Dados fictícios de vendas
    SELECT 301 as produto_id, 25 as quantidade, 89.90 as preco_unitario, 1 as filial_id
    UNION ALL
    SELECT 302, 12, 129.50, 2
    UNION ALL
    SELECT 303, 8, 45.99, 1
    UNION ALL
    SELECT 304, 15, 75.00, 2
    UNION ALL
    SELECT 305, 3, 199.99, 1
) v
CROSS JOIN (
    -- Dados fictícios de produtos
    SELECT 301 as id, 'Camiseta Básica' as nome, 60 as cor_id, 'M' as tamanho
    UNION ALL
    SELECT 302, 'Calça Jeans', 65, 'G'
    UNION ALL
    SELECT 303, 'Tênis Esportivo', 70, 'P'
    UNION ALL
    SELECT 304, 'Jaqueta Casual', 75, 'M'
    UNION ALL
    SELECT 305, 'Vestido Social', 80, 'G'
) p ON p.id = v.produto_id
CROSS JOIN (
    -- Dados fictícios de cores
    SELECT 60 as id, 'Rosa' as nome
    UNION ALL
    SELECT 65, 'Roxo'
    UNION ALL
    SELECT 70, 'Laranja'
    UNION ALL
    SELECT 75, 'Azul Marinho'
    UNION ALL
    SELECT 80, 'Verde Escuro'
) c ON c.id = p.cor_id
CROSS JOIN (
    -- Dados fictícios de filiais
    SELECT 1 as id, '12345678000199' as cnpj
    UNION ALL
    SELECT 2, '98765432000188'
) f ON f.id = v.filial_id
"""

# Executando a consulta e criando o DataFrame
df_vendas = pd.read_sql(query_vendas, engine)
print("DataFrame Vendas criado com sucesso!")

# Função para formatação do DataFrame de vendas
def format_vendas(df):
    """
    Formata o DataFrame de vendas conforme especificações.
    
    Args:
        df: DataFrame de vendas
    
    Returns:
        DataFrame formatado
    """
    # Converter colunas específicas para inteiros
    integer_columns = ['SKU', 'COR FORNECEDOR', 'QUANTIDADE VENDIDA']
    for col in integer_columns:
        df[col] = df[col].fillna(0).astype(int)
    
    # Remover caracteres especiais do CNPJ
    df['CNPJ FILIAL'] = df['CNPJ FILIAL'].astype(str).apply(lambda x: re.sub(r'[./-]', '', x))
    
    return df

# Aplicar formatação ao DataFrame
df_vendas = format_vendas(df_vendas)

def create_and_upload_csv(sftp, df, remote_path):
    """
    Cria um arquivo CSV diretamente na memória a partir de um DataFrame e envia para o caminho remoto via SFTP.
    
    Args:
        sftp: Objeto SFTP client
        df: DataFrame do pandas
        remote_path: Caminho completo no servidor remoto
    
    Returns:
        bool: True se o envio foi bem-sucedido, False caso contrário
    """
    try:
        # Cria um buffer em memória para o CSV
        csv_buffer = io.StringIO()
        
        # Salva o DataFrame como CSV no buffer
        df.to_csv(csv_buffer, index=False, sep=';', encoding='utf-8')
        
        # Converte para bytes para envio
        csv_bytes = io.BytesIO(csv_buffer.getvalue().encode('utf-8'))
        
        # Envia o arquivo diretamente para o servidor remoto
        sftp.putfo(csv_bytes, remote_path)
        logging.info(f"Arquivo CSV criado e enviado para '{remote_path}' com sucesso.")
        return True
    except Exception as e:
        logging.error(f"Erro ao criar e enviar o arquivo CSV para '{remote_path}': {e}")
        return False

def main():
    """
    Função principal que executa o processo de extração e envio de dados.
    """
    # Configurações do SFTP
    sftp_hostname = os.getenv("SFTP_HOSTNAME")
    sftp_port = int(os.getenv("SFTP_PORT", 22))
    sftp_username = os.getenv("SFTP_USERNAME")
    sftp_password = os.getenv("SFTP_PASSWORD")
    remote_directory = os.getenv("SFTP_REMOTE_DIR", "/")

    # Estabelecendo conexão SFTP
    try:
        transport = paramiko.Transport((sftp_hostname, sftp_port))
        transport.connect(username=sftp_username, password=sftp_password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        logging.info("Conexão SFTP estabelecida com sucesso.")
        print("Conexão SFTP estabelecida com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao conectar ao servidor SFTP: {e}")
        print(f"Erro ao conectar ao servidor SFTP: {e}")
        return

    try:
        # Criando e enviando o arquivo CSV de vendas
        if create_and_upload_csv(sftp, df_vendas, f"{remote_directory}VENDAS_{data_formatada}.csv"):
            print(f"VENDAS_{data_formatada}.csv enviado com sucesso!")
            logging.info("Processo concluído com sucesso.")
        else:
            logging.error("Falha no envio do arquivo de vendas.")
        
    except Exception as e:
        logging.error(f"Erro durante o processo principal: {e}")
    finally:
        # Fecha a conexão SFTP
        sftp.close()
        transport.close()
        logging.info("Conexão SFTP encerrada.")

if __name__ == "__main__":
    main()

# Fechando a conexão com o banco
engine.dispose()
