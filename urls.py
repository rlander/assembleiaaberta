from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", view='ranking.views.index', name='ranking_index'),
    url(r'^sobre/$', direct_to_template, {"template": "sobre.html"}, name="sobre"),
    url(r"^r/", include('ranking.urls')),
    url(r"^admin/", include(admin.site.urls)),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
