# 🌐 Local Radar · Canlı Rehberler

Bu depo, [Local Radar](https://github.com/cisey/local-radar) projesinin **canlı çıktılarını** barındırır.

Local Radar, Google Haritalar'da yüksek puanlı yerleri tarayan, puan ve yorum sayısına göre eleyen ve her ilçe için etkileşimli HTML rehberler üreten Python tabanlı bir araçtır. Üretilen rehberler buraya yüklenir ve **GitHub Pages** ile yayınlanır.

👉 **Canlı rehberler:** [https://cisey.github.io/LocalRadar/](https://cisey.github.io/LocalRadar/)

## ✨ Özellikler

- 📱 **Telefon öncelikli tasarım:** Telefon ekranına göre hazırlanmış sade ve hızlı arayüz
- 🌙 **Koyu tema:** Okunaklı yazılar, yumuşak geçişler ve kart tasarımı
- 🔍 **Anlık arama:** İl, ilçe veya dosya adına göre rehber bulma
- 🗂️ **Akıllı gruplama:** Rehberler illere göre otomatik gruplanır, iller kapalı başlar
- 📚 **Tüm İlçeler rehberi:** Her ilin ilçeleri tek bir rehberde birleşir, aynı mekan bir kez görünür
- 🗺️ **Haritadan seçim:** Türkiye haritasında ile ya da ilçeye dokunarak rehbere ulaşma
- 📍 **Konumumu bul:** Bulunduğun ilçeyi bulur, yakınındaki iyi yerleri (4,0+ puan, 100+ yorum) uzaklığa göre sıralar
- 🍽️ **Tür filtresi:** Yakındaki yerleri kebap, kahvaltı, tatlı, kafe gibi türlere göre süzme
- ⚡ **Otomatik dizin:** Yeni bir rehber yüklendiğinde bir GitHub Action (`update-guides.yml`) `rehberler.json` dosyasını otomatik günceller

## 📁 Nasıl Çalışır?

1. **Üretim:** Python programı bir ilçe için yeni bir `.html` rehber üretir.
2. **Yükleme:** Rehber bu depodaki `rehberler/` klasörüne yüklenir.
3. **Otomasyon:** GitHub Actions yeni dosyayı algılar ve `rehberler.json` dosyasını günceller.
4. **Yayın:** GitHub Pages yeni rehberi sunar. Ana sayfa (`index.html`) ve harita sayfaları (`harita.html`, `bolge.html`) rehberi hemen listeler.

## 🛠️ Mimari

- **Arayüz:** Saf HTML, CSS ve JavaScript (kütüphane yok, hızlı açılır)
- **Veri kaynağı:** `rehberler.json` (yedek olarak GitHub API)
- **Otomasyon:** Dizin güncellemesi için GitHub Actions
- **Yayın:** GitHub Pages
- **Harita:** İl ve ilçe sınırları SVG olarak sayfanın içine gömülüdür, dış harita servisi gerekmez

## 🤝 İlgili Projeler

- [cisey/local-radar](https://github.com/cisey/local-radar): Çekirdek Python tarayıcı, arayüz ve rehber üretici

## ⚠️ Uyarı

Bu rehberlerde gösterilen veriler, herkese açık Google Haritalar verilerinden toplanmıştır. Kişisel ve eğitim amaçlı kullanım içindir. Google ile bir bağlantısı yoktur.

Gezginler ve yemek sevenler için ❤️ ile yapıldı.
