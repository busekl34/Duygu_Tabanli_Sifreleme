import hashlib

# =========================
# 🔑 ANAHTAR ÜRETİMİ
# =========================
def generate_base_key(sentiment):
    # Anahtarı sadece duygu üzerinden (veya sabit bir tuzla) üretiyoruz.
    # Text parametresini çıkardık çünkü deşifre anında text elimizde olmayacak.
    raw = (sentiment + "ozel_guvenlik_tuzu").encode("utf-8")
    digest = hashlib.sha256(raw).digest()
    return list(digest)

# =========================
# 🔴 KIZGIN (GÜÇLÜ KAYDIRMA)
# =========================
def encrypt_angry(text, key):
    cipher = []
    for i, c in enumerate(text):
        val = ord(c) + key[i % len(key)] + (i * 2)
        cipher.append(val)
    return cipher

def decrypt_angry(cipher, key):
    res = ""
    for i, v in enumerate(cipher):
        val = v - key[i % len(key)] - (i * 2)
        res += chr(val)
    return res

# =========================
# 😢 ÜZGÜN (HAFİF KAYDIRMA)
# =========================
def encrypt_sad(text, key):
    return [ord(c) - (key[i % len(key)] % 10) for i, c in enumerate(text)]

def decrypt_sad(cipher, key):
    res = ""
    for i, v in enumerate(cipher):
        res += chr(v + (key[i % len(key)] % 10))
    return res

# =========================
# 😊 MUTLU (FIBONACCI KAYDIRMA)
# =========================
def encrypt_happy(text, key):
    a, b = 1, 1
    cipher = []
    for i, c in enumerate(text):
        val = ord(c) + a + (key[i % len(key)] % 5)
        cipher.append(val)
        a, b = b, a + b #FİBONACCİ SAYI DİZİSİ
    return cipher

def decrypt_happy(cipher, key):
    a, b = 1, 1
    res = ""
    for i, v in enumerate(cipher):
        val = v - a - (key[i % len(key)] % 5)
        res += chr(val)
        a, b = b, a + b
    return res

# =========================
# 😱 KORKU (XOR + CHAOS MAP)
# =========================
def encrypt_fear(text, key):
    x = sum(key) / (len(key) * 255) #1. adım : Başlangıç sayısı oluşturulur. Anahtardaki sayılar toplanır ve 0-1 arasnda sayı elde edilir
    r = 3.99  #logistic map
    cipher = []
    initial_x = x 
    for c in text:
        x = r * x * (1 - x) #2.adım: Kaos sistemi başlıyor.Bu formül her seferinde x'i değiştirir.
        k = int(x * 100) # 3.adım: x değeri 0-100 arasında sayıya çevrilir. Her karakter için yeni bir sayı oluşturulur.
        cipher.append(ord(c) ^ k) # 4.adım : xor ile şifreleme
    return cipher, initial_x

def decrypt_fear(cipher, key, x0):
    x = x0
    r = 3.99
    res = ""
    for v in cipher:
        x = r * x * (1 - x)
        k = int(x * 100)
        res += chr(v ^ k)
    return res

# =========================
# ⚪ NÖTR (STANDART KAYDIRMA)
# =========================
def encrypt_neutral(text, key):
    # Duygu dışı mesajlar için stabil kaydırma
    return [ord(c) + (key[0] % 15) for i, c in enumerate(text)]

def decrypt_neutral(cipher, key):
    res = ""
    for v in cipher:
        res += chr(v - (key[0] % 15))
    return res

# =========================
# 🔐 ANA ENCRYPT (ŞİFRELEME)
# =========================
def encrypt(text, sentiment):
    # Anahtar üretiminde artık text kullanmıyoruz
    key = generate_base_key(sentiment)
    
    if sentiment == "kızgın":
        return encrypt_angry(text, key), {"key": key}
    elif sentiment == "üzgün":
        return encrypt_sad(text, key), {"key": key}
    elif sentiment == "mutlu":
        return encrypt_happy(text, key), {"key": key}
    elif sentiment == "korku":
        cipher, x0 = encrypt_fear(text, key)
        return cipher, {"key": key, "x0": x0}
    else:
        # "notr" veya beklenmeyen bir durum gelirse burası çalışır
        return encrypt_neutral(text, key), {"key": key}

# =========================
# 🔓 ANA DECRYPT (DEŞİFRE)
# =========================
def decrypt(cipher, sentiment, params):
    try:
        key = params["key"]
        if sentiment == "kızgın":
            return decrypt_angry(cipher, key)
        elif sentiment == "üzgün":
            return decrypt_sad(cipher, key)
        elif sentiment == "mutlu":
            return decrypt_happy(cipher, key)
        elif sentiment == "korku":
            return decrypt_fear(cipher, key, params["x0"])
        else:
            return decrypt_neutral(cipher, key)
    except Exception as e:
        return f"[Deşifre Hatası: {str(e)}]"