from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import dev

app = Flask(__name__)
app.config.from_object(dev)
app.config.from_envvar('PREVISAO_TEMPO_SETTINGS',silent=True)
db = SQLAlchemy()

from app import models
from app.controller import cidade_controller

app.register_blueprint(cidade_controller.cidade_bp)

db.init_app(app)
