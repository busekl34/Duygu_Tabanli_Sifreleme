from pymongo import MongoClient

client = MongoClient("mongodb://localhost:/")

db = client["secure_chat"]
collection = db["messages"]


# =========================
# 💾 MESAJ KAYDET
# =========================
def save_message(data: dict):

    # 🔥 güvenlik: eksik alanları doldur
    safe_data = {
        "sender": data.get("sender", "").lower(),
        "receiver": data.get("receiver", "").lower(),
        "text": data.get("text", ""),
        "sentiment": data.get("sentiment", ""),
        "cipher": data.get("cipher", []),
        "params": data.get("params", {})
    }

    collection.insert_one(safe_data)


# =========================
# 📥 KULLANICI MESAJLARI
# =========================
def get_messages(user: str):
    return list(collection.find({"receiver": user.lower()}))


# =========================
# 📥 TÜM MESAJLAR
# =========================
def get_all():
    return list(collection.find())


# =========================
# 🔍 SON MESAJ
# =========================
def get_last():
    return collection.find_one(sort=[("_id", -1)])

def get_chat(user):
    return list(collection.find({
        "$or": [
            {"sender": user},
            {"receiver": user}
        ]
    }))
# =========================
# 🧹 TEMİZLE
# =========================
def clear_collection():
    collection.delete_many({})