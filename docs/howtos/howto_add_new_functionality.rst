##################################
Adding a new functionality in djau
##################################


This guide was defined for the following commit:

::

    commit 060fa4f371b89ce616f50af1c3770a73781ccd02
    Author: moiatjda <moises.gomez@iesjoandaustria.org>
    Date:   Tue Dec 17 17:29:03 2019 +0100

        added some documentation and cleaned up some extra whitespaces. While there're no tests for these files, I shouln't have broken anything

Adding an option to download all the students
=============================================

Since this option uses existing models (Alumne) it won't create a new
model.

It requires adding a new option in the menu. 




Adding the option in the menu
=============================

I've decided to place this option at Admin -> descarregues -> alumnes

File: aula/utils/menu

Function ``calcula_menu()``

Tuple: ``arbre1``

Section: ``administració``

After subitem ``Sincronitza`` added the definition of the new option:

::

                       # MGG: new option
                       (
                           "Descarrega",
                           "administracio__descarrega__blanc",
                           di,
                           None,
                           (
                               (
                                   "Alumnes",
                                   "administracio__descarrega__alumnes",
                                   di,
                                   None
                               ),
                           ),
                       ),

Adding the descarregas app
==========================

file: aula/settings_dir/common.py

Add the following entry in the list ``INSTALLED_APPS_AULA``:

::

    'aula.apps.descarregues',


File: aula/urls.py

Add the following entry in the list ``urlpatterns``:

::

    url(r'^descarregues/', include('aula.apps.descarregues.urls')),


File ``aula/utils/urls.py``

Add the following entry in the list ``urlpatterns``:

::

    url(r'^opcionsDescarrega/$', blanc,
        name ="administracio__descarrega__blanc" )    ,

Add url
=======


Create folder ``aula/app/descarregues``

Now, create file ``aula/apps/descarregues/urls.py`` to translate urls <->
menu names

::

    from django.conf.urls import url
    from aula.apps.descarregues import views

    urlpatterns = [
        url(r'^descarregaAlumnes/$', views.descarregaAlumnes,
            name="administracio__descarrega__descarrega_alumnes" ),
    ]

Adding the view
===============

Now it is time for the view

Create the file ``aula/apps/descarregues/views.py`` and include in:

::

    XXX here you are
    You've left the views containing the same code in another view and
    as a result, the app complains with a 

django.urls.exceptions.NoReverseMatch: Reverse for 'administracio__descarrega__alumnes' not found. 'administracio__descarrega__alumnes' is not a valid view function or pattern name.

