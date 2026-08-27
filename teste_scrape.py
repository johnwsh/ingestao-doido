import time
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url_base = "https://sei.aneel.gov.br/sei/modulos/pesquisa/"

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

lista_processos = []
inicio = 0
linhas_por_pagina = 50

# Inicia o loop infinito da paginação
while True:
    print(f"Buscando processos a partir do índice {inicio}...")
    
    # Atualiza a URL com o valor de 'inicio' atual e seta isPaginacao=true
    url_pesquisa = f"md_pesq_controlador_ajax_externo.php?acao_ajax_externo=protocolo_pesquisar&id_orgao_acesso_externo=0&isPaginacao=true&inicio={inicio}&rowsSolr={linhas_por_pagina}"
    url_final = url_base + url_pesquisa
    
    result = requests.post(url_final, data=payload, headers=headers, impersonate="chrome120", verify=False)
    
    soup = BeautifulSoup(result.text, 'html.parser')
    
    celulas_processos = soup.find_all('td', class_='pesquisaTituloEsquerda')
    
    # Condição de parada: se não encontrou mais nenhuma célula, a paginação acabou
    if not celulas_processos:
        print("Fim da paginação. Nenhum processo a mais encontrado nesta página.")
        break

    # Extrai os dados da página atual
    for td in celulas_processos:
        nup = td.get('data-prot')
        
        link_tag = td.find('a') 
        href_relativo = link_tag.get('href') if link_tag else None
        url_completa = urljoin(url_base, href_relativo) if href_relativo else None
        
        descricao = td.text.strip().replace('\n', '').replace('\r', '')
        descricao = ' '.join(descricao.split()) 

        lista_processos.append({
            'nup': nup,
            'descricao': descricao,
            'url_acesso': url_completa
        })
    
    # Incrementa o índice para buscar a próxima página no próximo ciclo
    inicio += linhas_por_pagina
    
    # Pausa de 1 segundo para não sobrecarregar o servidor
    time.sleep(1)

# ==========================================
# Testando a visualização dos resultados finais
# ==========================================
print("\n" + "="*50)
print(f"EXTRAÇÃO CONCLUÍDA! Total de processos coletados: {len(lista_processos)}")
print("="*50 + "\n")

# Mostrando apenas os primeiros e os últimos para confirmar
if lista_processos:
    print("--- PRIMEIRO PROCESSO DA LISTA ---")
    print(f"NUP: {lista_processos[0]['nup']}")
    print(f"Assunto: {lista_processos[0]['descricao']}")
    print(f"URL: {lista_processos[0]['url_acesso']}\n")
    
    print("--- ÚLTIMO PROCESSO DA LISTA ---")
    print(f"NUP: {lista_processos[-1]['nup']}")
    print(f"Assunto: {lista_processos[-1]['descricao']}")
    print(f"URL: {lista_processos[-1]['url_acesso']}")