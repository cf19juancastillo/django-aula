"""
    MGG 20191216

    He extret aquests tests de tests.py per estudiar-los

"""
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

import logging


class MySeleniumTests(SeleniumLiveServerTestCase):

    def setUp(self):
        self.db = TestDBCreator()
        #self.selenium = WebDriver()
        options = webdriver.FirefoxOptions()
        #Opció que mostra el navegador o no el mostra (prefereixo que no el mostri així puc programar mentre executo tests.)
        options.add_argument('-headless')

        self.selenium = webdriver.Firefox(firefox_options=options)

        self.selenium.implicitly_wait(5)

        logging.basicConfig(filename='/tmp/djau.log',level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    def tearDown(self):
        self.selenium.close()

    #def test_comprovarOpcioForcarTreure(self):
    #    #Login
    #    #Passa llista tot a present alumne X fa falta.
    #    #Treure alumne X de la hora. No marcar la opció forçar, comprovar que l'alumne continua present.
    #    #Treure alumne X de la hora. Marcar la opció forçar. Comprovar que l'alumne no està dins la hora.
    #    self.loginUsuari()
    #    self.selenium.get(self.live_server_url + '/presencia/afegeixAlumnesLlista/' +
    #        str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')

    #    alumneX=self.db.alumnes[0]
    #    self.seleccionarAlumne(alumneX.pk)
    #    self.seleccionarAlumne(self.db.alumnes[1].pk)
    #    self.seleccionarAlumne(self.db.alumnes[2].pk)
    #    self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    #    cas=ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
    #    casAlumneX = cas.get(alumne=alumneX)
    #    for ca in cas:
    #        self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_0"); x.click()'.format(ca.pk))
    #    self.selenium.execute_script('x=document.getElementById("label_id_{}-estat_1"); x.click()'.format(casAlumneX.pk))
    #    self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    #    self.selenium.get(self.live_server_url + '/presencia/treuAlumnesLlista/' +
    #        str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')
    #    self.seleccionarAlumne(alumneX.pk)
    #    self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    #    caAlumneX=ControlAssistencia.objects.get(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk, alumne=alumneX) #type: ControlAssistencia
    #    estat = caAlumneX.estat #type: EstatControlAssistencia
    #    self.assertTrue(estat.codi_estat=='F')

    #    self.selenium.get(self.live_server_url + '/presencia/treuAlumnesLlista/' +
    #        str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')
    #    self.seleccionarAlumne(alumneX.pk)
    #    botoTreureTot = self.selenium.find_element_by_id("id_tots-matmulla")
    #    botoTreureTot.click()
    #    self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    #    caAlumnes=ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk, alumne=alumneX) #type: ControlAssistencia
    #    self.assertTrue(len(caAlumnes) == 0)

    #def test_treureAlumnes(self):
    #    self.loginUsuari()

    #    self.selenium.get(self.live_server_url + '/presencia/afegeixAlumnesLlista/' +
    #        str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')
    #    #Comprovar quants alumnes hi ha seleccionats en aquesta hora. No n'hi hauria d'haver cap.
    #    cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
    #    self.assertTrue(len(cas)==0)

    #    #Seleccionar dos usuaris.
    #    for i in range(0,2):
    #        js = """ x = document.evaluate('//input[@type=\\\'checkbox\\\' and @value="""+str(self.db.alumnes[i].pk)+"""]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null );
    #                x.singleNodeValue.click();
    #            """
    #        self.selenium.execute_script(js)
    #    #import ipdb; ipdb.set_trace()
    #    self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    #    #Comprovar alumnes en aquesta hora, n'hi hauria d'haver-hi dos.
    #    cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
    #    self.assertTrue(len(cas)==2)

    #    self.selenium.get(self.live_server_url + '/presencia/treuAlumnesLlista/' +
    #        str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')

    #    #Seleccionar dos usuaris.
    #    js = """ x = document.evaluate('//input[@type=\\\'checkbox\\\' and @value="""+str(self.db.alumnes[0].pk)+"""]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null );
    #            x.singleNodeValue.click();
    #        """
    #    self.selenium.execute_script(js)
    #    self.selenium.find_elements_by_xpath("//button[@type='submit']")[0].click()

    #    #Queda només un usuari.
    #    cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
    #    self.assertTrue(len(cas)==1)

    #def test_afegirAlumnes(self):
    #    #Afegeix alumnes i comprova que hi siguin.
    #    self.loginUsuari()

    #    self.selenium.get(self.live_server_url + '/presencia/afegeixAlumnesLlista/' +
    #        str(self.db.programacioDillunsHoraBuidaAlumnes.pk) + '/')
    #    #Comprovar quants alumnes hi ha seleccionats en aquesta hora. No n'hi hauria d'haver cap.
    #    cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
    #    self.assertTrue(len(cas)==0)

    #    #Seleccionar uns quants usuaris.
    #    self.selenium.execute_script('''
    #       cbox = document.getElementsByTagName("input");
    #           for (i=0;i<cbox.length;i++){
    #               if (cbox[i].type == "checkbox") {
    #               console.log("hola:" + cbox[i].type);
    #               cbox[i].click()
    #           }
    #       }'''
    #    )
    #    botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
    #    botons[0].click()

    #    #Comprovar alumnes en aquesta hora, hi haurien de ser tots.
    #    cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDillunsHoraBuidaAlumnes.pk)
    #    self.assertTrue(len(cas)==self.db.nAlumnesGrup)

    def test_passaLlista(self):
        """ Aquest test selecciona un grup per passar llista
            Posa com a present el primer alumne i la resta com a faltes
        """
        #Passar llista convencional.
        logging.info('XXX test_passaLlista() starts')
        self.loginUsuari()

        url = self.live_server_url + '/presencia/passaLlista/' + str(self.db.programacioDiaAnterior.pk) + '/'
        logging.info(f"XXX\t getting url {url}")
        self.selenium.get(url)

        #Obtenir tots els controls d'assistenica de l'hora marcada
        cas=ControlAssistencia.objects.filter(impartir_id=self.db.programacioDiaAnterior.pk)

        # Seleccionar primer alumne per marcar-lo com a present (estat_0)
        css_selector = f"#label_id_{cas[0].pk}-estat_0"
        self.selenium.find_elements_by_css_selector(css_selector)[0].click()

        for i in range(1, len(cas)):
            # Selecciona la resta d'elements per marcar-los com a absents (estat_1)
            css_selector = f"#label_id_{cas[i].pk}-estat_1"
            self.selenium.find_elements_by_css_selector(css_selector)[0].click()

        # Envia el formulari amb la llista passada
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        botons[0].click()

        # Comprovar que tots els controls han quedat marcats. (He posat faltes a tots menys al primer)
        cas = ControlAssistencia.objects.filter(impartir_id=self.db.programacioDiaAnterior.pk)
        self.assertTrue(cas[0].estat.codi_estat=='P')
        for i in range(1, len(cas)):
            self.assertTrue(cas[i].estat.codi_estat=='F')

    def loginUsuari(self):
        """ realitza la seqüència de loging """
        self.selenium.get( self.live_server_url + '/usuaris/login/')
        #localitza usuari i paraulaDePas
        inputUser = self.selenium.find_element_by_name("usuari")
        inputUser.clear()
        inputUser.send_keys('SrProgramador')
        inputParaulaDePas = self.selenium.find_element_by_name("paraulaDePas")
        inputParaulaDePas.clear()
        inputParaulaDePas.send_keys('patata')
        botons = self.selenium.find_elements_by_xpath("//button[@type='submit']")
        boto = botons[0]
        boto.click()

    def seleccionarAlumne(self, codiAlumne):
        #type: (int)->None
        js = """ x = document.evaluate('//input[@type=\\\'checkbox\\\' and @value="""+str(codiAlumne)+"""]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null );
                    x.singleNodeValue.click();
                """
        self.selenium.execute_script(js)
