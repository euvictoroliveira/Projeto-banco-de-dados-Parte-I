#
# Arquivo principal, responsável por tratar a rota principal '/' e declarar as blueprints das outras rotas
#

from flask import Flask, render_template
from concorrencia import simular_concorrencia
from database import db

from routes.atendimento import atendimento_bp

from routes.estatisticas import estatisticas_bp

from routes.remover_Procedimento import remover_procedimento_bp

from routes.paciente import paciente_bp

from routes.home import home_bp

from routes.escala import escala_bp

from routes.views import views_bp

from routes.triggers import triggers_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:""@localhost:5432/projeto_hospital'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#
# Blueprints para outras rotas
#
app.register_blueprint(escala_bp)
app.register_blueprint(estatisticas_bp)
app.register_blueprint(paciente_bp)
app.register_blueprint(atendimento_bp)
app.register_blueprint(home_bp)
app.register_blueprint(views_bp)
app.register_blueprint(triggers_bp)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simular-concorrencia')
def simular():
    return simular_concorrencia(app)

if __name__ == '__main__':
    app.run(debug=True)