
# 🔐 Duygu Analizine Yönelik Şifreleme Yapan Mesajlaşma Platformu

Bu proje, mesajların içerdiği duyguyu analiz ederek elde edilen duygu sınıfına göre farklı şifreleme yöntemleri uygulayan deneysel bir mesajlaşma platformudur.

Projenin temel amacı; doğal dil işleme ve makine öğrenmesi kullanılarak mesajların duygusal durumunun belirlenmesi ve belirlenen duyguya göre farklı şifreleme süreçlerinin uygulanmasını sağlamaktır.

---

## 📌 Proje Hakkında


Sistem, kullanıcı tarafından gönderilen mesajı öncelikle duygu analizi modelinden geçirir.

Mesaj aşağıdaki beş duygu sınıfından birine dahil edilir:

- 😡 Kızgın
- 😨 Korku
- 😊 Mutlu
- 😢 Üzgün
- 😐 Nötr

Belirlenen duygu sınıfına göre ilgili şifreleme algoritması uygulanır ve mesaj bilgileri MongoDB veritabanına kaydedilir.

---

## 🔄 Sistem Akışı

```text
Kullanıcı Mesajı
       ↓
Metin İşleme
       ↓
Duygu Analizi
       ↓
SVM - RBF Sınıflandırıcı
       ↓
Duygu Sınıfının Belirlenmesi
       ↓
Duyguya Özel Şifreleme
       ↓
Şifrelenmiş Mesaj
       ↓
MongoDB
```

## 🧠 Duygu Analizi

```
Duygu sınıflandırma işleminde Kaggle üzerinden elde edilen bir veri seti kullanılmıştır.

📊 Veri Seti
Duygu	Örnek Sayısı
Kızgın	800
Korku	800
Mutlu	800
Üzgün	800
Nötr	799
Toplam	3999

Duygu sınıflandırması için Destek Vektör Makineleri (SVM) algoritmasının RBF çekirdeği kullanılmıştır.

Model yaklaşık %96 doğruluk oranı elde etmiştir.
```

## 🔐 Duyguya Göre Şifreleme
```
Duygu analizi sonucunda belirlenen sınıfa göre farklı şifreleme algoritmaları uygulanmaktadır.

Duygu	Uygulanan İşlem
😡 Kızgın	Şifreleme Algoritması
😨 Korku	Şifreleme Algoritması
😊 Mutlu	Şifreleme Algoritması
😢 Üzgün	Şifreleme Algoritması
😐 Nötr	Şifreleme Algoritması

Bu yapı sayesinde mesajın duygu sınıfı, şifreleme sürecinin bir parçası olarak kullanılmaktadır.
```

## 🗄️ MongoDB
```
Mesajların saklanması için MongoDB kullanılmaktadır.

Projede aşağıdaki veritabanı yapısı kullanılmaktadır:

Alan	Değer
Veritabanı	secure_chat
Collection	messages

Mesaj kayıtlarında aşağıdaki bilgiler tutulabilmektedir:

{
    "sender": "kullanici1",
    "receiver": "kullanici2",
    "text": "mesaj",
    "sentiment": "happy",
    "cipher": [],
    "params": {}
}

MongoDB; mesajların kaydedilmesi, kullanıcı mesajlarının getirilmesi, sohbet geçmişinin görüntülenmesi ve mesajların yönetilmesi için kullanılmaktadır.

```

## 🛠️ Kullanılan Teknolojiler
```
Python
Makine Öğrenmesi
Doğal Dil İşleme (NLP)
Scikit-learn
SVM
RBF Kernel
MongoDB
PyMongo
```
## ⚙️ Kurulum
```
1. Projeyi Klonlama : https://github.com/busekl34/Duygu_Tabanli_Sifreleme

2.Proje Klasörüne Girme: cd Duygu_Tabanli_Sifreleme

3. Gerekli kütüphaneleri yükleme: pip install -r requirements.txt

4.Çalıştırma: python app.py


