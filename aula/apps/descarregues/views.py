"""
    views for the descarregues option

    XXX TODO: right now it displays the same contents as aula/apps/extEsfera/views.py
"""
import csv
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from aula.utils.decorators import group_required
from aula.apps.descarregues.forms import descarregaAlumnesForm


@login_required
@group_required(['direcció','administradors'])
def descarregaAlumnes(request):
    """ Allows downloading the students in a csv file """

    #(user, l4) = tools.getImpersonateUser(request)
    #professor = User2Professor( user )

    #from aula.apps.extEsfera.sincronitzaEsfera import sincronitza

    #if request.method == 'POST':

    #    form = sincronitzaEsferaForm(request.POST, request.FILES)

    #    if form.is_valid():
    #        f=request.FILES['fitxerEsfera']
    #        resultat=sincronitza(f, user)

    #        return render(
    #                request,
    #                'resultat.html',
    #                {'head': 'Resultat importació Esfer@' ,
    #                 'msgs': resultat },
    #                )

    #else:
    #    form = sincronitzaEsferaForm()

    #return render(
    #                request,
    #                'sincronitzaEsfera.html',
    #                {'form': form },
    #            )



    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnes.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    form = descarregaAlumnesForm()
    
    return render(
                request,
                'form.html', 
                {'form': form }
                )
    #resultat = { 'errors': [], 'warnings': [], 'infos': [ 'Descarrega finalitzada' ] }
    #return render(
    #        request,
    #        'resultat.html',
    #        {'head': 'Resultat importació Esfer@' ,
    #         'msgs': resultat },
    #        )

