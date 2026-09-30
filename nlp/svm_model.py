import pandas as pd
import re
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score


# =========================
# 🧹 CLEAN TEXT
# =========================
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^\w\sçğıöşü]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# 📂 LOAD DATA
# =========================
df = pd.read_excel("guncel_veri_seti.xlsx", engine="openpyxl")

print("📌 Kolonlar:", df.columns)

df = df[["Tweet", "Etiket"]].dropna()
df["Tweet"] = df["Tweet"].apply(clean_text)

X = df["Tweet"]
y = df["Etiket"].astype(str)

# =========================
# ✂️ SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# 🤖 MODEL
# =========================
model = Pipeline([
    ("tfidf", TfidfVectorizer(
        max_features=20000,
        ngram_range=(1,2)
    )),
    ("svm", LinearSVC(C=3.0))
])

# =========================
# 🚀 TRAIN
# =========================
model.fit(X_train, y_train)

# =========================
# 🎯 PREDICT
# =========================
y_pred = model.predict(X_test)

print("\n📊 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📄 Classification Report:\n")
print(classification_report(y_test, y_pred))


# =========================
# 💾 MODEL KAYDET
# =========================
joblib.dump(model, "guncel_model.pkl")
print("\n✅ Model kaydedildi: guncel_model.pkl")


# =========================
# 🔍 TEST (opsiyonel)
# =========================
def predict(text):
    text = clean_text(text)
    return model.predict([text])[0]


print("\n🧪 Test:", predict("bugün çok mutluyum"))