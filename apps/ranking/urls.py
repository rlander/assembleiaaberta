from django.conf.urls.defaults import *

from ranking.models import Deputado

info_dict = {
    'queryset': Deputado.objects.all(),
}


urlpatterns = patterns('',
    #url(r"^$", view='ranking.views.index', name='ranking_index'),
    #url(r'^(?P<slug>[-\w]+)/$', view='django.views.generic.list_detail.object_detail', dict(slug_field='slug')),
    url(r'^(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', dict(info_dict), 'ranking_deputado_detail'),
)
