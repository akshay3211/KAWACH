from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# ✅ CORS fix (VERY IMPORTANT)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# ✅ Extra headers (Chrome extension ke liye)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response


# 🔹 HEALTH CHECK (test ke liye)
@app.route('/')
def home():
    return "KAWACH Backend Running 🚀"


# 🔹 PHISHING API
@app.route('/api/phishing/check', methods=['POST', 'OPTIONS'])
def phishing():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()
        url = data.get('url')

        print("🔍 Checking URL:", url)

        # Dummy logic (baad me apna OWASP logic daalna)
        return jsonify({
            "status": "Safe",
            "risk_score": 10,
            "reasons": []
        })

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({
            "status": "Error",
            "error": str(e)
        }), 500


# 🔹 VAULT API (PASSWORD SAVE)
@app.route('/api/vault', methods=['POST', 'OPTIONS'])
def vault():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        data = request.get_json()

        website = data.get("website")
        username = data.get("username")
        password = data.get("password")

        print("🔐 Received Vault Data:")
        print("Website:", website)
        print("Username:", username)
        print("Password:", password)

        # 👉 yaha future me DB save karna
        # abhi test ke liye direct success

        return jsonify({
            "status": "Success",
            "message": "Password saved successfully"
        })

    except Exception as e:
        print("❌ Vault Error:", e)
        return jsonify({
            "status": "Error",
            "error": str(e)
        }), 500


# 🔥 IMPORTANT (Render ke liye)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
