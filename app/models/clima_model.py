from app import db
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime


DATA_FORMAT = '%Y-%m-%d'


class Clima(db.Model):
    __tablename__ = 'clima'
    id = Column('id',Integer, primary_key=True)
    cidade_id = Column('cidade_id',Integer, ForeignKey('cidade.id'))
    data = Column('data', DateTime, nullable=False)
    probalidade = Column('probalidade', Integer, nullable=False)
    precipitacao = Column('precipitacao', Integer, nullable=False)
    minTemp = Column('minTemp', Integer, nullable=False)
    maxTemp = Column('maxTemp', Integer, nullable=False)

    def __init__(self,cidade_id,data,probalidade,precipitacao,minTemp,maxTemp):
        self.cidade_id = cidade_id
        self.data = data
        self.probalidade = probalidade
        self.precipitacao = precipitacao
        self.minTemp = minTemp
        self.maxTemp = maxTemp

    def serialize(self):
        return {
            'data': self.data,
            'probalidade': self.probalidade,
            'precipitacao': self.precipitacao,
            'minTemp': self.minTemp,
            'maxTemp': self.maxTemp
        }


def getAll(dataInicial, dataFinal):
    return db.session.query(Clima)\
        .filter(Clima.data >= dataInicial, Clima.data <= dataFinal).all()


def findByData(json):
    date_format = datetime.strptime(json['date'], DATA_FORMAT)

    return db.session.query(Clima).filter(Clima.data == date_format).first()


def save(cidadeId,json):
    date_format = datetime.strptime(json['date'], DATA_FORMAT)

    clima = Clima(cidadeId,
                  date_format,
                  json['rain']['probability'],
                  json['rain']['precipitation'],
                  json['temperature']['min'],
                  json['temperature']['max'])

    db.session.add(clima)
    db.session.commit()

    return clima