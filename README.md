## Previsao do Tempo

è um webservice que utilize um serviço de previsão do tempo  e persista os dados no banco de dados relacional com uma
interface para consumo externo.

## Objetivo

Demonstrar os conhecimentos de Python usando o Framework Flask, no banco de dados foi utilizado SQLAlchemy por ter flexibilidade em mapear objetos relacionais com suporte ao SQLite e foram implementados conhecimentos como Clean Code e MVC. 

## Tecnológias utilizadas

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) 

- [SQLalchemy](https://www.sqlalchemy.org/).

- [Swagger](https://swagger.io/)

## Install

### Linux

 ```shell
sudo apt-get install python3
sudo apt-get install python3-venv
 ```

<b>Instalando dependencias <b><br/>
 
 ```shell
 python3 -m venv ven
 pip install -r requirements.txt
 ```

### Run
 ```shell
python -m flask run
```

### Teste
 ```shell
export PREVISAO_TEMPO_SETTINGS=config/test.py
python -m flask run
python -m pytest
```

## Docs
<span style="color:cornflowerblue">GET</span> /api/docs  

URL: http://localhost:5000/api/docs  


## Exemplo de código

```Python
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
```

## Licença

[Gabriel Lorandi](https://www.linkedin.com/in/gabriel-lorandi/)

 
