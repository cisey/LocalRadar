# Local Radar Çıktıları

Local Radar programının ürettiği rehber sayfalarını (HTML) yayınlar. Telefondan (iPhone dahil) link ile açılır.

## Adresler

| Ne | Adres |
|---|---|
| Ana sayfa (projeler) | https://cisey.github.io/ |
| Rehber listesi | https://cisey.github.io/LocalRadar/ |

## Hangi dosya nerede

**Depo `cisey.github.io`** (ana sayfa)
- `index.html` → projelerin listesi. Pages'i açık depoları kendisi bulur. Normalde değiştirmeye gerek yok.

**Depo `local-radar-output`** (bu depo)
- `index.html` → rehber listesi. Depodaki `.html` dosyalarını kendisi bulur. Normalde değiştirmeye gerek yok.
- `Akkent-Karatas.html`, `Nizip.html`, ... → programın ürettiği rehberler.
- `README.md` → bu not.
- Ayar: Settings → Pages → Branch: `main` / `(root)`. Depo **Public** olmalı.

## Yeni mahalle / rehber ekleme

1. Programda mahalleyi tara, **🪶 İlçe (Sade)** ile sade HTML'yi oluştur (`..._guide_sade.html`).
2. Dosyaya kısa bir ad ver, boşluk koyma. Örnek: `Nizip.html`, `Akkent-Karatas.html`.
3. github.com/cisey/local-radar-output → **Add file → Upload files** → dosyayı sürükle → **Commit changes**.
4. 1-2 dakika sonra rehber listesinde kendiliğinden görünür. `index.html`'e dokunma.

Birkaç mahalleyi tek rehberde birleştirmek için: hepsini programda tara, sonra **🪶 HEPSİ (Sade)** düğmesine bas. Çıkan `local_radar_all_sade.html` dosyasını istediğin adla yükle.

## Yeni proje (başka depo) ekleme

1. Depoyu oluştur, **Public** yap, kökünde bir `index.html` olsun.
2. Settings → Pages → Branch: `main` / `(root)` → Save.
3. Ana sayfada kendiliğinden görünür (fork'lar ve `cisey.github.io` hariç).

## Sorun olursa

- **Sayfa 404 veriyor:** Pages açık mı, depo Public mi, dosya adı (büyük/küçük harf) doğru mu kontrol et. Yeni yüklemede 1-2 dakika bekle.
- **Listede görünmüyor:** Dosya uzantısı `.html` olmalı. GitHub'ın sorgu sınırı (saatte 60) dolduysa listede sadece yedek iki dosya görünür, bir saat sonra düzelir.
- **iPhone'da dosya açılmıyor:** Dosyayı değil linki gönder. .html dosyası WhatsApp/Mail'de web sayfası gibi açılmaz.
- **Harita stili bozuk:** `local_radar_core.py` güncel sürümde olmalı (harita stili sayfanın içine gömülür). Eski dosyalar yeniden oluşturulana kadar eski haliyle kalır.
