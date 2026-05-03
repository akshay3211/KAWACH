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

@app.route('/api/vault', methods=['GET', 'POST'])
def manage_vault():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # For prototype, assume user_id = 1
        user_id = 1
        
        # Ensure dummy user exists
        cursor.execute("INSERT OR IGNORE INTO users (id, username, password_hash) VALUES (1, 'admin', 'dummyhash')")
        conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to initialize vault connection: {e}")
        return jsonify({"status": "Error", "message": f"Database connection failed: {str(e)}"}), 500
    
    if request.method == 'POST':
        try:
            data = request.json
            website = data.get('website')
            username = data.get('username')
            password = data.get('password')
            
            if not all([website, username, password]):
                return jsonify({"status": "Error", "message": "Missing website, username, or password"}), 400
            
            print(f"[VAULT] Saving password for {website} / {username}")
            encrypted_pw, iv = encrypt_vault_data(password)
            print(f"[VAULT] Encryption successful, inserting into database")
            
            cursor.execute("INSERT INTO vault (user_id, website, username, encrypted_password, iv) VALUES (?, ?, ?, ?, ?)",
                           (user_id, website, username, encrypted_pw, iv))
            conn.commit()
            conn.close()
            print(f"[VAULT] Password saved successfully")
            return jsonify({"status": "Success", "message": "Password encrypted (AES-256) and saved"})
        except Exception as e:
            print(f"[ERROR] Vault POST failed: {e}")
            if conn:
                conn.close()
            return jsonify({"status": "Error", "message": f"Failed to save password: {str(e)}"}), 500
        
    elif request.method == 'GET':
        try:
            cursor.execute("SELECT id, website, username, encrypted_password, iv FROM vault WHERE user_id = ?", (user_id,))
            rows = cursor.fetchall()
            passwords = []
            for row in rows:
                try:
                    decrypted = decrypt_vault_data(row['encrypted_password'], row['iv'])
                except Exception as e:
                    print(f"[WARN] Failed to decrypt vault entry {row['id']}: {e}")
                    decrypted = "Error decrypting"
                passwords.append({
                    "id": row['id'],
                    "website": row['website'],
                    "username": row['username'],
                    "password": decrypted
                })
            conn.close()
            return jsonify({"vault": passwords})
        except Exception as e:
            print(f"[ERROR] Vault GET failed: {e}")
            if conn:
                conn.close()
            return jsonify({"status": "Error", "message": f"Failed to fetch vault: {str(e)}"}), 500

# 🚀 RUN
if __name__ == '__main__':
    app.run(debug=True)
