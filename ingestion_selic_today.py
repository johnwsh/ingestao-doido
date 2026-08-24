import requests
import json

# Na parte da url em baixo se usar 432 usa Selic Meta, se usar 1178 usa a Selic Efetiva (aparentemente usama a Efetiva)
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados?formato=json&dataInicial=01/01/2023&dataFinal=31/01/2023"

resposta = requests.get(url, verify=False)
resposta_moggadora = json.dumps(resposta.json(), indent=4, ensure_ascii=False)

print(resposta_moggadora)