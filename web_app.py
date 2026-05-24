from flask import Flask, render_template, request, jsonify
import requests
import json
from modules import ip_tracker, username_tracker

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track_ip', methods=['POST'])
def track_ip():
    ip = request.json.get('ip')
    response = requests.get(f"http://ip-api.com/json/{ip}")
    return jsonify(response.json())

@app.route('/search_user', methods=['POST'])
def search_user():
    username = request.json.get('username')
    # Implementar búsqueda real
    return jsonify({"status": "Buscando..."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
