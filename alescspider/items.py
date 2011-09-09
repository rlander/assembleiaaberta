# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AlescItem(Item):
    pass

class PresencaItem(Item):
    sessao = Field()
    data = Field()
    lista_presenca = Field()
    id_externo = Field()

class ProposicaoItem(Item):
    sessao = Field()
    codigo = Field()
    lista_votos = Field()
    url = Field()
    descricao = Field()
    data = Field()

class DeputadoItem(Item):
    image_urls = Field()
    images = Field()
    dados_pessoais = Field()
    dados_eleitorais = Field()
    votos = Field()

class DeputadoUrlItem(Item):
    nome = Field()
    url = Field()

    
    
