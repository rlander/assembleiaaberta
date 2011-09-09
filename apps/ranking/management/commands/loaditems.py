# -*- coding: utf-8 -*-

from datetime import datetime
import simplejson as json

from django.core.management.base import BaseCommand

from apps.ranking.models import *

from fuzzywuzzy import process

class Command(BaseCommand):
    args = '<presenca>'
    help = 'Carrega dados'
    
    def handle(self, *args, **options):
        for arg in args:
            if arg == 'presenca':
                self.load_presenca()
            elif arg == 'proposicao':
                self.load_proposicao()
            elif arg == 'deputado':
                self.load_deputado()
            elif arg == 'all':
                self.load_presenca()
                self.load_proposicao()
                self.load_deputado()
    
    def load_presenca(self):
        json_data = open("items_presenca.json").read()
        items = json.loads(json_data)
        print "Carregando dados de presencas em plenario..."
        for item in items:
            s, created_s = Sessao.objects.get_or_create(numero=item['sessao'], id_externo=item['id_externo'], data=datetime.strptime(item['data'], '%d/%m/%Y'))
            if created_s:
                for presenca in item['lista_presenca']:
                    deputado, create_d = Deputado.objects.get_or_create(nome=presenca['nome'])
                    p = Presenca(sessao=s, deputado=deputado, justificativa=presenca['justificativa'], presenca=presenca['presenca'])
                    p.save()
                    
    def load_proposicao(self):
        json_data = open("items_votos.json").read()
        items = json.loads(json_data)
        print "Carregando dados de votos e proposicoes em plenario..."
        for item in items:
            sessao, created_sessao = Sessao.objects.get_or_create(id_externo=item['sessao'])
            p, created_p = Proposicao.objects.get_or_create(codigo=item['codigo'])
            if created_p:
                p.sessao = sessao
                p.url = item['url']
                p.descricao = item['descricao']
                if created_sessao:
                    sessao.data = datetime.strptime(item['data'], '%d/%m/%Y')
                    sessao.save()
                p.save()
                for voto in item['lista_votos']:
                    deputado = Deputado.objects.get(nome=voto['nome'])
                    v = Voto(proposicao=p, deputado=deputado, voto=voto['voto'])
                    v.save()

    def load_deputado(self):
        json_data = open('items_deputado.json').read()
        items = json.loads(json_data)
        print "Carregando perfis dos deputados..."
        deputados = Deputado.objects.values_list('nome', flat=True)
        for item in items:
            dados_pessoais = item['dados_pessoais']
            match = process.extractOne(dados_pessoais['Nome completo:'], deputados)
            d = Deputado.objects.get(nome=match[0])
            print dados_pessoais['Nome completo:'].encode('utf-8'), match
            d.data_nascimento = datetime.strptime(dados_pessoais['Data de nascimento:'], '%d/%m/%Y')
            d.municipio_nascimento = dados_pessoais[u'Município de nascimento:']
            d.nacionalidade = dados_pessoais['Nacionalidade:']
            d.instrucao = dados_pessoais[u'Grau de Instrução:']
            d.ocupacao = dados_pessoais[u'Ocupação principal declarada:']
            d.votos_ultima_eleicao = item['votos']
            d.foto = item['image_urls'][0]
            d.save()
            
            
            
            
            