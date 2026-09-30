import sys
import os
import joblib

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from nlp.svm_model import SentimentModel

print("📂 Veri yükleniyor...")

model = SentimentModel()

print("🚀 Model eğitiliyor...")
model.train("data/TurkishTweets.xlsx")

# =========================
# 🔐 SADECE SKLEARN PIPELINE KAYDET
# =========================
joblib.dump(model.model, "nlp/svm_model.pkl")

print("✔ MODEL KAYDEDİLDİ")

# =========================
# 🔍 TEST
# =========================
print("\n🔍 TEST:")
print("çok sinirliyim →", model.predict("çok sinirliyim"))
print("çok mutluyum →", model.predict("çok mutluyum"))
print("korkuyorum →", model.predict("korkuyorum"))