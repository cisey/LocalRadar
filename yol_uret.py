"""Yol Üstü Lezzet Molası -> yol.html  (BİLGİSAYARDA çalıştır; internet gerekir)
Kullanım (repo kökünden):
  python yol_uret.py          -> gerçek sürüş rotalarını OSRM'den çeker, yol.html üretir
  python yol_uret.py --test   -> internetsiz deneme (düz çizgi Ankara-Konya), yol_test.html üretir
Yol verisi yol_cache/ klasörüne kaydedilir; ikinci çalıştırmada internet kullanmaz.
"""
import collections
import glob
import json
import math
import os
import re
import sys
import time
import urllib.request

CORE_YOLU = "C:/Users/Kahveci/projeler/local-radar"  # local-radar klasörünün yolu
MAX_SAPMA = 3.0       # anayoldan en fazla kuş uçuşu sapma (km)
DILIM_KM = 40         # her kaç km'de bir mola seçilsin
DILIM_ADET = 3        # her dilimde en fazla kaç mekan
KENAR_BOSLUK = 15.0   # başlangıç ve bitişteki şehir merkezini atla (km)
MIN_P = 4.3
MIN_Y = 100

# (hat adı, [(enlem, boylam), ...] -> başlangıç, isteğe bağlı ara noktalar, bitiş)
HATLAR = [
    # --- Marmara & Karadeniz ---
    ("İstanbul → Ankara", [(41.008, 28.978), (40.735, 31.606), (39.933, 32.859)]),
    ("İstanbul → İzmir", [(41.008, 28.978), (40.183, 29.067), (38.423, 27.142)]),
    ("İstanbul → Antalya (Bursa · Afyon)", [(41.008, 28.978), (40.183, 29.067), (38.756, 30.538), (37.720, 30.290), (36.884, 30.705)]),
    ("İstanbul → Trabzon (Karadeniz)", [(41.008, 28.978), (40.735, 31.606), (40.873, 35.462), (41.286, 36.330), (40.986, 37.879), (41.002, 39.717)]),
    ("İstanbul → Gaziantep (Ankara · Adana)", [(41.008, 28.978), (40.735, 31.606), (39.933, 32.859), (38.368, 34.036), (37.000, 35.321), (37.066, 37.383)]),
    ("İstanbul → Çanakkale → İzmir", [(41.008, 28.978), (40.978, 27.515), (40.155, 26.414), (39.319, 26.693), (38.423, 27.142)]),
    ("İstanbul → Edirne (Trakya)", [(41.008, 28.978), (41.159, 27.800), (41.406, 27.359), (41.677, 26.555)]),

    # --- İç Anadolu Çıkışlı ---
    ("Ankara → İzmir (Afyon · Uşak)", [(39.933, 32.859), (38.756, 30.538), (38.674, 29.406), (38.423, 27.142)]),
    ("Ankara → Antalya (Afyon · Isparta)", [(39.933, 32.859), (38.756, 30.538), (37.764, 30.556), (36.884, 30.705)]),
    ("Ankara → Konya", [(39.933, 32.859), (38.650, 33.070), (37.871, 32.484)]),
    ("Ankara → Samsun", [(39.933, 32.859), (40.550, 34.955), (41.286, 36.330)]),
    ("Ankara → Erzurum (Sivas · Erzincan)", [(39.933, 32.859), (39.820, 34.804), (39.748, 37.017), (39.750, 39.491), (39.904, 41.267)]),

    # --- Ege & Akdeniz ---
    ("İzmir → Antalya (Denizli üzerinden)", [(38.423, 27.142), (37.844, 27.845), (37.776, 29.086), (37.720, 30.290), (36.884, 30.705)]),
    ("İzmir → Fethiye (Aydın · Muğla)", [(38.423, 27.142), (37.844, 27.845), (37.215, 28.363), (36.659, 29.126)]),
    ("Antalya → Mersin (sahil yolu)", [(36.884, 30.705), (36.544, 32.000), (36.075, 32.836), (36.378, 33.934), (36.800, 34.641)]),

    # --- Güneydoğu & Doğu ---
    ("Mersin → Gaziantep", [(36.800, 34.641), (37.000, 35.321), (37.066, 37.383)]),
    ("Gaziantep → İzmir (Konya · Çivril · Uşak)", [(37.066, 37.383), (37.000, 35.321), (37.871, 32.484), (38.065, 30.165), (38.301, 29.738), (38.674, 29.406), (38.423, 27.142)]),
    ("Gaziantep → Trabzon (Malatya · Erzincan)", [(37.066, 37.383), (38.355, 38.309), (39.750, 39.491), (40.460, 39.481), (41.002, 39.717)]),
    ("Gaziantep → Diyarbakır", [(37.066, 37.383), (37.167, 38.795), (37.914, 40.230)]),
    ("Diyarbakır → Van (Bitlis · Tatvan)", [(37.914, 40.230), (37.887, 41.132), (38.400, 42.108), (38.501, 43.373)]),
]


def km_xy(lat, lon):
    return (lon * math.cos(math.radians(39)) * 111.32, lat * 110.57)


def mesafe(a, b):
    x1, y1 = km_xy(*a)
    x2, y2 = km_xy(*b)
    return math.hypot(x1 - x2, y1 - y2)


def osrm_rota(ad, noktalar):
    os.makedirs("yol_cache", exist_ok=True)
    cache_yolu = os.path.join("yol_cache", "osrm_" + re.sub(r"\W+", "_", ad) + ".json")
    if os.path.exists(cache_yolu):
        return json.load(open(cache_yolu, encoding="utf-8"))

    # OSRM koordinatları boylam,enlem sırasıyla ister
    koord = ";".join(f"{lon:.5f},{lat:.5f}" for lat, lon in noktalar)
    url = f"https://router.project-osrm.org/route/v1/driving/{koord}?overview=full&geometries=geojson"

    son_hata = None
    for deneme in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LocalRadar-yol/2.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode("utf-8"))
            if d.get("code") == "Ok" and d.get("routes"):
                rota = d["routes"][0]
                cizgi = [[lat, lon] for lon, lat in rota["geometry"]["coordinates"]]
                veri = {"cizgi": cizgi, "km": round(rota["distance"] / 1000.0, 1)}
                json.dump(veri, open(cache_yolu, "w", encoding="utf-8"))
                time.sleep(1.2)
                return veri
            son_hata = d.get("code", "boş yanıt")
        except Exception as e:
            son_hata = e
            print(f"  OSRM deneme {deneme + 1}/3 hatası: {e}")
            time.sleep(2)

    raise SystemExit(f"OSRM yanıt vermedi ({ad}): {son_hata}")


def yerleri_oku():
    sys.path.insert(0, CORE_YOLU)
    import local_radar_core as C

    src = open("ulusal_uret.py", encoding="utf-8").read()
    g = {}
    exec(src[: src.index("rows=[]")], g)
    kara, temiz, marka, DUZ, HARIC = g["kara"], g["temiz"], g["marka"], g["DUZ"], g["HARIC"]

    yer = []
    for f in sorted(glob.glob(os.path.join("rehberler", "*-Tum-Ilceler.html"))):
        il = os.path.basename(f).replace("-Tum-Ilceler.html", "")
        h = open(f, encoding="utf-8").read()
        v = json.JSONDecoder().raw_decode(h[h.find("const V=") + 8 :])[0]
        m = re.search(r"<title>([^<·–-]+)", h)
        a = m.group(1).strip() if m else il
        a = DUZ.get(a, DUZ.get(il, a))
        for x in v["I"]:
            if x.get("u") or x.get("S") not in C.POPULER_KATEGORILER or not x.get("l") or not x.get("e"):
                continue
            n0 = C._PUA.sub("", x["n"]).strip()
            t = C._PUA.sub("", x.get("t") or "")
            if C._zincir_mi(n0) or kara(n0, t) or HARIC.search(C.fold(n0)):
                continue
            try:
                p = float(str(x["p"]).replace(",", "."))
            except ValueError:
                continue
            y = x.get("y") or 0
            if MIN_P <= p <= 5 and y >= MIN_Y:
                yer.append(dict(
                    ad=temiz(n0), il=a, ilce=x.get("c") or "Merkez", kat=x["S"],
                    puan=p, yorum=y, link=x["l"], pt=(x["e"], x["b"]), k=marka(n0)
                ))

    Cm = sum(r["puan"] for r in yer) / len(yer)
    for r in yer:
        r["G"] = (r["yorum"] * r["puan"] + 250 * Cm) / (r["yorum"] + 250)
    return yer


def hat_isle(ad, cizgi, yer, osrm_km=None):
    if len(cizgi) < 2:
        print("  UYARI: rota boş ->", ad)
        return None

    # Çizgiyi ~400 metrelik noktalara sıklaştır ve baştan itibaren km hesapla
    pts = [tuple(cizgi[0])]
    kms = [0.0]
    toplam = 0.0
    for a, b in zip(cizgi, cizgi[1:]):
        L = mesafe(a, b)
        if L <= 0:
            continue
        n = max(1, int(L / 0.4))
        for i in range(1, n + 1):
            p = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
            toplam += L / n
            pts.append(p)
            kms.append(toplam)

    # OSRM gerçek mesafesi varsa ölçeği ona eşitle
    gercek_km = osrm_km if osrm_km else toplam
    olcek = (gercek_km / toplam) if toplam > 0 else 1.0
    kms = [k * olcek for k in kms]

    lo = min(p[0] for p in pts) - 0.05
    hi = max(p[0] for p in pts) + 0.05
    lw = min(p[1] for p in pts) - 0.05
    hw = max(p[1] for p in pts) + 0.05

    cell = collections.defaultdict(list)
    for idx, p in enumerate(pts):
        cell[(int(p[0] * 20), int(p[1] * 20))].append(idx)

    kenar = KENAR_BOSLUK if gercek_km > KENAR_BOSLUK * 3 else 0.0
    sonuc = []
    for r in yer:
        a, b = r["pt"]
        if not (lo <= a <= hi and lw <= b <= hw):
            continue
        cand = [
            idx
            for i in (-1, 0, 1)
            for j in (-1, 0, 1)
            for idx in cell.get((int(a * 20) + i, int(b * 20) + j), [])
        ]
        if not cand:
            continue
        en_idx = min(cand, key=lambda idx: (pts[idx][0] - a) ** 2 + (pts[idx][1] - b) ** 2)
        sap = mesafe(pts[en_idx], r["pt"])
        km_deger = kms[en_idx]
        if sap <= MAX_SAPMA and kenar <= km_deger <= (gercek_km - kenar):
            sonuc.append(dict(r, km=km_deger, sapma=sap))

    secilen = []
    dil = collections.defaultdict(list)
    for r in sorted(sonuc, key=lambda r: -r["G"]):
        b = int(r["km"] // DILIM_KM)
        if len(dil[b]) < DILIM_ADET and all(x["k"] != r["k"] for x in dil[b]):
            dil[b].append(r)
            secilen.append(r)

    secilen.sort(key=lambda r: r["km"])
    return dict(
        ad=ad,
        km=round(gercek_km),
        liste=[
            dict(
                ad=r["ad"], il=r["il"], ilce=r["ilce"], kat=r["kat"],
                puan=r["puan"], yorum=r["yorum"], link=r["link"],
                km=round(r["km"], 1), sapma=round(r["sapma"], 1),
                e=round(r["pt"][0], 4), b=round(r["pt"][1], 4),
            )
            for r in secilen
        ],
    )


def sayfa(veri, cikti):
    S = open("ulusal_sablon.html", encoding="utf-8").read()
    S = re.sub(r'<div class="sek">.*?</div>\n', "", S, flags=re.S)
    S = S.replace("Türkiye'nin En Popüler Yerleri · Local Radar", "Yol Üstü Lezzet Molası · Local Radar")
    S = S.replace("🏆 Türkiye'nin En Popüler Yerleri", "🛣️ Yol Üstü Lezzet Molası")
    S = S.replace(
        '<div class="fl"><select id="il"></select><select id="kat"></select></div>',
        '<div class="fl"><select id="il"></select><button type="button" class="geo" id="ters">↔ Ters çevir</button></div>'
        '<div class="fl"><button type="button" class="geo" id="geo" style="flex:1;padding:10px">📍 Konumuma en yakın molaya git</button></div>',
    )
    S = S.replace(
        "</style>",
        ".geo{background:#1e293b;color:var(--text);border:1px solid var(--line);border-radius:12px;padding:0 12px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}.k.vur{outline:2px solid var(--gold)}</style>",
        1,
    )
    a = S.index('<div class="not">')
    b = S.index("</div>", a) + 6
    S = (
        S[:a]
        + '<div class="not"><b>Nasıl seçildi?</b><br>'
        + "Her güzergâhın sürüş çizgisine en fazla 3 km uzaklıktaki, puanı en az 4,3 ve yorumu en az 100 olan, "
        + "zincir olmayan yerler alınır. Başlangıç ve bitişteki 15 km'lik şehir merkezleri hariç tutulur; yol boyunca "
        + "her 40 km'lik dilimden Güvenilir Skor'u en yüksek 3 yer gösterilir. Sapma mesafeleri kuş uçuşudur: "
        + "ücretli otoyollarda bariyer nedeniyle gerçek çıkış daha uzakta olabilir; sapmadan önce Haritalar'dan giriş "
        + 've park durumuna bakın. Ayrıntılar: <a href="puanlama.html#yol">Puanlama nasıl çalışır?</a></div>'
        + S[b:]
    )
    j0 = S.index("<script>\n")
    j1 = S.index("</script>", j0)
    js = """<script>
(function(){
var H={hatlar:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
if(!H.hatlar.length)return;
var $=function(i){return document.getElementById(i)},hi=0,ters=false,N=25,ADIM=25,sel=$('il');
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
sel.innerHTML=H.hatlar.map(function(h,i){return'<option value="'+i+'">'+esc(h.ad)+'</option>'}).join('');
function liste(){var h=H.hatlar[hi],l=h.liste.slice();if(ters)l.reverse();return l}
function ciz(vur){var h=H.hatlar[hi],l=liste();$('ac').textContent=h.ad.replace(' → ',ters?' ← ':' → ')+' · yaklaşık '+h.km+' km · '+l.length+' mola';
 $('say').textContent=ters?'Dönüş yönü':'Gidiş yönü';$('sf').style.display='none';
 var lim=Math.max(N,vur!=null?vur+3:0);
 $('liste').innerHTML=l.slice(0,lim).map(function(m,i){var km=ters?Math.max(0,Math.round(h.km-m.km)):Math.round(m.km);
  return'<a class="k'+(i===vur?' vur':'')+'" href="'+esc(m.link)+'" target="_blank" rel="noopener"><div class="no">'+km+'<div style="font-size:10px;font-weight:500">km</div></div><div class="b"><div class="ad">'+esc(m.ad)+'</div><div class="alt">'+esc(m.il)+' / '+esc(m.ilce)+' · '+esc(m.kat)+'</div><div class="pu"><b>★ '+Number(m.puan).toFixed(1).replace('.',',')+'</b> · '+Number(m.yorum).toLocaleString('tr-TR')+' yorum <span class="et">Anayoldan '+String(m.sapma).replace('.',',')+' km</span></div></div><div class="ok">↗</div></a>'}).join('');
 var kalan=l.length-lim;if(kalan>0){$('df').style.display='block';$('df').textContent='Daha fazla göster ('+kalan+' kaldı)'}else $('df').style.display='none';
 if(vur!=null){var e=document.querySelector('.k.vur');if(e)e.scrollIntoView({block:'center'})}}
function km(a,b,c,d){var r=Math.PI/180,x=(d-b)*r*Math.cos((a+c)/2*r),y=(c-a)*r;return 6371*Math.sqrt(x*x+y*y)}
sel.onchange=function(){hi=+sel.value;N=ADIM;ciz()};$('ters').onclick=function(){ters=!ters;N=ADIM;ciz()};$('df').onclick=function(){N+=ADIM;ciz()};
$('geo').onclick=function(){if(!navigator.geolocation){alert('Bu cihazda konum desteklenmiyor.');return}
 navigator.geolocation.getCurrentPosition(function(p){var l=liste(),b=0,bd=1e9;l.forEach(function(m,i){var d=km(p.coords.latitude,p.coords.longitude,m.e,m.b);if(d<bd){bd=d;b=i}});
  if(bd>60)alert('En yakın mola '+Math.round(bd)+' km uzakta; bu hattan uzaktasın.');ciz(b)},function(){alert('Konum alınamadı. Tarayıcıda konum iznini kontrol et.')},{timeout:10000})};
ciz();
})();
"""
    S = S[:j0] + js + S[j1:]
    T = open("puanlama.html", encoding="utf-8").read()
    gt = T[T.find("<!-- Google tag") : T.find("<meta charset")]
    open(cikti, "w", encoding="utf-8").write(
        S.replace("__GTAG__", gt).replace("__VERI__", json.dumps(veri, ensure_ascii=False, separators=(",", ":")))
    )


if __name__ == "__main__":
    yer = yerleri_oku()
    print(len(yer), "aday mekan")
    out = []
    if "--test" in sys.argv:
        a, b = (39.93, 32.85), (37.87, 32.49)
        yol = [(a[0] + (b[0] - a[0]) * i / 60, a[1] + (b[1] - a[1]) * i / 60) for i in range(61)]
        h = hat_isle("Ankara → Konya (TEST)", yol, yer)
        if h:
            out.append(h)
        cikti = "yol_test.html"
    else:
        for ad, noktalar in HATLAR:
            print("Hat:", ad)
            veri = osrm_rota(ad, noktalar)
            h = hat_isle(ad, veri["cizgi"], yer, osrm_km=veri["km"])
            if h:
                print(f"  {h['km']} km, {len(h['liste'])} mola")
                out.append(h)
        cikti = "yol.html"

    sayfa(dict(hatlar=out), cikti)
    print("->", cikti)
    for h in out:
        print(h["ad"], h["km"], "km", [(m["ad"], m["il"], m["km"], m["sapma"]) for m in h["liste"][:5]])