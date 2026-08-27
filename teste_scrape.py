from curl_cffi import requests

url_base = "https://sei.aneel.gov.br/sei/modulos/pesquisa/"
url_pesquisa = "md_pesq_controlador_ajax_externo.php?acao_ajax_externo=protocolo_pesquisar&id_orgao_acesso_externo=0&isPaginacao=false&inicio=0&rowsSolr=50"
url_final = url_base + url_pesquisa

payload = {
    'txtDataInicio': '03/08/2026', 
    'txtDataFim': '03/08/2026',
    'chkSinProcessos' : 'S',
    'partialfields' : 'sta_prot:P AND (dta_ger:[2026-08-03T00:00:00Z TO 2026-08-03T00:00:00Z] OR dta_inc:[2026-08-03T00:00:00Z TO 2026-08-03T00:00:00Z])',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://sei.aneel.gov.br',
    'Referer': 'https://sei.aneel.gov.br/sei/modulos/pesquisa/md_pesq_processo_pesquisar.php?acao_externa=protocolo_pesquisar&acao_origem_externa=protocolo_pesquisar&id_orgao_acesso_externo=0',
    'X-Requested-With': 'XMLHttpRequest'
}

result = requests.post(url_final, data=payload, headers=headers, impersonate="chrome120", verify=False)

#print(f"Status Code: {result.status_code}")
#print(result.text)

url_pesquisa = "md_pesq_documento_consulta_externa.php?yPDszXhdoNcWQHJaQlHJmJIqCNXRK_Sh2SMdn1U-tzMNfy7c8sRAVeWnpgI0O65tpoltpZDjHc52aYMTLVDoKULwEhlBtoDylkHIeCqgQ1QD0oAam8wIejLZHT4uYHBT"
url_final = url_base + url_pesquisa

result = requests.get(url_final, headers=headers, impersonate="chrome120", verify=False)

print(f"Status Code: {result.status_code}")
if result.status_code == 200:
    
    if b"%PDF" in result.content[:10]:
        
        with open("documento_aneel.pdf", "wb") as arquivo_pdf:
            arquivo_pdf.write(result.content)
            
        print("PDF salvo com sucesso!")
        
    else:
        print("O download funcionou, mas o arquivo não parece ser um PDF. Pode ser uma página de erro.")
        print(result.text[:200])
else:
    print(f"Falha ao baixar o documento. Status Code: {result.status_code}")
