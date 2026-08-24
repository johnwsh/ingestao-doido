import base64
import json
import requests

# 1. Configurando os parâmetros
parametros = {
    "language": "pt-br",
    "id": "SLP",
    "pageNumber": 1,
    "pageSize": 20,
    "date": "2026-08-21" 
}

# 2. Codificando para Base64
json_string = json.dumps(parametros)
payload_b64 = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

# 3. Montando a URL
url = f"https://sistemaswebb3-derivativos.b3.com.br/referenceRatesProxy/Search/GetList/{payload_b64}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 4. Consumindo a API
response = requests.get(url, headers=headers, verify="certificado.pem")

if response.status_code == 200:
    # Transforma a resposta em um dicionário Python
    dados_dict = response.json()
    
    # Faz o "Pretty Print" 
    # json.dumps() converte o dict de volta para string, e o indent=4 cria a identação visual
    pretty_json = json.dumps(dados_dict, indent=4, ensure_ascii=False)
    
    print(pretty_json)
else:
    print(f"Erro na requisição: {response.status_code}")