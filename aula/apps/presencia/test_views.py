"""
    This is a pytest test for presencia views

    The current aim of it is to allow getting views wrapped into an acceptable
    test coverage so it is possible to start refactoring
"""

import datetime

import pytest

from aula.utils import decorators

def test_mostraImpartir(monkeypatch):
    """ This test is aimed to get presencia.views.mostraImpartir properly tested """
    def fake_group_required(groups=[]):
        def decorator(func):
            def inner_decorator(request,*args, **kwargs):
                return func(request, *args, **kwargs)

            from django.utils.functional import wraps
            return wraps(func)(inner_decorator)

        return decorator

    # group_required decorator is accessing DB to check the group of the user. Let's say
    # always the group is there
    monkeypatch.setattr(decorators, 'group_required', fake_group_required)
    from .views import mostraImpartir
    from .views import FranjaHoraria
    from .views import Impartir
    from aula.apps.presencia import views

    class Empty:
        pass
    user = Empty()
    user.is_authenticated = lambda _ : True
    user.pk = 1000
    user.is_anonymous = True
    user.groups = Empty
    user.groups.filter = lambda _: []

    request = Empty()
    request.user = user
    request.session = Empty()
    request.session.has_key = lambda _: False       # no impersonation
    request.path_info = 'fake/path/info'

    fake_franjahoraria_objects = Empty()
    fake_franjahoraria_objects.all = lambda : ['08:15 a 09:15']
    monkeypatch.setattr(FranjaHoraria, 'objects', fake_franjahoraria_objects)

    fake_impartir_objects = Empty()                 # no impartir objects
    fake_impartir_objects.filter = lambda _: []
    monkeypatch.setattr(Impartir, 'objects', fake_impartir_objects)

    def fake_render(*args, **kwargs):
        return (args, kwargs)

    monkeypatch.setattr(views, 'render', fake_render)

    year, month, day = 2020, 1, 9
    response = mostraImpartir(request, year=year, month=month, day=day)

    expected_template = 'mostraImpartir.html' 
    found_template = response[0][1]
    assert expected_template == found_template

    expected_professor = 'None'
    found_professor = response[0][2]['professor']
    assert expected_professor == found_professor

    found_calendari = response[0][2]['calendari']
    expected_days = [ '06/01/2020', '07/01/2020', '08/01/2020', '09/01/2020', '10/01/2020']
    found_days = [ c[1] for c in found_calendari ]
    assert expected_days == found_days

    expected_impartir_tot = []
    found_impartir_tot = response[0][2]['impartir_tot']
    assert expected_impartir_tot == found_impartir_tot
    
    expected_dates_altres_moments = '2019-12-07,2019-12-30,2020-01-08,2020-01-10,2020-01-13,2020-02-05'

    found_altres_moments = response[0][2]['altres_moments']
    found_dates_altres_moments = ','.join([str(m[1]) for m in found_altres_moments if 'avui' not in m[0]])
    assert expected_dates_altres_moments == found_dates_altres_moments

    #print("XXX", found_dates_altres_moments)
    #assert False

