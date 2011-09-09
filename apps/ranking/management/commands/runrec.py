# -*- coding: utf-8 -*-


from django.core.management.base import BaseCommand

from apps.ranking.models import *
from apps.ranking.recommender import Recommender

class Command(BaseCommand):
    args = '<presenca>'
    help = 'Carrega dados'
    
    def handle(self, *args, **options):
        dep_list = Deputado.objects.all()
        item_list = Proposicao.objects.all()
        rec = Recommender()
        
        for i,dep in enumerate(dep_list):
            print "Processando %s... (%s/%s)" % (dep, i, len(dep_list))
            similar = rec.get_similar_users(dep, dep_list, item_list, limit=8)
            matches = [[int(s[0]*100), s[1]] for s in similar]
            dep.vota_com = matches
            dep.save()