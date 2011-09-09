from annoying.decorators import render_to

from ranking.models import Deputado


@render_to('ranking/index.html')
def index(request):
    ranking = sorted(Deputado.objects.all(), key=lambda d: d.porcentagem_de_presencas)
    return {'ranking': ranking}