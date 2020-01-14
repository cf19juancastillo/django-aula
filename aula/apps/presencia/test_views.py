"""
    This is a pytest test for presencia views

    The current aim of it is to allow getting views wrapped into an acceptable
    test coverage so it is possible to start refactoring
"""

import datetime

import pytest

from aula.utils import decorators
from django.contrib.auth.models import Group
from .views import mostraImpartir
from .views import FranjaHoraria
from .views import Impartir
from .views import User2Professor
from aula.apps.presencia import views

class Empty:
    def __init__(self, params=None):
        if params:
            self.__dict__ = params
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return self.__str__()

@pytest.fixture()
def fake_db():
    """ definition of the db cases """

    class RequestMessages:
        def __init__(self):
            self.contents = []
        def add(self, level, message, extra_tag):
            self.contents.append(f'level: {level} msg: {message} extra_tag:{extra_tag}')

    db = {
        'request' : Empty({
            'user': Empty(
                {
                    'pk': 1001,
                    'is_authenticated': lambda _: True,
                    'groups': Empty({
                        'objects': Empty({
                            'get': lambda _: ['professors'],
                        }),
                        'all': lambda: ['professors'],
                    })
                }),
            'session': Empty({
                'has_key': lambda _: False,       # no impersonation
            }),
            'path_info': 'fake/path/info',
            '_messages': RequestMessages(),
        }),
        'imparticions': [
            [ 
                Empty({
                    'horari': Empty({
                        #'08:15 a 09:15',
                        'assignatura': Empty({'nom_assignatura':'TEC'}),
                        'grup': None,
                    }),
                    'get_nom_aula': 'Aula1',
                    'color': lambda: None,
                    'resum': lambda: None,
                    'pk': 1002,
                    'professor_guardia': Empty({'pk': 1001}),
                    'hi_ha_alumnes_amb_activitat_programada': False,
                    'esReservaManual': False,
                }),

                Empty({
                    'horari': Empty({
                        'assignatura': Empty({'nom_assignatura':'NAT'}),
                        'grup': None,
                    }),
                    'get_nom_aula': 'Aula1',
                    'color': lambda: None,
                    'resum': lambda: None,
                    'pk': 1003,
                    'professor_guardia': Empty({'pk': 1004}),
                    'hi_ha_alumnes_amb_activitat_programada': True,
                    'esReservaManual': False,
                })

            ]
        ],
        'groups': [
            'professors',
        ],
        'horaris':[
            ['08:15 a 09:15', '09:15 a 10:15'],
        ],
        'dates':[
            (2020, 1, 9),
        ]
    }
    return db


@pytest.fixture()
def expected():
    """ composes and returns the expected values for each test set """
    return [
        {
            'expected_template' : 'mostraImpartir.html',
            'expected_professor_pk': "'pk': 1001",
            'expected_days' : [ '06/01/2020', '07/01/2020', '08/01/2020', '09/01/2020', '10/01/2020'],

            'expected_impartir_tot' : [[[[('08:15 a 09:15', '', '', '', '', '', '', '', '', '')], None],
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               True),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False)],
                             [[[('09:15 a 10:15', '', '', '', '', '', '', '', '', '')], None],
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               True),
                              ([('TEC', '', 'Aula1', 1002, '#softcolor', None, None, True, False, False),
                                ('NAT', '', 'Aula1', 1003, '#softcolor', None, None, False, True, False)],
                               False)]],

            'expected_dates_altres_moments' : '2019-12-07,2019-12-30,2020-01-08,2020-01-10,2020-01-13,2020-02-05',
        },
    ]



@pytest.mark.parametrize("test_set", [0,],)
def test_mostraImpartir_with_imparticions(monkeypatch, fake_db, expected, test_set):
    """ This test is aimed to get presencia.views.mostraImpartir properly tested """

    def fake_group_objects_get(**kwargs):
        return fake_db['groups'][0]

    def fake_render(*args, **kwargs):
        return (args, kwargs)


    # let's monkeypatch
    monkeypatch.setattr(Group, 'objects', Empty({
        'get': fake_group_objects_get
    }))
    monkeypatch.setattr(views, 'User2Professor', lambda u: u)
    monkeypatch.setattr(views, 'getSoftColor', lambda _: '#softcolor')
    monkeypatch.setattr(FranjaHoraria, 'objects', Empty({
        'all': lambda : fake_db['horaris'][test_set],
    }))
    monkeypatch.setattr(Impartir, 'objects', Empty({
        'filter': lambda _: fake_db['imparticions'][test_set]
    }))
    monkeypatch.setattr(views, 'render', fake_render)


    # call to the function under test
    year, month, day = fake_db['dates'][test_set]
    response = mostraImpartir(fake_db['request'], year=year, month=month, day=day)


    # assertion bunch
    found_template = response[0][1]
    assert expected[test_set]['expected_template'] == found_template

    found_professor = response[0][2]['professor']
    assert expected[test_set]['expected_professor_pk'] in found_professor

    found_calendari = response[0][2]['calendari']
    found_days = [ c[1] for c in found_calendari ]
    assert expected[test_set]['expected_days'] == found_days


    found_impartir_tot = response[0][2]['impartir_tot']
    assert expected[test_set]['expected_impartir_tot'] == found_impartir_tot


    found_altres_moments = response[0][2]['altres_moments']
    found_dates_altres_moments = ','.join([str(m[1]) for m in found_altres_moments if 'avui' not in m[0]])
    assert expected[test_set]['expected_dates_altres_moments'] == found_dates_altres_moments


    #assert False


