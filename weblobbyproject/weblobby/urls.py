# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from weblobby.views import visitante
from weblobby.views import home
from weblobby.views import blank
from weblobby.views import panel

urlpatterns = patterns(
    '',
    # Index
    url(r'^$', home.HomeView.as_view(), name='index'),
    url(r'^insert/$', visitante.VisitanteInsertView.as_view(), name='visitante_insert'),
    url(r'^profile/(?P<pk>\d+)/$', visitante.VisitanteProfileView.as_view(), name='visitante_profile'),
    url(r'^profile_reg/(?P<pk>\d+)/$', visitante.VisitanteProfileRegView.as_view(), name='visitante_profile_reg'),
    url(r'^profile/panel/(?P<pk>\d+)/$', visitante.VisitantePanelProfileView.as_view(), name='visitante_panel_profile'),
    url(r'^edit/(?P<pk>\d+)/$', visitante.VisitanteEditView.as_view(), name='visitante_edit'),
    url(r'^delete/(?P<pk>\d+)/$', visitante.VisitanteDeleteView.as_view(), name='visitante_delete'),
    url(r'^blank/?$', blank.BlankView.as_view(), name='blank'),
    url(r'^panel/?$', panel.PanelView.as_view(), name='panel'),
    url(r'^panel/hide/?$', panel.PanelHideView.as_view(), name='panel_hide'),
)
