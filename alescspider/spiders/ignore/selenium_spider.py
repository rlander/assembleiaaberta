# -*- coding: utf-8 -*-

# Esta spider requer o driver para python do selenium instalado.
# Também é necessário o Selenium Server (http://seleniumhq.org/download/)
# Para rodá-la, basta executar o Selenium Server (java -jar selenium-server-standalone-2.5.0.jar) e preencher os dados 
# na inicialização do driver (ex.: selenium("localhost", 444, "*chrome", "http:wwww.domain.com")).
#
# Isso tudo é necessário porque o Scrapy não é capaz de fazer o parsing de páginas que fazem uso extenso de javascript.
#


import time
import urllib
import simplejson as json

from bs4 import BeautifulSoup

from scrapy.spider import BaseSpider

from alescspider.items import DeputadoUrlItem

from selenium import selenium

class SeleniumSpider(BaseSpider):
	name = "selenium"
	allowed_domains = ["noticias.uol.com.br"]
	
	start_urls = []

	
	def __init__(self):
		BaseSpider.__init__(self)
		SeleniumSpider.start_urls = self.generate_urls(self.load_names('lista_inicial_nomes.json'))
		self.verificationErrors = []
		self.selenium = selenium("10.0.2.2", 4444, "*chrome", "http://www.google.com")
		self.selenium.start()
		
		
	def __del__(self):
		self.selenium.stop()
		print self.verificationErrors
		BaseSpider.__del__(self)
		
	
	def load_names(self, file):
	    nomes = json.load(open(file))
	    return nomes
	    
	
	def generate_urls(self, nomes):
	    urls = []
	    for nome in nomes:
	        urlized = self.latin_one_urlize(nome)
	        url = "http://noticias.uol.com.br/politica/politicos-brasil/resultado.jhtm?p=" + urlized + "&ano-eleicao=2010&dados-cargo-disputado-id=07&dados-uf-eleicao=SC&sort=dados-cargo-disputado-id#resultado"
	        urls.append(url)
	    return urls

	    
	def latin_one_urlize(self, string):
	    return urllib.quote_plus(string.lower().encode('iso-8859-1')).replace('+', '+AND+')
	    

	def parse(self, response):
		item = DeputadoUrlItem()		
		sel = self.selenium
		sel.open(response.url)
		
		#Wait for javscript to load in Selenium
		time.sleep(5)
		
		html = sel.get_html_source()
		soup = BeautifulSoup(html)
		item['nome'] = soup.find("ul", {"class" : "resultadoCorpo"}).li.dl.dd.text
		item['url'] = soup.find("ul", {"class" : "resultadoCorpo"}).li.h3.a['href']
		
		yield item
		
		

        