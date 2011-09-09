# -*- coding: utf-8 -*-
import simplejson as json

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from alescspider.items import DeputadoItem

from alescspider.spiders.helper_functions import clean_string


class DeputadoSpider(BaseSpider):
    name = "deputado"
    allowed_domains = ["noticias.uol.com.br"]
        
    start_urls = []
    
    def __init__(self):
        BaseSpider.__init__(self)
        DeputadoSpider.start_urls = self.get_start_urls()
    
    def get_start_urls(self):
        start_urls = json.load(open('lista_deputados_links.json'))
        return [i['url'] for i in start_urls]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        item = DeputadoItem()
        item['image_urls'] = hxs.select('//img[@class="foto"]/@src').extract()
        
        lista_dados_pessoais = hxs.select('//dl[@id="listaDadosPessoais"]/dt')
        dados_pessoais = {}
        for i, d in enumerate(lista_dados_pessoais):
            dados_pessoais[d.select('text()')[0].extract()] = clean_string(lista_dados_pessoais.select('//dl[@id="listaDadosPessoais"]/dd/text()')[i].extract())
        item['dados_pessoais'] = dados_pessoais
        
        lista_dados_eleitorais = hxs.select('//dl[@id="listaDadosEleitorais"]/dt')
        dados_eleitorais = {}
        for i, d in enumerate(lista_dados_eleitorais):
            dados_eleitorais[d.select('text()')[0].extract()] = clean_string(lista_dados_eleitorais.select('//dl[@id="listaDadosEleitorais"]/dd/text()')[i].extract())
        item['dados_eleitorais'] = dados_eleitorais
        
        votos = hxs.select('//td[@class="quantidadeVotos"]/text()')[0].extract()
        item['votos'] = clean_string(votos)
        
    
        return item
        