import sys, os
import joblib

# proje root erişimi
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from encryption.cipher import encrypt, decrypt
from db.mongo import save_message, get_chat


# =========================
# 🤖 MODEL LOAD
# =========================
model_path = os.path.join("nlp", "guncel_model.pkl")
model = joblib.load(model_path)


# =========================
# 💬 MESAJ GÖNDER
# =========================
def send_message(sender, receiver, text):

    sender = sender.lower().strip()
    receiver = receiver.lower().strip()
    text = text.strip()

    # 🤖 sentiment
    sentiment = model.predict([text])[0]
    sentiment = str(sentiment).lower()

    print("\n🤖 MODEL:", sentiment)

    # 🔐 default güvenli değerler
    cipher = None
    params = {}

    # 🔐 encrypt (SAFE)
    try:
        cipher, params = encrypt(text, sentiment)
    except Exception as e:
        print("❌ ENCRYPT ERROR:", e)
        cipher = "ENCRYPT_FAILED"
        params = {}

    # 🧾 payload
    data = {
        "sender": sender,
        "receiver": receiver,
        "text": text,
        "sentiment": sentiment,
        "cipher": cipher,
        "params": params
    }

    print("\n[DEBUG] MongoDB'ye yazılıyor...")

    try:
        save_message(data)
        print("✔ MongoDB SUCCESS")
    except Exception as e:
        print("❌ MongoDB ERROR:", e)

    print("\n🔐 CIPHER:", cipher)
    print("🔐 MESAJ KAYDEDİLDİ")


# =========================
# 🔓 MESAJ OKU
# =========================
def read_messages(user):

    user = user.lower().strip()

    messages = get_chat(user)

    print("\n========================")
    print(f"📩 {user.upper()} MESAJLARI")
    print("========================")

    if not messages:
        print("📭 Hiç mesaj yok")
        return

    for msg in messages:

        try:
            decrypted = decrypt(
                msg["cipher"],
                msg["sentiment"],
                msg.get("params", {})
            )
        except Exception as e:
            decrypted = f"[DECRYPT ERROR] {e}"

        print("\n------------------------")
        print("👤 FROM:", msg.get("sender", "unknown"))
        print("👤 TO  :", msg.get("receiver", "unknown"))
        print("💬 MSG :", decrypted)
        print("😡 SENT:", msg.get("sentiment"))


# =========================
# 💬 CHAT LOOP
# =========================
def chat():

    print("\n💬 SECURE CHAT SYSTEM")

    user = input("Adın: ").strip().lower()

    while True:

        print("\n1- Mesaj gönder")
        print("2- Mesajları oku")
        print("3- Çıkış")

        choice = input("Seçim: ").strip()

        if choice == "1":

            receiver = input("Kime: ").strip().lower()
            text = input("Mesaj: ").strip()

            send_message(user, receiver, text)

        elif choice == "2":
            read_messages(user)

        elif choice == "3":
            print("👋 Çıkış yapıldı")
            break

        else:
            print("❌ Geçersiz seçim")


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    chat()