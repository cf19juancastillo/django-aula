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

