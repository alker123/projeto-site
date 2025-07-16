from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import os
from firebase import initialize_all_firebase_apps  # Importa a função de inicialização
from firebase_admin import db

# Inicializar ambos os bancos de dados Firebase
initialize_all_firebase_apps()

app = Flask(__name__)

# Defina a chave secreta para a sessão
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# Função para proteger as rotas
def proteger_rota(f):
    def wrap(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('index'))  # Redireciona para a página de login se não estiver logado
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Rota inicial (Página de Login)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para pegar dados do Firebase (apenas exemplo)
@app.route('/dados')
def dados():
    # Usando o app1 para acessar o banco Firebase
    ref = db.reference('dados', app=firebase_admin.get_app("app1"))
    data = ref.get()  # Obter dados do Firebase

    return jsonify(data)  # Retorna os dados em formato JSON

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recebe os dados JSON do frontend
    usuario = data.get('usuario')
    senha = data.get('senha')

    # Conectar ao Firebase para verificar dados do usuário
    ref = db.reference(f'usuarios/{usuario}', app=firebase_admin.get_app("app1"))
    dados = ref.get()

    # Verifica se o usuário existe e se a senha está correta
    if dados and dados.get('senha') == senha:
        session['usuario'] = usuario  # Armazenando o usuário na sessão
        session['rota'] = dados.get('rota', 'default')  # Armazenando a rota do usuário (por exemplo, 'admin.html')
        
        # Calcula a página de redirecionamento
        redirect_to = session.get('redirectTo', f'/{dados["rota"].replace(".html", "")}')
        
        # Limpa a variável de redirecionamento após usá-la
        session.pop('redirectTo', None)
        
        return {'success': True, 'rota': redirect_to}  # Retorna a resposta no formato JSON
    else:
        return {'success': False, 'message': 'Usuário ou senha incorretos'}, 401
    
    
    
    
    
    from flask import Flask, render_template, request, session, redirect, url_for
import os
import requests

app = Flask(__name__)

# Defina a chave secreta para a sessão
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')

# URL do Firebase (base da URL do banco de dados)
link = 'https://princi-4dfd7-default-rtdb.firebaseio.com/'


# Função para proteger as rotas
def proteger_rota(f):
    def wrap(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('index'))  # Redireciona para a página de login se não estiver logado
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Rota inicial (Página de Login)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para pegar dados do Firebase (apenas exemplo)
@app.route('/dados')
def dados():
    response = requests.get(f"{link}/dados.json")  # URL do banco de dados + endpoint
    data = response.json()  # Parse da resposta JSON
    return str(data)  # Retorna os dados em formato de string

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recebe os dados JSON do frontend
    usuario = data.get('usuario')
    senha = data.get('senha')

    # Conectar ao Firebase e verificar dados do usuário
    response = requests.get(f"{link}/usuarios/{usuario}.json")  # Obtém os dados do usuário pelo ID (email)
    
    # Verifica se o Firebase retornou dados para o usuário
    if response.status_code != 200:
        return {'success': False, 'message': 'Erro ao acessar o banco de dados'}, 500

    dados = response.json()

    # Verifica se o usuário existe e se a senha está correta
    if dados and dados.get('senha') == senha:
        session['usuario'] = usuario  # Armazenando o usuário na sessão
        session['rota'] = dados.get('rota', 'default')  # Armazenando a rota do usuário (por exemplo, 'admin.html')
        
        # Calcula a página de redirecionamento
        redirect_to = session.get('redirectTo', f'/{dados["rota"].replace(".html", "")}')
        
        # Limpa a variável de redirecionamento após usá-la
        session.pop('redirectTo', None)
        
        return {'success': True, 'rota': redirect_to}  # Retorna a resposta no formato JSON
    else:
        return {'success': False, 'message': 'Usuário ou senha incorretos'}, 401