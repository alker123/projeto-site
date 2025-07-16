from flask import Flask, jsonify, render_template, request, session, redirect, url_for
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
            session['redirectTo'] = request.url 
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

# Rota para verificar se o usuário está autenticado
@app.route('/verificar_login')
def verificar_login():
    # Verifica se o usuário está autenticado (se a variável de sessão 'usuario' existir)
    if 'usuario' in session:
        return jsonify({'autenticado': True})
    else:
        return jsonify({'autenticado': False})

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

# Rota de logout
@app.route('/logout')
def logout():
    session.clear()  # Limpa todos os dados da sessão
    return redirect(url_for('index'))  # Redireciona para a página inicial

# Captura todas as outras rotas
@app.before_request
def redirecionar_ou_proteger_rota():
    if 'usuario' not in session:
        if request.endpoint not in ['index', 'login', 'verificar_login']:
            session['redirectTo'] = request.url  # Salva a URL original para redirecionar após o login
            return redirect(url_for('index'))  # Redireciona para o login

# Bloqueia acesso direto aos arquivos .html
@app.route('/<path:path>.html')
def redirect_html(path):
    return redirect(url_for('index'))  # Redireciona para o login se tentar acessar diretamente um arquivo .html

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, port=5000)
