# 🌐 Local Radar · Canlı Rehberler

Türkiye'nin **550'den fazla ilçesi** için hazırlanmış, Google Haritalar verisine dayalı yemek rehberleri.

Bu depo, [Local Radar](https://github.com/cisey/local-radar) projesinin **canlı çıktılarını** barındırır. Local Radar, Google Haritalar'da yüksek puanlı yerleri tarayan, puan ve yorum sayısına göre eleyen ve her ilçe için etkileşimli HTML rehberler üreten Python tabanlı bir araçtır. Üretilen rehberler buraya yüklenir ve **GitHub Pages** ile yayınlanır.

👉 **Canlı rehberler:** [https://cisey.github.io/LocalRadar/](https://cisey.github.io/LocalRadar/)

## ✨ Özellikler

- 📱 **Telefon öncelikli tasarım:** Telefon ekranına göre hazırlanmış sade ve hızlı arayüz
- 🌙 **Koyu tema:** Okunaklı yazılar, yumuşak geçişler ve kart tasarımı
- 🔍 **Anlık arama:** İl, ilçe veya dosya adına göre rehber bulma; rehberin içinde mekan, yemek türü ve adres araması
- 🗂️ **Akıllı gruplama:** Rehberler illere göre otomatik gruplanır, iller kapalı başlar
- 📚 **Tüm İlçeler rehberi:** 75 ilin ilçeleri tek bir rehberde birleşir, aynı mekan bir kez görünür
- ⭐ **En iyi 10 / 20:** Her rehberin en üstünde o bölgenin en iyi yerleri: ilçe rehberlerinde 10, il rehberlerinde 20 (aşağıda nasıl seçildiği yazıyor)
- 👀 **Tümü görünümü:** Her kategoriden en iyi 7 yer, altında "tamamını gör" düğmesi. Büyük şehirlerde sayfa hızlı açılır, uzun listeler "Daha fazla göster" ile yüklenir
- 🔗 **Paylaşılabilir görünüm:** Arama ve filtre seçimini tek linkle arkadaşına gönderme
- 📍 **Mesafe rozeti:** "Bana yakın" sıralamasında her mekanın yanında uzaklık
- 🗺️ **Haritadan seçim:** Türkiye haritasında ile ya da ilçeye dokunarak rehbere ulaşma
- 📍 **Konumumu bul:** Bulunduğun ilçeyi bulur, yakınındaki iyi yerleri uzaklığa göre sıralar
- 🍽️ **Tür filtresi:** Yakındaki yerleri kebap, kahvaltı, tatlı, kafe gibi türlere göre süzme
- 🏷️ **Yemek türüne göre bölümler:** Döner & Kebap, Pide & Lahmacun, Çiğ Köfte, Fast food, Türk & Aile Restoranı, Balık & Deniz Ürünleri, Kafe & Kahve, Kahvaltı, Fırın & Tatlı, Kasap
- ⚡ **Otomatik dizin:** Yeni bir rehber yüklendiğinde bir GitHub Action (`update-guides.yml`) `rehberler.json` dosyasını otomatik günceller

## ⭐ Sıralama nasıl yapılıyor?

Rehberler sadece puana ya da sadece yorum sayısına göre dizilmez. Az sayıda oyla alınmış 5,0 puanlar sıralamayı yanıltmasın diye, her yerin puanı **yorum sayısıyla birlikte** değerlendirilir:

- Çok yorumu olan yerin puanına olduğu gibi güvenilir.
- Az yorumlu yerin puanı ortalamaya (4,0) doğru çekilir.
- Ölçek, rehberin büyüklüğüne göre ayarlanır: İstanbul veya Gaziantep gibi büyük şehirlerde daha yüksek, küçük ilçelerde daha düşük.

**En iyi 10 / 20 kutusu:**
1. Google puanı **4,3 ve üzeri** olan yerler alınır.
2. Bu yerler yukarıdaki güven skoruna göre sıralanır.
3. Çeşitlilik için aynı türden en fazla 3 yer (il rehberlerinde 4) girer.
4. İlçe rehberlerinde ilk 10, il rehberlerinde ilk 20 yer gösterilir.

Aynı mekan farklı taramalarda iki kez bulunmuşsa Google'ın mekan kimliğine göre tek kayda indirilir.

Hesabın ayrıntıları, örnekler ve küçük bir hesap makinesi için: [Puanlama nasıl çalışıyor?](https://cisey.github.io/LocalRadar/puanlama.html)

## 📁 Nasıl Çalışır?

1. **Tarama:** Python programı bir ilçe için Google Haritalar'da yemek yerlerini tarar.
2. **Üretim:** Sonuçlar bir `.html` rehbere dönüştürülür. İlin tüm ilçelerini içeren "Tüm İlçeler" rehberi de güncellenir.
3. **Yükleme:** Rehberler bu depodaki `rehberler/` klasörüne yüklenir.
4. **Otomasyon:** GitHub Actions yeni dosyayı algılar ve `rehberler.json` dosyasını günceller.
5. **Yayın:** GitHub Pages yeni rehberi sunar. Ana sayfa (`index.html`) ve harita sayfaları (`harita.html`, `bolge.html`) rehberi hemen listeler.

Tarama, geceleri gözetimsiz çalışan bir sırayla yapılır: ilçe listesi verilir, program her ilçeyi sırayla tarayıp yükler. Daha önce taranmış alanlar tekrar açılmaz.

## 🛠️ Mimari

- **Arayüz:** Saf HTML, CSS ve JavaScript (kütüphane yok, hızlı açılır)
- **Veri kaynağı:** `rehberler.json` (yedek olarak GitHub API)
- **Otomasyon:** Dizin güncellemesi için GitHub Actions
- **Yayın:** GitHub Pages
- **Harita:** İl ve ilçe sınırları SVG olarak sayfanın içine gömülüdür, dış harita servisi gerekmez
- **Rehber sayfaları:** Her rehber tek bir bağımsız HTML dosyasıdır; veri sayfanın içine gömülüdür

## 🤝 İlgili Projeler

- [cisey/local-radar](https://github.com/cisey/local-radar): Çekirdek Python tarayıcı, arayüz ve rehber üretici

## ⚠️ Uyarı

Bu rehberlerde gösterilen veriler, herkese açık Google Haritalar verilerinden toplanmıştır. Puanlar ve yorum sayıları tarama tarihindeki değerlerdir, mekanlar zamanla kapanabilir ya da değişebilir. Kişisel ve eğitim amaçlı kullanım içindir. Google ile bir bağlantısı yoktur.

Gezginler ve yemek sevenler için ❤️ ile yapıldı.
