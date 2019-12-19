"""
    url definitions for the descarregas app
"""
from django.conf.urls import url
from .views import descarregaAlumnes

urlpatterns = [
    url(r'^descarregaAlumnes/$', descarregaAlumnes,
        name="administracio__descarrega__alumnes" ),
]


