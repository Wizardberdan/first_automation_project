# Sistema de Extração de Dados de Vendas

Este projeto é um sistema automatizado para extração de dados de vendas de um banco de dados SQL Server, com posterior geração de arquivo CSV e envio via SFTP.

## 📋 Funcionalidades

- **Extração de Dados**: Conecta-se ao SQL Server e executa consulta para obter dados de vendas do dia anterior
- **Processamento**: Formata os dados conforme especificações necessárias
- **Geração de Arquivo**: Cria arquivo CSV com nomenclatura baseada na data
- **Envio Automatizado**: Envia o arquivo via SFTP para servidor remoto

## 🚀 Tecnologias Utilizadas

- **Python 3.9**: Linguagem principal
- **Pandas**: Manipulação e análise de dados
- **SQLAlchemy**: ORM para conexão com banco de dados
- **PyODBC**: Driver para conexão com SQL Server
- **Paramiko**: Cliente SSH/SFTP para transferência de arquivos
- **Docker**: Containerização da aplicação

## 📦 Estrutura do Projeto

```
sistema-vendas/
├── Dockerfile              # Configuração do container Docker
├── docker-compose.yml      # Configuração Docker Compose
├── toFornecedor.py         # Script principal Python
├── requirements.txt        # Dependências Python
├── run_vendas.bat         # Script de execução para Windows
├── install_task.bat       # Script para criar tarefa agendada
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Docker instalado
- Acesso a um servidor SQL Server
- Acesso a um servidor SFTP

### Configuração com Docker

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd sistema-vendas
   ```

2. **Construa e execute com Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Configure as variáveis de ambiente:**
   
   Crie um arquivo `.env` ou configure as variáveis diretamente:
   ```bash
   # Configurações do Banco de Dados
   DB_SERVER=seu_servidor_sql
   DB_DATABASE=sua_base_dados
   DB_USERNAME=seu_usuario
   DB_PASSWORD=sua_senha
   
   # Configurações SFTP
   SFTP_HOSTNAME=seu_servidor_sftp
   SFTP_PORT=22
   SFTP_USERNAME=usuario_sftp
   SFTP_PASSWORD=senha_sftp
   SFTP_REMOTE_DIR=/caminho/remoto/
   ```

4. **Execute manualmente (teste):**
   ```bash
   docker-compose exec sistema-vendas python toFornecedor.py
   ```

### Configuração de Execução Automatizada (Windows)

Para executar automaticamente todos os dias:

1. **Configure a tarefa agendada:**
   ```batch
   # Execute como Administrador
   install_task.bat
   ```

2. **O script criará:**
   - Tarefa diária no Agendador de Tarefas do Windows
   - Execução automática às 08:00
   - Logs detalhados em `logs/vendas_YYYY-MM-DD.log`

3. **Executar manualmente:**
   ```batch
   run_vendas.bat
   ```

### Instalação Local

1. **Clone o repositório e instale as dependências:**
   ```bash
   git clone <url-do-repositorio>
   cd sistema-vendas
   pip install -r requirements.txt
   ```

2. **Configure as variáveis de ambiente no seu sistema**

3. **Execute o script:**
   ```bash
   python toFornecedor.py
   ```

## 📊 Formato dos Dados

### Vendas
- **SKU**: Código do produto
- **MODELO FORNECEDOR**: Descrição do produto
- **COR FORNECEDOR**: Código da cor
- **COR**: Descrição da cor
- **TAMANHO**: Tamanho do produto
- **DATA VENDA**: Data no formato YYYYMMDD
- **CNPJ FILIAL**: CNPJ da filial (sem formatação)
- **QUANTIDADE VENDIDA**: Quantidade vendida
- **VALOR VENDA**: Valor unitário da venda

## 📝 Arquivo Gerado

O arquivo é nomeado com a seguinte convenção:
- `VENDAS_DDMMYYYY.csv`

Onde DDMMYYYY representa a data de ontem da execução.

## 🔒 Segurança

### Recomendações para Produção

1. **Não hardcode credenciais**: Use sempre variáveis de ambiente
2. **Docker Secrets**: Para ambientes Docker Swarm, considere usar Docker Secrets
3. **Criptografia**: Use conexões SSL/TLS para banco de dados e SFTP
4. **Usuário não-root**: O container executa com usuário não-privilegiado
5. **Validação de dados**: Implemente validações adicionais conforme necessário

## 📋 Logs e Monitoramento

### Sistema de Logs
- **Logs automáticos**: Cada execução gera logs detalhados
- **Localização**: `logs/vendas_YYYY-MM-DD.log`
- **Conteúdo dos logs**:
  - Timestamps de início e fim
  - Status do container Docker
  - Sucessos e falhas na execução
  - Detalhes de erros quando ocorrem
  - Logs do próprio script Python

### Estrutura dos Logs
```
==========================================
[DD/MM/YYYY HH:MM:SS] Iniciando execução do sistema de vendas
==========================================
[DD/MM/YYYY HH:MM:SS] Executando script de extração de vendas...
[timestamp] - INFO - Iniciando execução do script toFornecedor.py
[timestamp] - INFO - DataFrame Vendas criado com sucesso!
[timestamp] - INFO - Conexão SFTP estabelecida com sucesso.
[timestamp] - INFO - Arquivo CSV criado e enviado para '/VENDAS_DDMMYYYY.csv' com sucesso.
[timestamp] - INFO - Processo concluído com sucesso.
[DD/MM/YYYY HH:MM:SS] Execução concluída com SUCESSO
==========================================
```

### Monitoramento
- Logs diários separados por data
- Códigos de erro para troubleshooting
- Verificação automática do status do container

## 🔧 Manutenção e Troubleshooting

### Comandos Úteis

```batch
# Verificar status do container
docker ps --filter "name=sistema-vendas"

# Ver logs do container
docker logs sistema-vendas

# Executar manualmente para teste
run_vendas.bat

# Verificar tarefa agendada
schtasks /query /tn "Sistema-Vendas-Diario"

# Executar tarefa agendada imediatamente
schtasks /run /tn "Sistema-Vendas-Diario"
```

### Problemas Comuns

1. **Container não está rodando**:
   ```batch
   docker-compose up -d
   ```

2. **Erro de conexão com banco**:
   - Verificar variáveis de ambiente no `.env`
   - Testar conectividade de rede

3. **Erro de SFTP**:
   - Verificar credenciais SFTP
   - Testar conexão manual

4. **Logs não são gerados**:
   - Verificar permissões da pasta `logs`
   - Executar como administrador

## 📞 Suporte

Para dúvidas ou suporte, entre em contato através de:
- Email: alberdan.gbmenezes@gmail.com

## 🔄 Versionamento

- **v1.0**: Versão inicial com funcionalidades básicas de extração e envio
