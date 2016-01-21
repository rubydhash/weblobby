# -*- coding: utf-8 -*-

from django import shortcuts

from weblobby.views import base
from weblobby.models import Visitante
from weblobby.models import Registros
from weblobby.models import Log

class HomeView(base.WeblobbyBaseView):
    def get(self, request, *args, **kwargs):
        last_edited_users = Visitante.objects.all().order_by('-data_ultima_alteracao')[:10]
        last_registros = Registros.objects.all().order_by('-dataehora')[:10]

        if request.user.is_superuser:
            logs = Log.objects.all().order_by('-created')[:10]
        else:
            logs = Log.objects.filter(user=request.user).order_by('-created')[:10]

        return shortcuts.render(request, 'home.html', {'last_edited_users': last_edited_users,
                                                       'last_registros': last_registros,
                                                       'logs': logs})