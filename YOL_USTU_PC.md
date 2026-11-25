# Yol Üstü Lezzet Molası: bilgisayarda yapılacaklar

Hazır olan: `yol_uret.py` (betik, sahte yolla denendi, çalışıyor). Eksik olan tek şey gerçek yol verisi.

1. Bilgisayarda repo klasörünü aç (internet bağlı olsun).
2. `yol_uret.py` içinde en üstteki `CORE_YOLU` satırına `local_radar_core.py` dosyasının bulunduğu klasörü yaz.
3. Terminalde (repo kökünde): `python yol_uret.py`
   - Betik OpenStreetMap'ten (Overpass) 7 hattın yolunu indirir (birkaç dakika sürebilir, `yol_cache` klasörüne kaydeder).
   - Her hat için "yol parçası: N, kavşak: N" ve "... km, ... mola" yazar.
4. Çıkan uyarılara bak:
   - "yol bulunamadı" ya da "yol parçası: 0": o hattın OSM `ref` yazımı farklı. https://overpass-turbo.eu adresinde o hattın bir yerine tıklayıp ref'ini öğren, `HATLAR` listesinde düzelt.
   - "başlangıç ile bitiş birbirine bağlanmıyor": yol parçaları kopuk; başlangıç/bitiş koordinatını yola yaklaştır ya da `ref` listesine ek yol ekle.
5. Çıkan `yol.html` dosyasını tarayıcıda aç, birkaç hattın sonuçlarına bak (sapma km, sıralama). Beğenirsen repoya yükle.
6. Sonra: ana sayfaya düğme ve `puanlama.html`'e "Yol Üstü Lezzet Molası" bölümü eklenecek (Claude'a söyle, yazar).

Dosya: `python yol_uret.py --test` internetsiz deneme yapar (`yol_test.html`).
