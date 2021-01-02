import requests
import pytest
from app.controller import cidade_controller
from app.models import cidade_model
from app.models import clima_model


@pytest.mark.parametrize('id', (
        '', 'ABC', '112341233213'
))
def test_cidade_params_negative(id):
    response = requests.get("http://localhost:5000/cidade?id=" + id)
    assert response.status_code == 400


@pytest.mark.parametrize(('id'), (
        ('3801'), ('3802'), ('3803')
))
def test_cidade_params_positive(id):
    response = requests.get("http://localhost:5000/cidade?id=" + id)
    assert response.status_code == 201
    assert response.json != None


@pytest.mark.parametrize(('data_inicial', 'data_final'), (
        ('', '2020-01-02'),
        ('2020-01-02', ''),
        ('2020/01/02', '2020/01/05')
))
def test_analise_params_negative(data_inicial, data_final):
    response = requests.get("http://localhost:5000/analise?data_inicial=" + data_inicial + "&data_final=" + data_final)
    assert response.status_code == 400


@pytest.mark.parametrize(('data_inicial', 'data_final'), (
        ('2020-01-01', '2020-12-31'),
        ('2020-01-02', '2020-01-05'),
        ('2019-05-23', '2020-12-12')
))
def test_analise_params_positive(data_inicial, data_final):
    response = requests.get("http://localhost:5000/analise?data_inicial=" + data_inicial + "&data_final=" + data_final)
    assert response.status_code == 200
    assert response.json != None


clima1 = clima_model.Clima(3801, None, None, 5, None, 27)
clima2 = clima_model.Clima(3802, None, None, 10, None, 35)
clima3 = clima_model.Clima(3801, None, None, 15, None, 32)

cidade1 = cidade_model.Cidade(3801, "Teste1", None, None)
cidade2 = cidade_model.Cidade(3802, "Teste1", None, None)
cidade3 = cidade_model.Cidade(3803, "Teste1", None, None)

cidade1.clima = [clima1]
cidade2.clima = [clima2]
cidade3.clima = [clima3]

cidades = [cidade1, cidade2, cidade3]


def test_maiorTemp():
    cidade = cidade_controller.maiorTemp(cidades)
    assert cidade.id == 3803


def test_mediaPrecipitacao():
    media = cidade_controller.mediaPrecipitacao(cidades)
    assert media == 10.0
