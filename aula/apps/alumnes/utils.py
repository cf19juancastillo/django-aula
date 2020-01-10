"""
    This module defines utilities for reporting
"""

from django.db.models import Q

from aula.utils import tools
from aula.utils.tools import unicode
from aula.apps.tutoria.models import TutorIndividualitzat
from aula.apps.usuaris.models import Professor
from aula.utils import tools

from .models import Alumne

def duplicats_rpt():
    """ composes a report with duplicated alumnes """

    report = []

    taula = tools.classebuida()

    taula.tabTitle = 'Duplicacions detectades'

    taula.titol = tools.classebuida()
    taula.titol.contingut = u'Duplicacions detectades '

    taula.capceleres = []

    capcelera = tools.classebuida()
    capcelera.amplade = 30
    capcelera.contingut = u'Grup duplicat'
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 70
    capcelera.contingut = u'Opcions'
    taula.capceleres.append( capcelera )

    taula.fileres = []

    for a in Alumne.objects.filter(data_baixa__isnull = True):

        q_mateix_cognom = Q(cognoms=a.cognoms)
        q_mateix_nom = Q(nom=a.nom,)
        q_mateix_neixement = Q(
                        data_neixement = a.data_neixement
                            )
        q_mateixa_altres = Q(
                        adreca = a.adreca,
                        telefons = a.telefons,
                        localitat = a.localitat,
                        centre_de_procedencia = a.centre_de_procedencia,
                        adreca__gte= u""
                            )

        condicio1 = q_mateix_nom & q_mateix_cognom & q_mateix_neixement
        condicio2 = q_mateix_nom & q_mateix_cognom & q_mateixa_altres
        condicio3 = q_mateix_nom & q_mateixa_altres & q_mateix_neixement


        alumne_grup = Alumne.objects.filter(condicio1 | condicio2 | condicio3)

        if alumne_grup.count() > 1:
            filera = []

            #-grup--------------------------------------------
            camp = tools.classebuida()
            camp.multipleContingut =  [ (u'{0} {1}'.format(ag, ag.grup.nom_grup ), None )  for ag in alumne_grup ]
            filera.append(camp)

            #-opcions--------------------------------------------
            camp = tools.classebuida()
            camp.esMenu = True
            primer_alumne = a
            camp.multipleContingut =  [ (u'Fusionar', u'/alumnes/fusiona/{0}'.format( primer_alumne.pk )) , ]
            filera.append(camp)

            taula.fileres.append( filera )

    report.append(taula)

    return report


def reportLlistaTutorsIndividualitzats(  ):

    tutors_ids = TutorIndividualitzat.objects.all().values_list( 'pk' )

    report = []

    #--sense alumnes.................
    taula = tools.classebuida()
    taula.capceleres = []

    capcelera = tools.classebuida()
    capcelera.amplade = 30
    capcelera.contingut = u'{0}'.format('Professor')
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 50
    capcelera.contingut = u'{0}'.format('Alumnes amb tutoria individualitzada')
    taula.capceleres.append( capcelera )

    capcelera = tools.classebuida()
    capcelera.amplade = 20
    capcelera.contingut = u'{0}'.format('Accions')
    taula.capceleres.append( capcelera )

    taula.fileres = []
    for tutor in Professor.objects.all():
            filera = []

            #-nom--------------------------------------------
            camp = tools.classebuida()
            camp.enllac = ''
            camp.contingut = unicode(tutor)
            filera.append(camp)

            #-alumnes....................
            camp = tools.classebuida()
            camp.multipleContingut = []
            for alumne in Alumne.objects.filter( tutorindividualitzat__professor = tutor ):

                camp.enllac = ''
                camp.multipleContingut.append( (unicode(alumne) + ' (' + unicode(alumne.grup) + ')', None,) )
            filera.append(camp)

            #-accions--------------------------------------------
            camp = tools.classebuida()
            camp.enllac = '/alumnes/gestionaAlumnesTutor/{0}'.format( tutor.pk )
            camp.contingut = unicode(u"Gestiona Alumnes")
            filera.append(camp)
            taula.fileres.append( filera )

    report.append(taula)

    return report



