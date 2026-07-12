#
# Arquivo principal, responsável por tratar a rota principal '/' e declarar as blueprints das outras rotas
#

from flask import Flask, render_template
from routes.atendimento import atendimento_bp

app = Flask(__name__)

#
# Blueprints para outras rotas
#
app.register_blueprint(atendimento_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atendimento')
def atendimento():
    return render_template('atendimento.html')

if __name__ == '__main__':
    app.run(debug=True)