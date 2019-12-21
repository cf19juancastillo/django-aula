############################################
How To: afegir una nova funcionalitat a djau
############################################


Aquesta guia es va definir pel següent commit

::

    commit 060fa4f371b89ce616f50af1c3770a73781ccd02
    Author: moiatjda <moises.gomez@iesjoandaustria.org>
    Date:   Tue Dec 17 17:29:03 2019 +0100

        added some documentation and cleaned up some extra whitespaces. While there're no tests for these files, I shouln't have broken anything

És possible que en futures versions de djau, aquests continguts quedin
obsolets.

Descàrrega d'alumnes
====================

A continuació descric les passes a seguir per introduir la nova
funcionalitat de descarregar la llista d'alumnes de djau.

La funcionalitat consisteix en: afegir una opció al menú ``Admin``
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
                return compose_alumnes_csv_response()
        else:
            form = descarregaAlumnesForm()

        return render(request,
                      'form.html',
                      {'form': form, 'head': 'Descarrega'}
                      )

Fixa't que la nova opció requereix loging i que qui fa la petició sigui
del grup ``direcció``.

forms.py
--------

Aquest fitxer, de moment, només defineix un simple formulari sense cap
opció, a banda del butó per enviar.

En un futur, podria contenir més opcions, com ara filtres (quins alumnes,
quins camps…)

::

    """
        Forms for the descarrega app
    """
    from django import forms

    class descarregaAlumnesForm(forms.Form):
        pass

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

Inclou un únic mètode que composa un HttpResponse amb el contingut
requerit en format csv.

Donat que no hem establert filtres, el mètode agafa tots els alumnes i, de
moment, quatre dels camps disponibles.

::

    """
        This module contains utility methods to construct the information
        to be downloaded by the descarregues app
    """

    import csv

    from django.http import HttpResponse

    from aula.apps.alumnes.models import Alumne

    def compose_alumnes_csv_response():
        """ composes the alumnes data in a csv format and returns it as a http response """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="alumnes.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nom', 'Cognoms', 'Grup', 'Data de naixement'])

        alumnes = Alumne.objects.all()
        for alumne in alumnes:
            row = [alumne.nom, alumne.cognoms, alumne.grup, alumne.data_neixement]
            writer.writerow(row)

        return response


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

