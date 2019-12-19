"""
    url definitions for the descarregas app
"""
from django.conf.urls import url
from aula.apps.descarregues import views

urlpatterns = [
    url(r'^descarregaAlumnes/$', views.descarregaAlumnes,
        name="administracio__descarrega__alumnes" ),
]


