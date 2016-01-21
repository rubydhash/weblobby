from django.views import generic
from lib.djangoutils import customviews

from weblobby.forms.visitante import VisitanteFormSearch

class WeblobbyBaseView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        request.menu_form = VisitanteFormSearch()

        return super(WeblobbyBaseView, self).dispatch(request, *args, **kwargs)

class WeblobbyBaseRestrictedView(customviews.RestrictedView, WeblobbyBaseView):
    dummy = False