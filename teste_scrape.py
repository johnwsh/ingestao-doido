import time
from datetime import datetime
from curl_cffi import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def listar_processos(data_inicio: str, data_fim: str) -> list:
    """
    Busca os processos no SEI da ANEEL em um intervalo de datas.
    
    :param data_inicio: Data de início no formato 'DD/MM/YYYY'
    :param data_fim: Data de fim no formato 'DD/MM/YYYY'
    :return: Lista de dicionários contendo os dados dos processos
    """
    
    data_inicio_iso = datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d")
    data_fim_iso = datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d")
    
    # Monta a query do Solr (partialfields) dinamicamente usando f-string
    partialfields = f'sta_prot:P AND (dta_ger:[{data_inicio_iso}T00:00:00Z TO {data_fim_iso}T00:00:00Z] OR dta_inc:[{data_inicio_iso}T00:00:00Z TO {data_fim_iso}T00:00:00Z])'

    url_base = "https://sei.aneel.gov.br/sei/modulos/pesquisa/"
    
    payload = {
        'txtDataInicio': data_inicio, 
        'txtDataFim': data_fim,
        'chkSinProcessos': 'S',
        'partialfields': partialfields,
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

    while True:
        print(f"Buscando processos ({data_inicio} a {data_fim}) a partir do índice {inicio}...")
        
        url_pesquisa = f"md_pesq_controlador_ajax_externo.php?acao_ajax_externo=protocolo_pesquisar&id_orgao_acesso_externo=0&isPaginacao=true&inicio={inicio}&rowsSolr={linhas_por_pagina}"
        url_final = url_base + url_pesquisa
        
        result = requests.post(url_final, data=payload, headers=headers, impersonate="chrome120", verify=False)
        
        soup = BeautifulSoup(result.text, 'xml')
        
        celulas_processos = soup.find_all('td', class_='pesquisaTituloEsquerda')
        
        if not celulas_processos:
            print("Fim da paginação. Nenhum processo a mais encontrado nesta página.")
            break

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
        
        inicio += linhas_por_pagina
        time.sleep(1)

    return lista_processos

if __name__ == "__main__":
    
    # Chama a função passando as datas
    processos_hoje = listar_processos("04/08/2026", "04/08/2026")
    
    print("\n" + "="*50)
    print(f"EXTRAÇÃO CONCLUÍDA! Total de processos coletados: {len(processos_hoje)}")
    print("="*50 + "\n")
    
    # Imprime os 3 primeiros como teste
    for p in processos_hoje[:3]:
        print(f"NUP: {p['nup']}")
        print(f"URL: {p['url_acesso']}")
        print(f"Assunto: {p['descricao']}")
        print("-" * 50)