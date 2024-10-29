import os
from flask import Flask, render_template, request, jsonify
import redis
import string
import random
from prometheus_client import Counter, start_http_server, generate_latest

app = Flask(__name__)

# Flask server port
port = int(os.getenv("PORT", 5000))

# Redis configuration
redis_host = os.environ.get('REDIS_HOST', 'redis-service')
redis_port = 6379
redis_password = ""

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

# Prometheus counter
senha_gerada_counter = Counter('senha_gerada', 'Contador de senhas geradas')

def criar_senha(tamanho, incluir_numeros, incluir_caracteres_especiais):
    caracteres = string.ascii_letters
    if incluir_numeros:
        caracteres += string.digits
    if incluir_caracteres_especiais:
        caracteres += string.punctuation
    senha = ''.join(random.choices(caracteres, k=tamanho))
    return senha

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tamanho = int(request.form.get('tamanho', 8))
        incluir_numeros = request.form.get('incluir_numeros') == 'on'
        incluir_caracteres_especiais = request.form.get('incluir_caracteres_especiais') == 'on'
        senha = criar_senha(tamanho, incluir_numeros, incluir_caracteres_especiais)
        r.lpush("senhas", senha)
        senha_gerada_counter.inc()
    senhas = r.lrange("senhas", 0, 9)
    senhas_geradas = [{"id": index + 1, "senha": senha} for index, senha in enumerate(senhas)]
    senha_gerada = senhas_geradas[0]['senha'] if senhas_geradas else ''
    return render_template('index.html', senhas_geradas=senhas_geradas, senha=senha_gerada)

@app.route('/api/gerar-senha', methods=['POST'])
def gerar_senha_api():
    dados = request.get_json()
    tamanho = int(dados.get('tamanho', 8))
    incluir_numeros = dados.get('incluir_numeros', False)
    incluir_caracteres_especiais = dados.get('incluir_caracteres_especiais', False)
    senha = criar_senha(tamanho, incluir_numeros, incluir_caracteres_especiais)
    r.lpush("senhas", senha)
    senha_gerada_counter.inc()
    return jsonify({"senha": senha})

@app.route('/api/senhas', methods=['GET'])
def listar_senhas():
    senhas = r.lrange("senhas", 0, 9)
    resposta = [{"id": index + 1, "senha": senha} for index, senha in enumerate(senhas)]
    return jsonify(resposta)

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    
    metrics_port = int(os.getenv("METRICS_PORT", 8088))
    start_http_server(metrics_port)
    
    app.run(host="0.0.0.0", port=port, debug=False)
