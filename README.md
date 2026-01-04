<div align="center">

# 🎧 Mood-to-Music  
### Duygu Farkındalıklı Müzik ve Regülasyon Asistanı

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Gemini API](https://img.shields.io/badge/Google%20Gemini-API-orange?style=for-the-badge&logo=google)
![Spotify](https://img.shields.io/badge/Spotify-API-1DB954?style=for-the-badge&logo=spotify)
![WeatherAPI](https://img.shields.io/badge/WeatherAPI-Integrated-2096F3?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<br>

> **Kullanıcının duygusal dengesini bulmasına yardımcı olan,<br>
çok ajanlı (multi-agent) müzik ve mikro aktivite öneri sistemi.**

</div>

---

## 📌 İçindekiler
- [Proje Hakkında](#-proje-hakkında)
- [Sistem Mimarisi](#-sistem-mimarisi)
- [Özellikler](#-özellikler)
- [Ekran Görüntüleri](#-ekran-görüntüleri)
- [Kurulum & Çalıştırma](#-kurulum--çalıştırma)
- [Proje Yapısı](#-proje-yapısı)
- [Teknolojiler](#-teknolojiler)
- [Ekip](#-ekip)
- [Lisans](#-lisans)

---

## 📖 Proje Hakkında

**Mood-to-Music**, klasik tek etiketli duygu analizinin ötesine geçerek, kullanıcının duygusal durumunu **5 farklı boyutta** analiz eden yapay zeka tabanlı bir **Duygu Regülasyon Asistanıdır**.

Sistem; kullanıcının yazılı ifadesini, günlük bağlamını (olaylar, mesajlar), mikro geri bildirimlerini (örn. yemek durumu) ve çevresel faktörleri (hava durumu, zaman) bir araya getirerek yalnızca mevcut ruh halini değil, bu ruh halinin **dengeye göre konumunu** anlamlandırır.

Amaç, sadece kullanıcının moduna uygun müzik önermek değil; kullanıcıyı **daha dengeli (homeostatik)** bir duygu durumuna yönlendiren terapötik bir akış sunmaktır.

### Temel Hedefler

Kullanıcının duygusal durumu şu vektörler üzerinden modellenir ve **0–100** aralığında tutulur:

1. **Valence** – Pozitif / Negatif duygu yükü  
2. **Arousal** – Uyarılma / enerji seviyesi  
3. **Physical Comfort** – Fiziksel rahatlık  
4. **Environmental Calm** – Çevresel sakinlik  
5. **Emotional Intensity** – Duygu yoğunluğu  

> ℹ️ Grafik gösteriminde **50 değeri denge noktası** kabul edilir ve görselleştirme için değerler `[-1, +1]` aralığına normalize edilir.

---

## 🧠 Sistem Mimarisi

Uygulama, merkezi bir **CoordinatorAgent** tarafından yönetilen, görevleri ayrıştırılmış çok ajanlı bir mimariye sahiptir.

```mermaid
graph TD
    User[Kullanıcı Girdisi] --> Coordinator[Coordinator Agent]

    Coordinator --> Emotion[Emotion Agent]
    Coordinator --> Event[Event Agent]
    Coordinator --> Context[Context Agent]
    Coordinator --> Micro[MicroSignal Agent]

    Emotion --> Affect[Affect Vector Agent]
    Event --> Affect
    Context --> Affect
    Micro --> Affect

    Affect --> Regulation[Regulation Agent]
    Regulation --> Spotify[Spotify Agent]

    Spotify --> Output[Müzik & Mikro Aktivite Önerisi]
````

### 🤖 Kullanılan Ajanlar

| Ajan                  | Görev                                                                   |
| --------------------- | ----------------------------------------------------------------------- |
| **EmotionAgent**      | Türkçe metin üzerinden duygu analizi (BERT + Rule-based + LLM).         |
| **EventAgent**        | Günlük olayların kullanıcı üzerindeki etkisini analiz eder.             |
| **MicroSignalAgent**  | Küçük geri bildirimleri (örn. açlık/tokluk) sayısal katkıya dönüştürür. |
| **ContextAgent**      | Hava durumu ve zaman bilgisini bağlama ekler.                           |
| **AffectVectorAgent** | Verileri 5 boyutlu duygu vektörüne (0–100) dönüştürür.                  |
| **RegulationAgent**   | Mevcut durum ile hedef denge arasındaki farkı hesaplar.                 |
| **SpotifyAgent**      | Regülasyon hedefine uygun müzik ve mikro aktivite önerir.               |

---

## ✨ Özellikler

* ✅ **Çok Boyutlu Duygu Analizi**
* ✅ **Regülasyon Odaklı Yaklaşım**
* ✅ **Dengeye Göre Normalize Grafikler**
* ✅ **Bağlam Farkındalığı (hava durumu, zaman, olay)**
* ✅ **Spotify API ile Akıllı Müzik Seçimi**
* ✅ **Mikro Aktivite Önerileri**
* ✅ **Şeffaf Karar İzleri ve Debug Paneli**

---

## 📷 Ekran Görüntüleri

### Ana Arayüz

![Ana Arayüz](screenshots/main.png)

### Müzik ve Mikro Aktivite Önerisi

![Müzik Önerisi](screenshots/music.png)

### Karar İzleri ve Sistem Logları

![Debug Paneli](screenshots/debug.png)

---

## 🛠 Kurulum & Çalıştırma

### Gereksinimler

* Python 3.9+
* Spotify Developer Hesabı
* Google Gemini API Anahtarı
* WeatherAPI Anahtarı

### Kurulum

```bash
git clone https://github.com/busrayesinn/mood2music.git
cd mood2music
pip install -r requirements.txt
```

### Ortam Değişkenleri

Proje kök dizininde `.env` dosyası oluşturun:

```env
GOOGLE_API_KEY=...
SPOTIFY_CLIENT_ID=...
SPOTIFY_CLIENT_SECRET=...
WEATHER_API_KEY=...
```

### Çalıştırma

```bash
python gui.py
```

---

## 📂 Proje Yapısı

```text
mood2music/
├── agents/              # Tüm ajan sınıfları
├── screenshots/         # README için ekran görüntüleri
├── gui.py               # Uygulama giriş noktası
├── requirements.txt     # Python bağımlılıkları
├── .env                 # Ortam değişkenleri (gitignore)
└── README.md
```

---

## 🧰 Teknolojiler

* **Dil:** Python
* **NLP & AI:** HuggingFace Transformers (BERT), Google Gemini API
* **API’ler:** Spotify Web API, WeatherAPI
* **Arayüz:** CustomTkinter
* **Görselleştirme:** Matplotlib

---

## 👥 Ekip

Bu proje ekip çalışması olarak geliştirilmiştir:

- **[Melike Dal](https://github.com/melikedal)**
- **[Büşra Yesin](https://github.com/busrayesinn)**

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır.
