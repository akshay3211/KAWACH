from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# ✅ Enable CORS properly
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


# 🔥 TEMP STORAGE (RAM)
vault_data = []


# ✅ HEALTH CHECK
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "API Running 🚀"
    })


# 🔹 PHISHING API
@app.route('/api/phishing/check', methods=['POST', 'OPTIONS'])
def phishing():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    url = data.get('url')

    return jsonify({
        "status": "Safe",
        "risk_score": 10,
        "reasons": []
    })


# 🔹 VAULT API (GET + POST)
@app.route('/api/vault', methods=['GET', 'POST', 'OPTIONS'])
def vault():
    if request.method == 'OPTIONS':
        return '', 200

    global vault_data

    # 👉 SAVE DATA
    if request.method == 'POST':
        data = request.json
        print("Received:", data)

        vault_data.append(data)

        return jsonify({
            "status": "Saved",
            "total": len(vault_data)
        })

    # 👉 GET DATA
    if request.method == 'GET':
        return jsonify({
            "vault": vault_data
        })


# 🔥 OPTIONAL ROOT ROUTE (no more 404)
@app.route('/')
def home():
    return "KAWACH API RUNNING 🚀"


# 🚀 RUN
if __name__ == '__main__':
    app.run(debug=True)
