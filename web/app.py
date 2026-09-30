import sys, os
import joblib
from flask import Flask, request, jsonify, render_template

# Proje root erişimi
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from encryption.cipher import encrypt, decrypt
from db.mongo import save_message, get_chat

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 

# =========================
# 🤖 MODEL LOAD (GÜNCEL MODEL)
# =========================
# Dosya adını senin belirttiğin guncel_model.pkl olarak değiştirdik
model_path = os.path.join("nlp", "guncel_model.pkl") 
try:
    model = joblib.load(model_path)
    print(f"✔ Yeni model ({model_path}) başarıyla yüklendi.")
except Exception as e:
    print(f"❌ Model yükleme hatası: {e}")
    model = None

# =========================
# 🏠 ANA SAYFA
# =========================
@app.route('/')
def index():
    return render_template('index.html')

# =========================
# 💬 MESAJ GÖNDER (POST)
# =========================
@app.route('/send', methods=['POST'])
def api_send_message():
    data = request.json
    sender = data.get("sender", "gonderici").lower().strip()
    receiver = data.get("receiver", "").lower().strip()
    text = data.get("text", "").strip()

    if not receiver or not text:
        return jsonify({"error": "Alıcı veya mesaj alanı boş olamaz!"}), 400

    # 🤖 Sentiment Analizi
    sentiment = "notr" 
    
    if model:
        try:
            # Modelin tahminini alıyoruz
            prediction = str(model.predict([text])[0]).lower()
            
            # BURASI KRİTİK: 'sürpriz'i sildik, yerine 'notr' ekledik!
            # Eğer bu listede 'notr' olmazsa, kod her tahmini geçersiz sayar.
            valid_sentiments = ["mutlu", "üzgün", "kızgın", "korku", "notr"]
            
            if prediction in valid_sentiments:
                sentiment = prediction
            else:
                sentiment = "notr"
        except:
            sentiment = "notr"

    # 🔐 Encrypt
    try:
        cipher, params = encrypt(text, sentiment)
    except Exception as e:
        return jsonify({"error": f"Şifreleme işlemi başarısız: {str(e)}"}), 500

    # 🧾 MongoDB Payload
    payload = {
        "sender": sender,
        "receiver": receiver,
        "text": text, 
        "sentiment": sentiment,
        "cipher": cipher,
        "params": params
    }

    try:
        save_message(payload)
        return jsonify({
            "status": "success",
            "sentiment": sentiment,
            "cipher": cipher
        })
    except Exception as e:
        return jsonify({"error": f"Veritabanı kayıt hatası: {str(e)}"}), 500

# =========================
# 🔓 MESAJ OKU (GET)
# =========================
@app.route('/read/<username>', methods=['GET'])
def api_read_messages(username):
    user = username.lower().strip()
    
    try:
        messages = get_chat(user)
        
        if not messages:
            return jsonify([])

        last_msg = messages[-1]
        
        try:
            decrypted_text = decrypt(
                last_msg["cipher"],
                last_msg.get("sentiment", "notr"),
                last_msg.get("params", {})
            )
        except Exception as e:
            decrypted_text = f"[Şifre Çözme Hatası: {str(e)}]"

        result = [{
            "from": last_msg.get("sender"),
            "to": last_msg.get("receiver"),
            "cipher": last_msg.get("cipher"),
            "message": decrypted_text,
            "sentiment": last_msg.get("sentiment")
        }]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Mesajlar getirilirken hata oluştu: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)