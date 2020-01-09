"""
    This module tests utilities of alumnes app
"""
from datetime import date

from django.test import TestCase

from aula.apps.alumnes.models import Nivell, Curs, Grup
from .utils import duplicats_rpt
from .models import Alumne

from aula.utils.testing.tests import TestUtils

class ReportDuplicatsTest(TestCase):

    def setUp(self):
        DAM = Nivell.objects.create(nom_nivell='DAM') #type: Nivell
        primerDAM = Curs.objects.create(nom_curs='1er', nivell=DAM) #type: Curs
        self.primerDAMA = Grup.objects.create(nom_grup='A', curs=primerDAM) #type: Grup
        self.tUtils = TestUtils()

    def test_sense_duplicats_quan_difereixen_en_cognom_i_dataneixement(self):
        alumne = self.tUtils.afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 7), self.primerDAMA)
        alumne = self.tUtils.afegeix_alumne_a_grup('Mariola', 'Ganapia', date(2000, 7, 8), self.primerDAMA)
        report = duplicats_rpt()[0]
        self.assertEqual(len(report.fileres), 0, "Sobren duplicats")

    def test_duplicats_quan_hi_ha_duplicats_amb_nom_cognoms_i_datanaixement(self):
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 7), self.primerDAMA)
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 7), self.primerDAMA)
        report = duplicats_rpt()[0]
        self.assertEqual(len(report.fileres), 2, "Falten duplicats quan nom, cognoms i data naixement coincideixen")

    def test_duplicats_quan_hi_ha_duplicats_amb_nom_cognoms_i_datanaixement(self):
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 7), self.primerDAMA)
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 8), self.primerDAMA)
        report = duplicats_rpt()[0]
        self.assertEqual(len(report.fileres), 2, "Falten duplicats quan nom, cognoms i altres coincideixen")

    def test_duplicats_quan_hi_ha_duplicats_amb_nom_i_datanaixement(self):
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 7), self.primerDAMA)
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ganapia', date(2000, 7, 7), self.primerDAMA)
        report = duplicats_rpt()[0]
        self.assertEqual(len(report.fileres), 2, "Falten duplicats quan nom, cognoms i data naixement coincideixen")

    def test_duplicats_quan_hi_ha_duplicats_amb_nom_i_datanaixement_pero_no_cognom(self):
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ripoll', date(2000, 7, 7), self.primerDAMA)
        alumne = TestUtils().afegeix_alumne_a_grup('Mariola', 'Ganapia', date(2000, 7, 7), self.primerDAMA)
        alumne = TestUtils().afegeix_alumne_a_grup('Sebastià', 'Ganapia', date(2000, 7, 7), self.primerDAMA)
        report = duplicats_rpt()[0]
        self.assertEqual(len(report.fileres), 2, "Podria estar comptant com a duplicats quan coincideixen en cognom i data naixement")

