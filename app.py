from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
import requests
import secrets
from datetime import timedelta

app = Flask(__name__)

# Defina a chave secreta para a sessão
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')
app.permanent_session_lifetime = timedelta(minutes=30)  # Sessão expira em 30 minutos

# URL do Firebase
link = 'https://princi-4dfd7-default-rtdb.firebaseio.com/'

# Função para proteger as rotas
def proteger_rota(f):
    def wrap(*args, **kwargs):
        if 'usuario' not in session or 'token' not in session:
            session['redirectTo'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Página inicial (login)
@app.route('/')
def index():
    if 'usuario' in session and 'token' in session:
        return redirect(url_for('operador'))
    return render_template('index.html')

# Rota para buscar dados no Firebase (exemplo)
@app.route('/dados')
def dados():
    response = requests.get(f"{link}/dados.json")
    data = response.json()
    return str(data)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        usuario = data.get('usuario')
        senha = data.get('senha')

        response = requests.get(f"{link}/usuarios/{usuario}.json")
        if response.status_code != 200:
            return {'success': False, 'message': 'Erro ao acessar o banco de dados'}, 500

        dados = response.json()

        if dados and dados.get('senha') == senha:
            session.permanent = True
            session['usuario'] = usuario
            session['rota'] = dados.get('rota', 'default')
            session['token'] = secrets.token_hex(16)  # Token aleatório

            redirect_to = session.get('redirectTo', f'/{dados["rota"].replace(".html", "")}')
            session.pop('redirectTo', None)

            return {'success': True, 'rota': redirect_to}
        else:
            return {'success': False, 'message': 'Usuário ou senha incorretos'}, 401

    return render_template('index.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Rotas protegidas
@app.route('/operador')
@proteger_rota
def operador():
    return render_template('operador.html')

@app.route('/admin')
@proteger_rota
def admin():
    return render_template('admin.html')

@app.route('/juradoA')
@proteger_rota
def juradoA():
    return render_template('juradoA.html')

@app.route('/juradoB')
@proteger_rota
def juradoB():
    return render_template('juradoB.html')

@app.route('/juradoC')
@proteger_rota
def juradoC():
    return render_template('juradoC.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)
