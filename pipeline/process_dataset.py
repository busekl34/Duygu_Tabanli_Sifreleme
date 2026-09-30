import pandas as pd
from tqdm import tqdm

from nlp.svm_model import SentimentModel
from encryption.cipher import encrypt
from db.mongo import save_message


# =========================
# 📂 MODEL YÜKLE
# =========================
import joblib

model = joblib.load("nlp/svm_model.pkl")


# =========================
# 🔄 DATASET İŞLE
# =========================
def process_dataset(path):

    print("🚀 Dataset işleniyor...")

    df = pd.read_excel(path)

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    count = 0

    for _, row in tqdm(df.iterrows(), total=len(df)):

        text = str(row["Tweet"])
        label = row["Etiket"]

        # 1️⃣ sentiment tahmini (istersen modelden de alabiliriz)
        sentiment = model.predict(text)[0]

        # 2️⃣ encryption
        cipher, params = encrypt(text, sentiment)

        # 3️⃣ MongoDB kayıt
        data = {
            "text": text,
            "label": label,
            "sentiment": sentiment,
            "cipher": cipher,
            "params": params
        }

        save_message(data)
        count += 1

    print(f"✅ MongoDB'ye yazıldı: {count}")


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    process_dataset("data/TurkishTweets.xlsx")