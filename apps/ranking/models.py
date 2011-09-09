# -*- coding: utf-8 -*-
from datetime import date
from django.db import models
from autoslug import AutoSlugField
from serializeddatafield import SerializedDataField


class VotoManager(models.Manager):
    
    def get_for_user_in_bulk(self, user):
        votos_dict = {}
        votos = list(self.filter(deputado__pk=user.id, voto_int__isnull=False))
        votos_dict = dict([(voto.proposicao, voto) for voto in votos])
        return votos_dict
        

class Deputado(models.Model):
    
    nome = models.CharField(blank=True, max_length=80)
    slug = AutoSlugField(populate_from='nome', unique=True)
    data_nascimento = models.DateField(blank=True, null=True)
    municipio_nascimento = models.CharField(blank=True, max_length=150)
    nacionalidade = models.CharField(blank=True, max_length=150)
    instrucao = models.CharField(blank=True, max_length=80)
    ocupacao = models.CharField(blank=True, max_length=80)
    votos_ultima_eleicao = models.CharField(blank=True, max_length=80)
    foto = models.ImageField(blank=True, upload_to="uploads/MODELNAME/%Y/%m/%d")
    vota_com = SerializedDataField(null=True, blank=True)
    
    
    @property
    def total_de_presencas(self):
        return Presenca.objects.filter(deputado=self, presenca="Presente").count()
    
    # Total de sessoes realizadas durante o seu mandato     
    @property
    def total_de_sessoes(self):
        return Presenca.objects.filter(deputado=self).count()
    
    @property    
    def porcentagem_de_presencas(self):
        return int((self.total_de_presencas * 100 ) / self.total_de_sessoes)
    
    @property
    def idade(self):
        dias_no_ano = 365.25
        return int((date.today() - self.data_nascimento).days/dias_no_ano)
    
    class Meta:
        pass

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self):
        raise NotImplementedError        
        
class Sessao(models.Model):
    
    numero = models.CharField(blank=True, max_length=80)
    data = models.DateField(blank=True, null=True)
    id_externo = models.IntegerField(blank=True, null=True)
    
    class Meta:
        ordering = ['-data']

    def __unicode__(self):
        return "Sessao numero %s" % self.numero

    def get_absolute_url(self):
        raise NotImplementedError

        
class Presenca(models.Model):
    
    sessao = models.ForeignKey(Sessao, blank=True, null=True)
    deputado = models.ForeignKey(Deputado, blank=True, null=True)
    presenca = models.CharField(blank=True, max_length=80)
    justificativa = models.CharField(blank=True, max_length=200)
    
    class Meta:
        ordering = ['-sessao']

    def __unicode__(self):
        return "Sessao numero %s - Dep. %s" % (self.sessao.numero, self.deputado.nome)

    def get_absolute_url(self):
        raise NotImplementedError

class Proposicao(models.Model):
    """
    
    """
    
    codigo = models.CharField(blank=True, max_length=80)
    sessao = models.ForeignKey(Sessao, blank=True, null=True)
    url = models.URLField(blank=True)
    descricao = models.TextField(blank=True)
    
    class Meta:
        pass

    def __unicode__(self):
        return self.codigo

    def get_absolute_url(self):
        raise NotImplementedError

class Voto(models.Model):
    """
    
    """
    
    proposicao = models.ForeignKey(Proposicao, blank=True, null=True)
    deputado = models.ForeignKey(Deputado, blank=True, null=True)
    voto = models.CharField(blank=True, max_length=80)
    voto_int = models.SmallIntegerField(blank=True, null=True)
    
    objects = VotoManager()
    
    class Meta:
        pass

    def __unicode__(self):
        return "Dep. %s: %s" % (self.deputado.nome, self.voto)

    def get_absolute_url(self):
        raise NotImplementedError
        
    def save(self, *args, **kwargs):
        if not self.id:
            if self.voto == u'Sim':
                self.voto_int = 1
            elif self.voto == u'Não':
                self.voto_int = -1
        super(Voto, self).save()



