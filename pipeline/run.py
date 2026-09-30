import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import joblib

from db.mongo import save_message
from encryption.cipher import encrypt, decrypt


# =========================
# 🤖 MODEL YÜKLE
# =========================
model_path = os.path.join("nlp", "svm_model.pkl")
model = joblib.load(model_path)


# =========================
# 🧪 TEST METNİ
# =========================
text = "Bugün her şey çok kötü gidiyor ve sinirliyim"


# =========================
# 🎯 1. DUYGU TAHMİNİ
# =========================
pred = model.predict(text)

print("MODEL RAW OUTPUT:", pred)

# güvenli normalize
if isinstance(pred, list) or isinstance(pred, tuple):
    sentiment = pred[0]
else:
    sentiment = pred

sentiment = str(sentiment).strip().lower()


# =========================
# 🔐 2. ŞİFRELEME
# =========================
cipher, params = encrypt(text, sentiment)


# =========================
# 💾 3. MONGODB KAYIT
# =========================
data = {
    "text": text,
    "sentiment": sentiment,
    "cipher": cipher,
    "params": params
}

save_message(data)


# =========================
# 🔓 4. DECRYPT TEST (DOĞRULAMA)
# =========================
decoded = decrypt(cipher, sentiment, params)


# =========================
# 📊 SONUÇ
# =========================
print("\n========================")
print("🎯 DUYGU:", sentiment)
print("🔐 CIPHER:", cipher)
print("🔓 DECRYPTED:", decoded)
print("========================\n")