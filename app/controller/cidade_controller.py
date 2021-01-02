from flask import Blueprint, jsonify, request, render_template
from app.models import clima_model, cidade_model
from datetime import datetime
from app import db

import requests

cidade_bp = Blueprint("cidadeController", __name__)

PATH = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/ID/days/15?token=TOKEN'
TOKEN = 'b22460a8b91ac5f1d48f5b7029891b53'


@cidade_bp.before_request
def create_database():
    db.create_all()
    pass


@cidade_bp.route('/api/docs')
def get_docs():
    return render_template('swaggerui.html')

@cidade_bp.errorhandler(Exception)
def error_handle(err):
    if (isinstance(err, ValueError)):
        return jsonify(err=err.args[0],
                       msg="Parâmetros no formato inválido"), 400

    return jsonify(err=err.args[0],
                   msg="Ops! Aconteceu algo de errado, "
                       "golfinhos treinados estão consertando o problema,"
                       "tente novamente dentro de algumas minutos"), 500


@cidade_bp.route('/analise', methods=["GET"])
def analise():
    if 'data_inicial' and 'data_final' in request.args:
        dataInicial = datetime.strptime(request.args.get('data_inicial'), '%Y-%m-%d')
        dataFinal = datetime.strptime(request.args.get('data_final'), '%Y-%m-%d')
    else:
        return jsonify(msg="Parâmetros data_inicial ou data_final não encontrados."), 400

    cidades = cidade_model.getAll(dataInicial, dataFinal)

    maiorTempCidade = maiorTemp(cidades)
    media = mediaPrecipitacao(cidades)

    if maiorTempCidade is None:
        return jsonify(maior_temperatura_cidade=maiorTempCidade, media=media), 200

    return jsonify(maior_temperatura_cidade=maiorTempCidade.serialize(), media=media), 200


@cidade_bp.route('/cidade', methods=["GET"])
def cidade():
    if 'id' in request.args:
        idCidade = request.args.get('id')
    else:
        return jsonify(msg="Parâmetro id não encontrado"), 400

    url = PATH
    url = url.replace('ID', idCidade).replace('TOKEN', TOKEN)

    resposta = requests.get(url)

    status = resposta.status_code

    json = resposta.json()

    if status != 200:
        return jsonify(msg=json["detail"]), status

    cidade = cidade_model.getOne(json['id'])

    if cidade is None:
        cidade = saveCidade(json)
    else:
        cidade = updateCidade(cidade, json)

    return jsonify(cidade=cidade.serialize()), 201


def saveCidade(json):
    add = cidade_model.save(json)

    for data in json['data']:
        clima_model.save(add.id, data)

    return add


def updateCidade(update, json):
    for data in json['data']:
        clima = clima_model.findByData(data)

        if clima is None:
            clima_model.save(update.id, data)

    return update


def maiorTemp(cidades):
    cidadeMaiorTemp = None
    for cidade in cidades:

        climaMaiorTemp = None

        for clima in cidade.clima:
            if climaMaiorTemp is None or clima.maxTemp > climaMaiorTemp.maxTemp:
                climaMaiorTemp = clima
                cidadeMaiorTemp = cidade

    return cidadeMaiorTemp


def mediaPrecipitacao(cidades):
    if len(cidades) == 0:
        return None

    mediaPrecipitacaoCidades = 0

    for cidade in cidades:

        mediaPrecipitacaoClimas = 0
        for clima in cidade.clima:
            mediaPrecipitacaoClimas += clima.precipitacao

        mediaPrecipitacaoCidades += mediaPrecipitacaoClimas

    return mediaPrecipitacaoCidades / len(cidades)
