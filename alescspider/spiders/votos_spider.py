# -*- coding: utf-8 -*-
import re
from itertools import islice

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from alescspider.items import ProposicaoItem

from helper_functions import find_start_urls, clean_string


class VotosSpider(CrawlSpider):
    
    name = "votos"
    allowed_domains = ["www.alesc.sc.gov.br"]
    start_urls = find_start_urls()
    
    rules = (
        Rule(SgmlLinkExtractor(allow=r'.*/transparencia/planilha_votacao_detalhe.php\?cod=[0-9]+&ciod=[0-9]+'),
            'parse_proposicao', follow=True,
        ),
    )
    
     
    def parse_proposicao(self, response):
        hxs = HtmlXPathSelector(response)
        item = ProposicaoItem()
        
        item['url'] = response.url
        
        m_codigo_sessao = re.search("cod=[0-9]+", response.url)
        item['sessao'] = m_codigo_sessao.group(0).split('=')[1]
        
        item['codigo'] = hxs.select('//div[@id="conteudo"]/h3/text()')[0].extract().split()[1]
        #m_codigo = re.search("[A-Z]+\/\d+.\d\/\d{4}", proposicao_data)
        #item['codigo'] = m_codigo.group(0)
        
        item['descricao'] = hxs.select('//div[@id="conteudo"]/p/text()')[0].extract()
        
        lista_votos = []
        rows = hxs.select('//table[@class="pagamentos"]/tr')
        for row in islice(rows,1,None):
            partido, nome, voto = row.select('td/text()').extract()
            lista_votos.append(
            {
                'partido' : clean_string(partido),
                'nome' : clean_string(nome),
                'voto' : clean_string(voto),
            }) 
            
        item['lista_votos'] = lista_votos
        
        url = hxs.select('//div[@id="conteudo"]/p[2]/a/@href')[0].extract()
        request = Request(url, callback = self.parse_prop, dont_filter=True)
        request.meta['item'] = item
        if url.startswith('http://'):
            yield request
        else:
            yield item
            
        
    def parse_prop(self, response):
        item = response.request.meta['item']
        hxs = HtmlXPathSelector(response)
        item['data'] = hxs.select("//td[@class='eM' and contains(.,'Ordem do Dia')]/parent::tr/td/li").re('\d{2}\/\d{2}\/\d{4}')[-1]
        
        yield item
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
