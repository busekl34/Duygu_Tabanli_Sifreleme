import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.mongo import get_all
from encryption.cipher import decrypt


# =========================
# 🔍 TEST FONKSİYONU
# =========================
def test_decryption():

    data_list = get_all()

    if len(data_list) == 0:
        print("❌ MongoDB boş!")
        return

    # ilk kaydı al
    data = data_list[0]

    text = data["text"]
    sentiment = data["sentiment"]
    cipher = data["cipher"]
    params = data["params"]

    # decrypt
    decrypted = decrypt(cipher, sentiment, params)

    # sonuç
    print("\n========================")
    print("ORIGINAL :", text)
    print("DECRYPTED:", decrypted)
    print("SENTIMENT:", sentiment)
    print("========================\n")

    # doğrulama
    assert text == decrypted, "❌ Decryption başarısız!"
    print("✅ Decryption başarılı!")


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    test_decryption()