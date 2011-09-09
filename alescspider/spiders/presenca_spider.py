# -*- coding: utf-8 -*-

import re

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from alescspider.items import PresencaItem

from helper_functions import get_first, clean_string


class PresencaSpider(CrawlSpider):
    name = "presenca"
    allowed_domains = ["www.alesc.sc.gov.br"]
    
    start_urls = ["http://www.alesc.sc.gov.br/portal/transparencia/presenca_plenaria.php?periodo=08-2011&Submit=Enviar",
        "http://www.alesc.sc.gov.br/portal/transparencia/presenca_plenaria.php?periodo=07-2011&Submit=Enviar",
        "http://www.alesc.sc.gov.br/portal/transparencia/presenca_plenaria.php?periodo=06-2011&Submit=Enviar",
        "http://www.alesc.sc.gov.br/portal/transparencia/presenca_plenaria.php?periodo=05-2011&Submit=Enviar",
        "http://www.alesc.sc.gov.br/portal/transparencia/presenca_plenaria.php?periodo=04-2011&Submit=Enviar"]
        
    rules = (
        Rule(SgmlLinkExtractor(allow=r'.*/transparencia/presenca_plenaria_detalhes.php\?id=[0-9]+'),
            'parse_presenca', follow=True,
        ),
    )
     
    def parse_presenca(self, response):
        hxs = HtmlXPathSelector(response) 
        
        item = PresencaItem()
        sessao_data = hxs.select('//div[@id="conteudo"]/h3/text()')[0].extract()
        
        # Extrai id externo da sessao
        m_id_externo = re.search("[0-9]+", response.url)
        
        # Extrai numero da sessao
        m_sessao = re.search("^[0-9]+", sessao_data)

        # Extrai data da sessao
        m_data = re.search("\d{1,2}\/\d{1,2}\/\d{4}$", sessao_data)
        
        item['id_externo'] = int(m_id_externo.group(0))

        item['sessao'] = int(m_sessao.group(0))

        item['data'] = m_data.group(0)   
        
        lista_presenca = []
        rows = hxs.select('//table[@class="pagamentos"]/tr')  
        for row in rows:
            
            nome = row.select('td/text()')[0].extract()
            presenca = row.select('td/text()')[1].extract().lstrip().rstrip()
            justificativa = ''
            
            if not presenca:
                presenca = row.select('td/a/text()')[0].extract()
                justificativa = get_first(row.select('td/div/text()').extract())
                #import pdb; pdb.set_trace()
            
            lista_presenca.append(
            {
                'presenca' : clean_string(presenca),
                'justificativa' : justificativa,
                'nome' : clean_string(nome),
            })
                

        item['lista_presenca'] = lista_presenca
        return item
        
        
        
        
        
        