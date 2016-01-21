# -*- coding: utf-8 -*-

__author__ = 'jimmy'

from django import shortcuts
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.core import serializers

from weblobby import models
from weblobby.views.base import WeblobbyBaseView

class PanelView(WeblobbyBaseView):
    def get(self, request, *args, **kwargs):
        return shortcuts.render(request, 'panel.html')

    def post(self, request, *args, **kwargs):
        try:
            vis = request.session.pop('visitante_panel')
        except:
            return HttpResponseNotFound()

        if request.is_ajax():
            return HttpResponse(serializers.serialize('json', [vis, ]))
        else:
            return shortcuts.render(request, 'panel.html')

class PanelHideView(WeblobbyBaseView):
    def get(self, request, *args, **kwargs):
        request.session['visitante_panel'] = models.Visitante()

        if request.is_ajax():
            return HttpResponse()
        else:
            return shortcuts.render(request, 'home.html')
