#encoding: utf-8
import re
from datetime import date, timedelta

from django.test import TestCase, LiveServerTestCase
from django.test import Client
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox import webelement

from aula.apps.alumnes.models import Nivell, Curs, Grup
from aula.apps.horaris.models import DiaDeLaSetmana, FranjaHoraria, Horari
from aula.apps.assignatures.models import Assignatura, TipusDAssignatura
from aula.apps.presencia.models import Impartir, ControlAssistencia, EstatControlAssistencia
from aula.apps.presencia.test.testDBCreator import TestDBCreator
from aula.utils.testing.tests import SeleniumLiveServerTestCase

class SimpleTest(TestCase):

    def setUp(self):
        self.db = TestDBCreator()
        self.url = 'http://localhost:8000'

    def test_numeroAlumnesMostratsEsCorrecte(self):
        c = Client()
        response = c.post(self.url + '/usuaris/login/', {'usuari':'SrProgramador', 'paraulaDePas':'patata'})
        response = c.get( self.url + '/presencia/passaLlista/' + str(self.db.programacioDiaAnterior.pk) + '/')
        c:bytes = response.content
        nBotonsPresent = c.count(b"btn btn-default btnPresent")
        self.assertTrue(nBotonsPresent == self.db.nAlumnesGrup, "Error falten usuaris en el llistat")

    def test_passarLlistaModificaBD(self):
        c = Client()
        response = c.post(self.url + '/usuaris/login/', {'usuari':'SrProgramador', 'paraulaDePas':'patata'})
        response = c.get(self.url + '/presencia/passaLlista/' + str(self.db.programacioDiaAnterior.pk) + '/')
        #Localitzar els CA's que cal enviar.
        estatsAEnviar=self.obtenirEstats(response.content.decode('utf-8'))

        response = c.post(self.url + '/presencia/passaLlista/' + str(self.db.programacioDiaAnterior.pk) + '/',
         estatsAEnviar)

        #Comprova que ha canviat l'estat.
        controlsAssistencia = ControlAssistencia.objects.filter(impartir=self.db.programacioDiaAnterior, estat=self.db.estats['p'])
        self.assertTrue(len(controlsAssistencia) == self.db.nAlumnesGrup,
            "Error el número de controls d'assisència marcats com a present hauria de ser " + str(self.db.nAlumnesGrup) +
            "i és:" + str(len(controlsAssistencia)))

    def obtenirEstats(self, html:str):
        valorsAEnviar={}

        matches=re.findall('name="[0-9]+-estat"', html)
        for match in matches:
            coincidencia = str(match)[6:-1]
            valorsAEnviar[coincidencia] = self.db.estats['p'].pk
        return valorsAEnviar


