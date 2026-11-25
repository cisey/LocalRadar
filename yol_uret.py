"""Yol Üstü Lezzet Molası -> yol.html  (BİLGİSAYARDA çalıştır; internet gerekir)
Kullanım (repo kökünden):   python3 yol_uret.py            -> yolları OpenStreetMap'ten (Overpass) çeker, yol.html üretir
                            python3 yol_uret.py --test     -> internetsiz deneme (sahte Ankara-Konya yolu), yol_test.html üretir
Gerekli: local_radar_core.py yolu (aşağıda CORE_YOLU). Yol verisi yol_cache/ klasörüne kaydedilir, tekrar indirmez.
Mantık: yol çizgisi -> çizge, başlangıçtan her noktaya km (Dijkstra) -> mekanı yola en yakın noktaya bağla -> sapma <= 3 km
        -> her 40 km dilimde en iyi 3 mekan. Otoyollarda sadece kavşak (motorway_junction) noktalarına yakın mekanlar."""
import re,json,glob,math,heapq,collections,sys,os,time,urllib.request,urllib.parse
CORE_YOLU='/home/claude/cisey/local-radar'        # <- bilgisayarında local-radar klasörünün yolunu yaz
MAX_SAPMA,DILIM_KM,DILIM_ADET,MIN_P,MIN_Y=3.0,40,3,4.3,100
# (ad, OSM ref listesi, başlangıç (enlem,boylam), bitiş, otoyol_mu)  -- ref'ler OSM'de farklı yazılmış olabilir: betik bulunan yol sayısını yazar, 0 çıkarsa düzelt
HATLAR=[('İstanbul → Ankara',['O-4','D100'],(41.0,28.95),(39.93,32.85),False),
        ('İstanbul → İzmir',['O-5','D550','D200'],(41.0,28.95),(38.42,27.14),False),
        ('Antalya → Mersin (sahil yolu)',['D400'],(36.89,30.70),(36.80,34.64),False),
        ('Ankara → Konya',['D715','D650','O-21'],(39.93,32.85),(37.87,32.49),False),
        ('Ankara → Samsun',['D795','D010','D100'],(39.93,32.85),(41.29,36.33),False),
        ('Mersin → Gaziantep',['O-51','D400','D817'],(36.80,34.64),(37.06,37.38),False),
        ('Gaziantep → Diyarbakır',['D400','D875'],(37.06,37.38),(37.91,40.24),False)]
SERV=['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter']
def km_xy(lat,lon):return (lon*math.cos(math.radians(39))*111.32,lat*110.57)
def mesafe(a,b):
    x1,y1=km_xy(*a);x2,y2=km_xy(*b);return math.hypot(x1-x2,y1-y2)
def overpass(sorgu,ad):
    os.makedirs('yol_cache',exist_ok=True);f='yol_cache/'+re.sub(r'\W+','_',ad)+'.json'
    if os.path.exists(f):return json.load(open(f,encoding='utf-8'))
    for s in SERV:
        try:
            r=urllib.request.urlopen(urllib.request.Request(s,urllib.parse.urlencode({'data':sorgu}).encode(),{'User-Agent':'LocalRadar-yol/1.0'}),timeout=180).read()
            d=json.loads(r);json.dump(d,open(f,'w',encoding='utf-8'));time.sleep(2);return d
        except Exception as e:print('  overpass hatası',s,e)
    raise SystemExit('Overpass yanıt vermedi, biraz sonra tekrar dene.')
def hat_verisi(ad,refs,bas,bit):
    s=min(bas[0],bit[0])-0.5;w=min(bas[1],bit[1])-0.5;n=max(bas[0],bit[0])+0.5;e=max(bas[1],bit[1])+0.5
    rx='(^|;) ?('+'|'.join(re.escape(r).replace('-','-?') for r in refs)+') ?($|;)'
    bb='(%s,%s,%s,%s)'%(s,w,n,e)
    d=overpass('[out:json][timeout:180];way[highway~"^(motorway|trunk|primary)$"][ref~"%s"]%s;out geom;'%(rx,bb),ad)
    yollar=[[(p['lat'],p['lon']) for p in el['geometry']] for el in d['elements'] if el.get('geometry')]
    j=overpass('[out:json][timeout:120];node[highway=motorway_junction]%s;out;'%bb,ad+'_kavsak')
    return yollar,[(el['lat'],el['lon']) for el in j['elements']]
def cizge(yollar):
    G=collections.defaultdict(list);P={}
    key=lambda p:(round(p[0],4),round(p[1],4))
    for y in yollar:
        D=[y[0]]
        for a,b in zip(y,y[1:]):
            L=mesafe(a,b);k=max(1,int(L/0.3))
            for i in range(1,k+1):D.append((a[0]+(b[0]-a[0])*i/k,a[1]+(b[1]-a[1])*i/k))
        for a,b in zip(D,D[1:]):
            ka,kb=key(a),key(b);P[ka]=a;P[kb]=b
            if ka==kb:continue
            L=mesafe(a,b);G[ka].append((kb,L));G[kb].append((ka,L))
    return G,P
def dijkstra(G,k0):
    d={k0:0.0};h=[(0.0,k0)]
    while h:
        c,u=heapq.heappop(h)
        if c>d.get(u,1e18):continue
        for v,L in G[u]:
            if c+L<d.get(v,1e18):d[v]=c+L;heapq.heappush(h,(c+L,v))
    return d
def en_yakin(P,pt,aday=None):
    k=min(aday or P,key=lambda q:(P[q][0]-pt[0])**2+(P[q][1]-pt[1])**2);return k,mesafe(P[k],pt)
def yerleri_oku():
    sys.path.insert(0,CORE_YOLU);global C;import local_radar_core as C
    src=open('ulusal_uret.py',encoding='utf-8').read();g={};exec(src[:src.index('rows=[]')],g)
    kara,temiz,marka,DUZ,HARIC=g['kara'],g['temiz'],g['marka'],g['DUZ'],g['HARIC'];yer=[]
    for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
        il=f.split('/')[-1].replace('-Tum-Ilceler.html','');h=open(f,encoding='utf-8').read()
        v=json.JSONDecoder().raw_decode(h[h.find('const V=')+8:])[0];m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);a=DUZ.get(a,DUZ.get(il,a))
        for x in v['I']:
            if x.get('u') or x.get('S') not in C.POPULER_KATEGORILER or not x.get('l') or not x.get('e'):continue
            n0=C._PUA.sub('',x['n']).strip();t=C._PUA.sub('',x.get('t') or '')
            if C._zincir_mi(n0) or kara(n0,t) or HARIC.search(C.fold(n0)):continue
            try:p=float(str(x['p']).replace(',','.'))
            except:continue
            y=x.get('y') or 0
            if MIN_P<=p<=5 and y>=MIN_Y:yer.append(dict(ad=temiz(n0),il=a,ilce=x.get('c') or 'Merkez',kat=x['S'],puan=p,yorum=y,link=x['l'],pt=(x['e'],x['b']),k=marka(n0)))
    Cm=sum(r['puan'] for r in yer)/len(yer)
    for r in yer:r['G']=(r['yorum']*r['puan']+250*Cm)/(r['yorum']+250)
    return yer
def hat_isle(ad,yollar,kavsaklar,bas,bit,yer,otoyol):
    G,P=cizge(yollar)
    if not P:print('  UYARI: yol bulunamadı ->',ad);return None
    kb,sb=en_yakin(P,bas);ke,se=en_yakin(P,bit)
    if sb>25 or se>25:print('  UYARI: başlangıç/bitiş yola uzak (%.0f/%.0f km) ->'%(sb,se),ad)
    d1=dijkstra(G,kb);d2=dijkstra(G,ke)
    if ke not in d1:print('  UYARI: başlangıç ile bitiş birbirine bağlanmıyor (yol parçaları kopuk) ->',ad);return None
    T=d1[ke];koridor={k for k in d1 if d1[k]+d2.get(k,1e18)<=T*1.03+3}
    aday=koridor
    if otoyol and kavsaklar:aday={en_yakin({k:P[k] for k in koridor},j)[0] for j in kavsaklar if en_yakin({k:P[k] for k in koridor},j)[1]<0.3}
    elif otoyol:print('  UYARI: kavşak bulunamadı ->',ad)
    ex=[P[k] for k in aday];lo=min(p[0] for p in ex)-0.05;hi=max(p[0] for p in ex)+0.05;lw=min(p[1] for p in ex)-0.05;hw=max(p[1] for p in ex)+0.05
    cell=collections.defaultdict(list)
    for k in aday:cell[(int(P[k][0]*20),int(P[k][1]*20))].append(k)
    sonuc=[]
    for r in yer:
        a,b=r['pt']
        if not(lo<=a<=hi and lw<=b<=hw):continue
        cand=[k for i in(-1,0,1) for j in(-1,0,1) for k in cell.get((int(a*20)+i,int(b*20)+j),[])]
        if not cand:continue
        k,sap=en_yakin(P,r['pt'],cand)
        if sap<=MAX_SAPMA:sonuc.append(dict(r,km=d1[k],sapma=sap))
    sonuc.sort(key=lambda r:r['km']);secilen=[];dil=collections.defaultdict(list)
    for r in sorted(sonuc,key=lambda r:-r['G']):
        b=int(r['km']//DILIM_KM)
        if len(dil[b])<DILIM_ADET and all(x['k']!=r['k'] for x in dil[b]):dil[b].append(r);secilen.append(r)
    secilen.sort(key=lambda r:r['km'])
    return dict(ad=ad,km=round(T),liste=[dict(ad=r['ad'],il=r['il'],ilce=r['ilce'],kat=r['kat'],puan=r['puan'],yorum=r['yorum'],link=r['link'],km=round(r['km'],1),sapma=round(r['sapma'],1),e=round(r['pt'][0],4),b=round(r['pt'][1],4)) for r in secilen])
def sayfa(veri,cikti):
    S=open('ulusal_sablon.html',encoding='utf-8').read()
    S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
    S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","Yol Üstü Lezzet Molası · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","🛣️ Yol Üstü Lezzet Molası")
    S=S.replace('<div class="fl"><select id="il"></select><select id="kat"></select></div>','<div class="fl"><select id="il"></select><button type="button" class="geo" id="ters">↔ Ters çevir</button></div><div class="fl"><button type="button" class="geo" id="geo" style="flex:1;padding:10px">📍 Konumuma en yakın molaya git</button></div>')
    S=S.replace('</style>','.geo{background:#1e293b;color:var(--text);border:1px solid var(--line);border-radius:12px;padding:0 12px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}.k.vur{outline:2px solid var(--gold)}</style>',1)
    a=S.index('<div class="not">');b=S.index('</div>',a)+6
    S=S[:a]+'''<div class="not"><b>Nasıl seçildi?</b><br>Her hattın ana yol çizgisine en fazla 3 km uzaklıktaki, puanı en az 4,3 ve yorumu en az 100 olan, zincir olmayan yerler alınır. Yol boyunca her 40 km'lik dilimden Güvenilir Skor'u en yüksek 3 yer gösterilir. Mesafeler kuş uçuşudur: otoyol bariyeri nedeniyle gerçek sapma uzun olabilir, bu yüzden otoyollarda yalnızca kavşaklara yakın yerler alınır. Girişe ve park durumuna gitmeden önce Haritalar'dan bakın. Ayrıntılar: <a href="puanlama.html#yol">Puanlama nasıl çalışır?</a></div>'''+S[b:]
    j0=S.index('<script>\n');j1=S.index('</script>',j0)
    js='''<script>
(function(){
var H={hatlar:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
var $=function(i){return document.getElementById(i)},hi=0,ters=false,N=25,ADIM=25,sel=$('il');
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
sel.innerHTML=H.hatlar.map(function(h,i){return'<option value="'+i+'">'+esc(h.ad)+'</option>'}).join('');
function liste(){var h=H.hatlar[hi],l=h.liste.slice();if(ters)l.reverse();return l}
function ciz(vur){var h=H.hatlar[hi],l=liste();$('ac').textContent=h.ad.replace(' → ',ters?' ← ':' → ')+' · yaklaşık '+h.km+' km · '+l.length+' mola';
 $('say').textContent=ters?'Dönüş yönü':'Gidiş yönü';$('sf').style.display='none';
 var lim=Math.max(N,vur!=null?vur+3:0);
 $('liste').innerHTML=l.slice(0,lim).map(function(m,i){var km=ters?Math.round(h.km-m.km):Math.round(m.km);
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
'''
    S=S[:j0]+js+S[j1:]
    T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
    open(cikti,'w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',json.dumps(veri,ensure_ascii=False,separators=(',',':'))))
if __name__=='__main__':
    yer=yerleri_oku();print(len(yer),'aday mekan');out=[]
    if '--test' in sys.argv:
        a,b=(39.93,32.85),(37.87,32.49);yol=[[(a[0]+(b[0]-a[0])*i/60,a[1]+(b[1]-a[1])*i/60) for i in range(61)]]
        h=hat_isle('Ankara → Konya (TEST)',yol,[],a,b,yer,False)
        if h:out.append(h)
        cikti='yol_test.html'
    else:
        for ad,refs,bas,bit,oto in HATLAR:
            print('Hat:',ad);yollar,kav=hat_verisi(ad,refs,bas,bit);print('  yol parçası:',len(yollar),'kavşak:',len(kav))
            h=hat_isle(ad,yollar,kav,bas,bit,yer,oto)
            if h:print('  ',h['km'],'km,',len(h['liste']),'mola');out.append(h)
        cikti='yol.html'
    sayfa(dict(hatlar=out),cikti);print('->',cikti)
    for h in out:print(h['ad'],h['km'],'km',[ (m['ad'],m['il'],m['km'],m['sapma']) for m in h['liste'][:6]])
