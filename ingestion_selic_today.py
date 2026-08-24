import requests
import json

url = "https://www3.bcb.gov.br/novoselic/rest/taxaSelicApurada/pub/search"

# Como essa API tem paginação, colocamos um pageSize alto para trazer o ano todo de uma vez
parametros = {
    "page": 1,
    "pageSize": 500 
}

payload = {
    "dataInicial": "01/01/2023",
    "dataFinal": "31/12/2023"
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

resposta = requests.post(url, params=parametros, json=payload, headers=headers, verify=False)
resposta_moggadora = json.dumps(resposta.json(), indent=4, ensure_ascii=False)

print(resposta_moggadora)