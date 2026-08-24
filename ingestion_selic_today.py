import requests
import json

dt_end = "31/01/2023"
dt_start ="01/01/2023"
codigo_serie = "1178"

# Na parte da url em baixo se usar 432 usa Selic Meta, se usar 1178 usa a Selic Efetiva (aparentemente usama a Efetiva)
url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={dt_start}&dataFinal={dt_end}"

resposta = requests.get(url, verify=False)
resposta_moggadora = json.dumps(resposta.json(), indent=4, ensure_ascii=False)

print(resposta_moggadora)