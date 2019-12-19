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


