# Bilgisayarda yapılacaklar (sırayla)

Her madde bağımsız; hangisini yaparsan yap. Hazır olan her şey bu repoda.

## 1. Alkollü mekan ve yemek dışı yer ayıklamasını programa ekle (kolay, ~5 dk)
1. Bu depodaki `pc_yama_alkol.py` dosyasını indir.
2. Terminalde: `python pc_yama_alkol.py <local_radar_core.py'nin yolu>`
   (yedeğini `.bak` olarak alır, iki kez çalıştırsan zarar vermez; "Yama uygulandı" yazmalı).
3. Programdan rehberleri yeniden üret (yemek dışı ayıklama menüsü / rehber üretimi), çıkan HTML'leri bu depoya yükle.
4. Kontrol: bir rehberde "meyhane", "pub" adlı yer kalmadığına bak. "Sıra gecesi" mekanları kalmalı.

## 2. Yol Üstü Lezzet Molası (orta, ~20 dk)
Adımlar `YOL_USTU_PC.md` dosyasında. Betik hazır (`yol_uret.py`), tek eksik gerçek yol verisi (internet gerekir).

## 3. Yeni rehber eklediysen
`python3 indeks_uret.py rehberler rehber_indeks.json` komutuyla indeksi yenile, `rehber_indeks.json` dosyasını yükle.
Ardından sayfaları yenilemek için sırayla: `ulusal_uret.py`, `gizli_uret.py`, `ustalar_uret.py`, `dna_uret.py`, `ilce_uret.py` (hepsi repo kökünde çalışır; her birinin başındaki `local_radar_core.py` yolunu kendi bilgisayarına göre düzelt: `ulusal_uret.py` ve `yol_uret.py` içinde).

## 4. Küçük işler (isteğe bağlı)
- `rehberler_yedek_kasim/` klasörünü birkaç gün sonra sil.
- `rehberler/harita.html` varsa sil (ana sayfadaki harita.html kullanılıyor).
- `bolge.html` sayfasına tema düğmesi, "Bana yakın sırala" düğmesi.
