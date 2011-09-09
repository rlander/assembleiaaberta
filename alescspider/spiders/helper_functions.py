# -*- coding: utf-8 -*-

import twill

def clean_string(string):
    return ' '.join(string.split())
    
def get_first(iterable, default=''):
    if iterable:
        for item in iterable:
            return item
    return default

def find_start_urls():
    """ Os dados sobre votações na assembleia só podem ser acessados depois do preenchimento de um formulario.
        Esta função itera sobre todas as opções possíveis do formulario (datas e sessões) para montar uma lista com 
        todas as urls disponiveis com dados de votações.
        
        Retorna uma lista de urls.
    """
   
    dates = []
    start_urls = []
    
    # Primeiramente itera sobre todas as datas disponiveis ate então
    b = twill.commands.get_browser()
    b.go("http://www.alesc.sc.gov.br/portal/transparencia/planilha_votacao.php")
    forms = b.get_all_forms()
    for p in forms[0].possible_items('periodo'):
        dates.append(p)

    # Primeiro elemento é espaço em branco
    del dates[0]
    
    # Formulário é reenviado com cada data disponível para encontrar as sessões.
    for date in dates:
        url = "http://www.alesc.sc.gov.br/portal/transparencia/planilha_votacao.php?periodo=%s" % date
        b.go(url)
        forms = b.get_all_forms()
        for p in forms[0].possible_items('ordemdia'):
            start_url = "http://www.alesc.sc.gov.br/portal//transparencia/planilha_votacao.php?periodo=%s&ordemdia=%s&Submit=Enviar" % (date, p)
            start_urls.append(start_url)
    
    return  start_urls

