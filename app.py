from flask import Flask, send_from_directory
from routes import rotas  # ← adicionar

app = Flask(__name__)
app.secret_key = "intranet-2025"

app.register_blueprint(rotas)  # ← adicionar

@app.route('/')
def index():
    return send_from_directory('static', 'login.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('static', 'dashboard.html')

@app.route('/disciplinas')
def disciplinas():
    return send_from_directory('static', 'disciplinas.html')

@app.route('/disciplinas/algoritmos')
def algoritmos():
    return send_from_directory('static', 'algoritmos.html')

@app.route('/disciplinas/programacao-estruturada')
def programacao_estruturada():
    return send_from_directory('static', 'programacao-estruturada.html')

@app.route('/disciplinas/aplicativos-computacionais')
def aplic_computacionais():
    return send_from_directory('static', 'aplicativos-computacionais.html')

@app.route('/disciplinas/comunicacao-organizacional')
def comunicacao_org():
    return send_from_directory('static', 'comunicacao-organizacional.html')

@app.route('/disciplinas/etica-e-responsabilidade-social')
def etica():
    return send_from_directory('static', 'etica-e-responsabilidade-social.html')

@app.route('/disciplinas/programacao-para-web-i')
def programacao_web_1():
    return send_from_directory('static', 'programacao-web-1.html')

@app.route('/noticias')
def noticias():
    return send_from_directory('static', 'noticias.html')

@app.route('/documentacao')
def documentacao():
    return send_from_directory('static', 'documentacao.html')

@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')

if __name__ == "__main__":
    print("Servidor rodando em http://localhost:5000")
    app.run(debug=True)