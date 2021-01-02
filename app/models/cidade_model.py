from sqlalchemy.orm import relationship, contains_eager
from sqlalchemy import Column, Integer, String
from app import db
from app.models.clima_model import Clima


class Cidade(db.Model):
    __tablename__ = 'cidade'
    id = Column('id', Integer, primary_key=True)
    nome = Column('nome', String(50), nullable=False)
    estado = Column('estado', String(3), nullable=False)
    pais = Column('pais', String(3), nullable=False)
    clima = relationship("Clima")

    def __init__(self, id, nome, estado, pais):
        self.id = id
        self.nome = nome
        self.estado = estado
        self.pais = pais

    def serialize(self):
        climas = []
        if self.clima:
            climas = [clima.serialize() for clima in self.clima]

        return {
            'id': self.id,
            'nome': self.nome,
            'estado': self.estado,
            'pais': self.pais,
            'climas': climas
        }


def getAll(dataInicial, dataFinal):
    result = db.session.query(Cidade) \
        .options(contains_eager(Cidade.clima)) \
        .join(Clima) \
        .filter(Clima.data >= dataInicial, Clima.data <= dataFinal) \
        .all()

    return result


def getOne(id):
    return db.session.query(Cidade).get(id)


def save(json):
    cidade = Cidade(json['id'],
                    json['name'],
                    json['state'],
                    json['country'])

    db.session.add(cidade)
    db.session.commit()

    return cidade