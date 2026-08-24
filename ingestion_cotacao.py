import requests
import json

# URL direto com as datas
url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='08-01-2026',dataFinalCotacao='08-10-2026')?$format=json"

# Faz a requisição e pega o JSON como dicionário
resposta = requests.get(url, verify=False)
dados = resposta.json()

# Transforma de volta em string, mas agora com indentação (bonito)
resultado_bonito = json.dumps(dados, indent=4, ensure_ascii=False)

# Imprime o resultado formatado na tela
print(resultado_bonito)