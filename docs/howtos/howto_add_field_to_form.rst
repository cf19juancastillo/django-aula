#####################################
How To: afegir un camp a un formulari
#####################################

Aquesta guia es va definir pel següent commit

::

    commit 4cf2ab2ca2b6cfdbfbb561962d7273a4e6c179e9
    Author: moiatjda <moises.gomez@iesjoandaustria.org>
    Date:   Thu Dec 19 12:12:42 2019 +0100

        finished the guide to add a new functionality to djau

És possible que en futures versions de djau, aquests continguts quedin
obsolets.

Descàrrega d'alumnes per grup
=============================

A continuació descric les passes a seguir per introduir la nova
funcionalitat de descarregar la llista d'alumnes de djau. En aquesta nova
versió, els alumnes poden ser filtrats pel seu grup.

La implementació consisteix en: afegir una opció al menú ``Admin``
anomenada ``Descarrega``, i dins d'aquesta, l'opció ``Alumnes``.

La idea és que ``Admin > Descarrega`` vagi incorporant diferents opcions
de descàrrega. De moment la d'alumnes.

Aquesta opció no requereix crear cap nou model de dades. Només li cal fer
servir el model ``Alumne`` que es troba definit a
``aula.apps.alumnes.models``.

Les passes necessaries per introduir aquesta funcionalitat són:

* crear la nova app

* registrar la nova app

* afegir la nova opció al menú

* afegir la nova opció a les urls


Crear la nova app
=================

La nostra nova app es guardarà en la carpeta ``aula/apps/descarregues``
(que haurem de crear)

A dins, hi afegirem els següents fitxers:

* views.py

  És el codi que donarà resposta a les peticions sobre la nova app de
  descàrregues

* forms.py

  És el codi que descriurà els formularis que hi haurà a la nova app

* urls.py

  Inclourà les definicions de les urls que corresponen a descàrregues.

* utils.py

  Inclourà el codi que se n'encarregarà de composar els fitxers a
  descarregar.


views.py
========

Aquest fitxer oferirà una funció per gestionar les peticions de descàrrega
dels alumnes

::

    """
        views for the descarregues option
    """

    from django.contrib.auth.decorators import login_required
    from django.shortcuts import render
    from django.http import HttpResponseRedirect

    from aula.utils.decorators import group_required
    from .forms import descarregaAlumnesForm
    from .utils import compose_alumnes_csv_response

    @login_required
    @group_required(['direcció'])
    def descarregaAlumnes(request):
        """ Download the students in a csv file """
        if request.method == 'POST':
            form = descarregaAlumnesForm(request.POST)
            if form.is_valid():
                selected_grups = form.cleaned_data.get('grups')
                return compose_alumnes_csv_response(
                    filtres={ 'grups': selected_grups})
        else:
            form = descarregaAlumnesForm()

            return render(request,
                      'form.html',
                      {'form': form, 'head': 'Descarrega'}
                      )

Fixa't que la nova opció requereix loging i que qui fa la petició sigui
del grup ``direcció``.

Fixa't també com seleccionem quins grups s'acceptaran. El formulari
contindrà un camp anomenat 'grups' i ``form.cleaned_data.get('grups')``
ens oferirà una llista amb la descripció dels grups seleccionats.


forms.py
--------

Aquest fitxer defineix un formulari amb un camp de sel·lecció múltiple.

::

    """
        Forms for the descarrega app
    """
    from django import forms
    from .utils import composa_opcions_grups

    class descarregaAlumnesForm(forms.Form):
        grups = forms.CharField(label="Quins grups?",
                               widget=forms.SelectMultiple(
                                   choices=composa_opcions_grups()
                                   ))


urls.py
-------

En aquest cas, només ens cal afegir la url per l'opció nova:

::

    """
        url definitions for the descarregas app
    """
    from django.conf.urls import url
    from .views import descarregaAlumnes

    urlpatterns = [
        url(r'^descarregaAlumnes/$', descarregaAlumnes,
            name="administracio__descarrega__alumnes" ),
    ]

utils.py
--------

Inclou dos mètodes:

* ``compose_alumnes_csv_response()``

  Aquest mètode retorna un ``HttpResponse`` amb els valors dels alumnes
  trobats, en format csv.

  Admet el paràmetre ``filtres`` que, de ser indicat, s'espera que sigui
  un diccionari amb clau el camp del filtre (de moment només accepta
  "grups") i com a valor, els valors acceptats pel filtre.

  De moment, només retorna alguns dels camps disponibles dels alumnes.

* ``composa_opcions_grups()``

  Retorna la llista de grups disponibles de manera que pugui ser
  utilitzada per un ``form.SelectMultiple``, és a dir, una llista de
  tuples amb els valors i text a mostrar de cada opció.

  Inclou l'opció *TOTS* per permetre seleccionar tots.

::

    """
        This module contains utility methods to construct the information
        to be downloaded by the descarregues app
    """

    import csv

    from django.http import HttpResponse

    from aula.apps.alumnes.models import Alumne, Grup

    _OPCIO_TOTS = '-- TOTS --'

    def compose_alumnes_csv_response(filtres=None):
        """ composes the alumnes data in a csv format and returns it as a http response
            It accepts filtres as a dict with keys:
                'grups': list of groups names
        """
        def filtra_alumnes(filtres):
            """ retorna els alumnes que respecten els filtres indicats """
            alumnes = Alumne.objects.all()

            if not filtres:
                return alumnes

            if 'grups' in filtres:
                if _OPCIO_TOTS not in filtres['grups']:
                    alumnes = [a 
                               for a in alumnes 
                               if a.grup.descripcio_grup in filtres['grups'] ]
            return alumnes

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="alumnes.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nom', 'Cognoms', 'Grup', 'Data de naixement'])

        alumnes = filtra_alumnes(filtres)
        for alumne in alumnes:
            row = [alumne.nom, alumne.cognoms, alumne.grup, alumne.data_neixement]
            writer.writerow(row)

        return response

    def  composa_opcions_grups():
        """ returns a list with the groups as a tuple (display name, group) """
        opcio_tots = [ (_OPCIO_TOTS, _OPCIO_TOTS) ]
        return opcio_tots + [(g.descripcio_grup, g.descripcio_grup)
                             for g in Grup.objects.all()]

Registrar la nova app
=====================

Per registrar la nova app que crearem, anirem a ``aula/settings_dir/common.py``, hi
localitzarem la llista ``INSTALLED_APPS_AULA``, i hi afegirem l'entrada:

::

    'aula.apps.descarregues',

D'aquesta manera, Django sabrà que ha de fer cas a la nostra nova app.


Afegir la nova app al menú
==========================

Afegirem la nova opció a ``Admin > Descarrega > Alumnes``

Per fer-ho, accedirem a ``aula/utils/menu.py``, localitzarem la tupla
``arbre1`` i, dins la secció ``administració``, després de
``Sincronitza``, hi afegim la nostra entrada:

::

    (
       "Descarrega",                                # subitem_id
       "administracio__descarrega__blanc",          # subitem_url
       di,                                          # subitem_condicio (permissos)
       None,                                        # alerta
       (                                            # subitems
           (
               "Alumnes",                           # subsubitem_id
               "administracio__descarrega__alumnes",# subsubitem_url
               di,                                  # subsubitem_condicio
               None                                 # alerta
           ),
       ),
    )



Afegir la nova app a les urls
=============================

La incorporació de la nova url, tal i com està definit djau, requereix
modificar els següents fitxers:

* ``aula/urls.py``

  A la llista ``urlpatterns`` hi afegirem l'entrada:

  ::

        url(r'^descarregues/', include('aula.apps.descarregues.urls')),

* ``aula/utils/urls.py``

  A la llista ``urlpatterns`` hi afegirem l'entrada:

::

    url(r'^opcionsDescarrega/$', blanc,
        name ="administracio__descarrega__blanc" )    ,

