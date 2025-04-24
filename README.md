
# 🌍 İstanbul Deprem Risk Analizi (Streamlit Uygulaması)

Bu uygulama, geçmiş yıllarda gerçekleşen depremlerin konum ve büyüklük bilgilerine dayanarak **İstanbul ilçeleri için göreli bir deprem risk analizi** sunar. Zemin tipi, deprem merkezine uzaklık ve deprem büyüklüğü gibi değişkenler üzerinden her ilçe için **bir risk skoru** hesaplanır ve bu skorlar **interaktif bir harita** üzerinde görselleştirilir.

---

## 🚀 Özellikler

- 📍 İstanbul'un 39 ilçesi için risk analizi
- 🗂️ CSV dosyası yükleyerek kendi verinizi kullanma imkânı
- 🌐 Harita üzerinde pop-up ile ilçe bazlı risk görüntüleme
- 📊 Risk skorlarına göre tablo görünümü
- 🎨 Riske göre renk skalası: Yeşil (düşük), Turuncu (orta), Kırmızı (yüksek)

---

## 📦 Kurulum

```bash
git clone https://github.com/kullaniciadi/deprem-risk-analiz-app.git
cd deprem-risk-analiz-app
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Varsayılan Veri

Projeye dahil olan `data/deprem_kaydi.csv` dosyası, örnek bir deprem verisidir. Kullanıcı herhangi bir veri yüklemediği sürece bu dosya ile analiz otomatik olarak başlatılır.

---

## 🔄 Hesaplama Yöntemi

Her ilçe için:

```
Risk Skoru = (Deprem Büyüklüğü / İlçeye Uzaklık) × Zemin Çarpanı
```

- Zemin sınıfı A → 0.8
- Zemin sınıfı B → 1.0
- Zemin sınıfı C → 1.2
- Sadece 100 km'den daha yakın depremler dikkate alınır.

---

## 🧪 Kendi Verinizi Kullanmak

`ML`, `Enlem` ve `Boylam` sütunlarını içeren `.csv` dosyanızı yükleyin. Uygulama bu veriyi analiz ederek yeni bir risk haritası oluşturacaktır.

---

## 🌐 Streamlit Cloud’da Yayınlama

1. Projeyi GitHub’a yükleyin
2. [Streamlit Cloud](https://streamlit.io/cloud)’a giriş yapın
3. “New App” → GitHub repo → `app.py` → Deploy 🎉

---

## 🧠 Katkı ve Geliştirme

Bu uygulama sadece İstanbul özelinde geliştirilmiştir. Başka şehirler için risk hesaplamaları eklemek isterseniz, `istanbul_ilceleri` sözlüğünü genişleterek uygulamayı kolayca özelleştirebilirsiniz.

---

## 📜 Lisans

Bu proje [MIT lisansı](https://opensource.org/licenses/MIT) ile lisanslanmıştır.
