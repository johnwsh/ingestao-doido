# Ingestão de Dados Financeiros e Web Scraping ANEEL

Este repositório contém scripts em Python dedicados à coleta e ingestão de dados publicos, relacionados ao setor elétrico, como cotação do dólar, taxas Selic e processos administrativos da ANEEL.

---

## Estrutura do Projeto

*   **`ingestion_cotacao.py`**: Consome a API oficial do Banco Central do Brasil (BCB) para buscar a cotação do dólar (PTAX compra/venda) em um período específico.
*   **`ingestion_selic_today.py`**: Acessa os endpoints do Banco Central para obter o histórico das taxas Selic apuradas e divulgadas.
*   **`ingestion_selic_predict.py`**: Realiza buscas na API de taxas de referência da B3 (como projeções da Selic / SLP) codificando parâmetros de busca em Base64.
*   **`teste_scrape.py`**: Script de web scraping que consulta processos no SEI da ANEEL em determinado intervalo de datas, coleta metadados detalhados de cada processo e realiza o download de seus documentos associados.
*   **`requirements.txt`**: Declaração das dependências necessárias para a execução dos scripts.

---

## Pré-requisitos e Instalação

### 1. Criar e ativar o ambiente virtual (opcional, mas recomendado)
No diretório raiz do projeto, execute no terminal:
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
# No Windows (CMD):
.venv\Scripts\activate.bat
# No Linux/macOS:
source .venv/bin/activate
```

### 2. Instalar as dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

As principais bibliotecas utilizadas são:
*   `requests`: Para chamadas HTTP convencionais nas APIs do BCB.
*   `curl_cffi`: Utilizada no scraper da ANEEL para simular a assinatura TLS de navegadores reais (impersonate Chrome 120), evitando bloqueios de segurança do SEI.
*   `bs4` (BeautifulSoup): Para parsear e extrair dados das páginas HTML/XML do SEI.
*   `lxml`: Parser XML/HTML de alto desempenho utilizado pelo BeautifulSoup.

---

## Como Executar cada Script

### 1. Cotação do Dólar (PTAX)
O script `ingestion_cotacao.py` busca as cotações oficiais do dólar de um intervalo definido.
```bash
python ingestion_cotacao.py
```

### 2. Taxa Selic Diária
O script `ingestion_selic_today.py` traz o histórico diário da Selic dentro de um intervalo de datas.
```bash
python ingestion_selic_today.py
```

### 3. Projeção da Selic (B3 Derivativos)
O script `ingestion_selic_predict.py` consulta taxas de referência da B3 baseadas em projeções de derivativos.
```bash
python ingestion_selic_predict.py
```

### 4. Web Scraping SEI ANEEL
O script `teste_scrape.py` pesquisa processos públicos abertos ou alterados em datas específicas, salvando suas informações estruturadas em diretórios locais.
```bash
python teste_scrape.py
```

---

## 📦 Estrutura de Saída do Web Scraping (ANEEL)

Ao executar o scraper, os processos são catalogados em uma pasta raiz chamada `processos_aneel/`. Dentro dela, cada processo ganha uma pasta própria nomeada pelo seu NUP (Número Único de Protocolo) com caracteres especiais substituídos por underscores.

Exemplo de estrutura gerada:
```text
processos_aneel/
└── 48500_025115_2026-40/
    ├── metadados.json
    ├── 1234567.html
    └── 1234568.pdf
```

*   **`metadados.json`**: Contém informações detalhadas estruturadas extraídas da página de consulta do processo no formato:
    ```json
    {
        "processo": {
            "Número": "48500.025115/2026-40",
            "Interessados": "Empresa X | Órgão Y",
            "Assunto": "Pedido de Outorga...",
            "Data de Autuação": "27/08/2026"
        },
        "documentos": [
            {
                "id_documento": "1234567",
                "tipo": "Despacho",
                "data": "27/08/2026",
                "data_inclusao": "27/08/2026 10:00",
                "unidade_sigla": "SCG"
            }
        ],
        "historico": [
            {
                "data_hora": "27/08/2026 09:00",
                "unidade": "Protocolo",
                "descricao": "Processo autuado..."
            }
        ]
    }
    ```
*   **Arquivos baixados**: Documentos do processo são salvos em seus formatos nativos (como `.pdf`, `.html`, `.xlsx` etc.) usando o ID do documento como nome do arquivo.

