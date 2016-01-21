# -*- coding: utf-8 -*-

from django import shortcuts
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from django import http

from weblobby import models
from weblobby.models import Log
from weblobby.forms.registros import RegistrosAddForm
from weblobby.forms.visitante import VisitanteAddAndEditForm
from weblobby.views.base import WeblobbyBaseView, WeblobbyBaseRestrictedView

class VisitanteProfileView(WeblobbyBaseView):
    model = models.Visitante
    template_name = 'profile.html'
    aba_registros = False

    def __get_registros(self, visitante_id):
        return models.Registros.objects.filter(visitante=visitante_id).order_by('-dataehora')

    def get(self, request, *args, **kwargs):
        visitante = shortcuts.get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        registros = self.__get_registros(visitante.id)
        form = RegistrosAddForm()

        return shortcuts.render(request, self.template_name, {'object': visitante,
                                                              'registros_form': form,
                                                              'aba_registros': self.aba_registros,
                                                              'registros': registros})

    def post(self, request, *args, **kwargs):
        visitante = shortcuts.get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        registros = self.__get_registros(visitante.id)
        form = RegistrosAddForm(request.POST)
        form.usuario = request.user
        form.visitante = visitante

        if form.is_valid():
            form.save()
            return shortcuts.redirect(urlresolvers.reverse('weblobby:visitante_profile_reg', args=(visitante.id,)))

        return shortcuts.render(request, self.template_name, {'object': visitante,
                                                              'registros_form': form,
                                                              'aba_registros': True,
                                                              'registros': registros})

# Abre o perfil na aba de registros
class VisitanteProfileRegView(VisitanteProfileView):
    aba_registros = True

class VisitantePanelProfileView(WeblobbyBaseView):
    model = models.Visitante
    template_name = 'panel.html'

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            visitante = shortcuts.get_object_or_404(self.model, pk=self.kwargs.get('pk'))
            if visitante.wifi:
                request.session['visitante_panel'] = visitante
            return http.HttpResponse()
        return http.HttpResponseNotFound()


class VisitanteInsertView(WeblobbyBaseRestrictedView):
    model = models.Visitante
    template_name = 'insert.html'
    perm_name = 'add'
    
    def get(self, request, *args, **kwargs):
        # Zera o painel, es esta cadastrando um usuario novo nao tem que mostrar nada
        # Para zerar tem que mandar um usuario vazio
        request.session['visitante_panel'] = models.Visitante()

        form = VisitanteAddAndEditForm()
        return shortcuts.render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VisitanteAddAndEditForm(request.POST)

        if form.is_valid():
            vis = form.save()

            Log(user=request.user, msg=_(u"Visitante '%s' cadastrado" % vis)).save()

            if vis.wifi:
                request.session['visitante_panel'] = vis

            return shortcuts.redirect(urlresolvers.reverse('weblobby:visitante_profile_reg', args=(vis.id,)))

        return shortcuts.render(request, self.template_name, {'form': form})

class VisitanteEditView(WeblobbyBaseRestrictedView):
    model = models.Visitante
    template_name = 'edit.html'
    perm_name = 'change'

    def __get_form(self, visitante, include_initial=False, post=None, form_errors=None):
        if include_initial:
            init = {'cpf': visitante.cpf_display()}
        else:
            init = {}
        if post is not None:
            new_post = post.copy()
            new_post.appendlist('senha', visitante.senha)
            new_post.appendlist('expiracao_acesso_wifi', visitante.expiracao_acesso_wifi)
            form = VisitanteAddAndEditForm(new_post, instance=visitante, initial=init)
        else:
            form = VisitanteAddAndEditForm(instance=visitante, initial=init)
        if form_errors is not None:
            form._errors = form_errors._errors
        return form

    def get(self, request, *args, **kwargs):
        visitante = shortcuts.get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        form = self.__get_form(visitante, True)
        return shortcuts.render(request, self.template_name, {'form': form, 'object': visitante})

    def post(self, request, *args, **kwargs):
        visitante = shortcuts.get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        form = self.__get_form(visitante, False, request.POST)

        if form.is_valid():
            form.save()

            Log(user=request.user, msg=_(u"Visitante '%s' editado" % visitante)).save()

            return shortcuts.redirect(urlresolvers.reverse('weblobby:visitante_profile_reg', args=(visitante.id,)))

        new_form = self.__get_form(visitante, True, request.POST, form)
        return shortcuts.render(request, self.template_name, {'form': new_form, 'object': visitante})

class VisitanteDeleteView(WeblobbyBaseRestrictedView):
    perm_name = 'delete'
    model = models.Visitante

    def get(self, request, *args, **kwargs):
        visitante = shortcuts.get_object_or_404(self.model, pk=self.kwargs.get('pk'))

        Log(user=request.user, msg=_(u"Visitante '%s' deletado" % visitante)).save()

        visitante.delete()

        return shortcuts.redirect(urlresolvers.reverse('weblobby:index'))