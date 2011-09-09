# -*- coding: utf-8 -*-
from django.contrib import admin
from ranking.models import Deputado, Sessao, Presenca, Proposicao, Voto
    
class PresencaInline(admin.TabularInline):
    model = Presenca
    extra = 0

class PresencaAdmin(admin.ModelAdmin):
    pass

class SessaoAdmin(admin.ModelAdmin):
    inlines = [PresencaInline,]
    list_display = ('numero', 'id_externo', 'data')

class VotoInline(admin.TabularInline):
    model = Voto
    extra = 0

class VotoAdmin(admin.ModelAdmin):
    pass
    
class DeputadoAdmin(admin.ModelAdmin):
    inlines = [VotoInline,]
    readonly_fields = ['vota_com',]
    list_display = ('nome', 'data_nascimento', 'votos_ultima_eleicao')

class ProposicaoAdmin(admin.ModelAdmin):
    inlines = [VotoInline,]
    
admin.site.register(Deputado, DeputadoAdmin)
admin.site.register(Sessao, SessaoAdmin)
admin.site.register(Presenca, PresencaAdmin)
admin.site.register(Proposicao, ProposicaoAdmin)
admin.site.register(Voto, VotoAdmin)