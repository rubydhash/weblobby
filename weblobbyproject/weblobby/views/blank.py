# -*- coding: utf-8 -*-

from django import shortcuts
from django.core import urlresolvers
from django.views import generic

from weblobby import models

class BlankView(generic.View):
    template_name = 'blank.html'

    def get(self, request, *args, **kwargs):
        return shortcuts.render(request, self.template_name)