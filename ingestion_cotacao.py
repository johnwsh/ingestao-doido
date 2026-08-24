import requests
import json

dt_start = "'08-01-2026'"
dt_end = "'08-10-2026'"


# URL direto com as datas
url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial={dt_start},dataFinalCotacao={dt_end})?$format=json"

# Faz a requisição e pega o JSON como dicionário
resposta = requests.get(url, verify=False)
dados = resposta.json()

# Transforma de volta em string, mas agora com indentação (bonito)
resultado_bonito = json.dumps(dados, indent=4, ensure_ascii=False)

# Imprime o resultado formatado na tela
print(resultado_bonito)