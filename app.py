#
# Arquivo principal, responsável por tratar a rota principal '/' e declarar as blueprints das outras rotas
#

from flask import Flask, render_template
from database import db

from routes.atendimento import listar_atendimentos_bp, novo_atendimento_bp, listar_procedimentos_bp

from routes.estatisticas import estatisticas_bp

from routes.remover_Procedimento import remover_procedimento_bp

from routes.atendimento_unificado import atendimento_bp

from routes.paciente_unificadp import paciente_bp

from routes.Home import home_bp

from routes.views import views_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:""@localhost:5432/projeto_hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#
# Blueprints para outras rotas
#
app.register_blueprint(listar_procedimentos_bp)
app.register_blueprint(estatisticas_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(atendimento_bp)
app.register_blueprint(home_bp)
app.register_blueprint(views_bp)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)