"""Gizli Cevherler -> gizli.html. ulusal_uret.py'nin veri yükleme/temizleme kısmını yeniden kullanır. Repo kökünden: python3 gizli_uret.py"""
import re,json,collections,statistics
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('TR=max(')])
MIN_P,FARK,TOP,K=4.5,0.2,100,150
by=collections.defaultdict(list)
for r in rows:by[r['il']].append(r)
adaylar=[]
_k=collections.defaultdict(list);_t=collections.defaultdict(list)
for r in rows:
    if r['y']>=50:_k[(r['il'],r['S'])].append(r['p']);_t[r['S']].append(r['p'])
def hedef(il,S,ort):
    a=_k.get((il,S),[])
    if len(a)>=8:return sum(a)/len(a)
    a=_t.get(S,[]);return sum(a)/len(a) if len(a)>=8 else ort
for il,L in by.items():
    iyi=[r['p'] for r in L if r['y']>=50]
    if len(L)<50 or len(iyi)<10:continue
    ort=sum(iyi)/len(iyi)
    ys=sorted(r['y'] for r in L)
    tavan=ys[int(len(ys)*0.85)]                       # ilin en çok yorumlu %15'lik dilimi = "herkesin bildiği"
    miny=100 if len(L)>=1000 else 60
    for r in L:
        if not(MIN_P<=r['p']<=5) or r['y']<miny or r['y']>=tavan or r['y']>500:continue
        if r['p']>=5.0 and r['y']<100:continue
        h=hedef(il,r['S'],ort);g=(r['y']*r['p']+K*h)/(r['y']+K)
        if g-h>=FARK:adaylar.append((g-h,r,h))
adaylar.sort(key=lambda a:-a[0])
out=[];ic=collections.Counter();kc=collections.Counter();br=set()
for f,r,ort in adaylar:
    a=ad[r['il']]
    if ic[a]>=(5 if a in BUY else 3) or kc[r['S']]>=20 or r['k'] in br:continue
    out.append(dict(ad=r['n'],il=a,ilce=r['c'] or 'Merkez',e=r.get('e'),b=r.get('b'),kat=r['S'],puan=r['p'],yorum=r['y'],link=r['l'],etiket='Benzerlerinden +%s'%('%.1f'%f).replace('.',',')))
    ic[a]+=1;kc[r['S']]+=1;br.add(r['k'])
    if len(out)==TOP:break
veri=json.dumps(dict(secki=out,zirve=[]),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
S=S.replace('</style>','.geo{background:var(--btn);color:var(--text);border:1px solid var(--line);border-radius:12px;padding:0 12px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}</style>',1)
S=S.replace('<div class="fl"><select id="il"></select><select id="kat"></select></div>','<div class="fl"><select id="il"></select><select id="kat"></select><button type="button" class="geo" id="geo">📍 Yakından uzağa</button></div>')
S=S.replace("var S='secki',","""var __g=false;function __km(a,b,c,d){var r=Math.PI/180,x=(d-b)*r*Math.cos((a+c)/2*r),y=(c-a)*r;return 6371*Math.sqrt(x*x+y*y)}
function __geo(cb){var g=$('geo');if(__g){__g=false;window.__pos=null;g.textContent='📍 Yakından uzağa';cb();return}
 if(!navigator.geolocation){alert('Bu cihazda konum desteklenmiyor.');return}g.textContent='Konum alınıyor…';
 navigator.geolocation.getCurrentPosition(function(p){window.__pos=p.coords;__g=true;g.textContent='⭐ Puana göre';cb()},function(){g.textContent='📍 Yakından uzağa';alert('Konum alınamadı. Tarayıcıda konum iznini kontrol et.')},{timeout:10000})}
function __sirala(l){if(!window.__pos)return l;l=l.slice();l.forEach(function(m){m.km=m.e!=null?__km(window.__pos.latitude,window.__pos.longitude,m.e,m.b):1e9});return l.sort(function(a,b){return a.km-b.km})}
var __KM=function(m){return window.__pos&&m.km<1e8?'<span class="et">'+Math.round(m.km)+' km</span> ':''};
var S='secki',""",1)
S=S.replace("var l=k.filter(function(m){return(!i||m.il===i)&&(!c||m.kat===c)});","var l=__sirala(k.filter(function(m){return(!i||m.il===i)&&(!c||m.kat===c)}));")
S=S.replace("' yorum '+(m.etiket?","' yorum '+__KM(m)+(m.etiket?")
S=S.replace("$('df').onclick=function(){N+=ADIM;ciz()};","$('df').onclick=function(){N+=ADIM;ciz()};$('geo').onclick=function(){__geo(function(){N=ADIM;ciz()})};")
S=S.replace("$('t1').onclick=function(){sek('secki')};$('t2').onclick=function(){sek('zirve')};","")
S=S.replace("$('t1').classList.toggle('a',x==='secki');$('t2').classList.toggle('a',x==='zirve');","")
S=re.sub(r"\$\('ac'\)\.textContent=x==='secki'\?'[^']*':'[^']*';","$('ac').textContent='Herkesin bildiği yerler değil: yorumu azdan ortaya, ama puanı aynı ildeki benzerlerinin ortalamasının belirgin üstünde olan yerler.';",S)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","Gizli Cevherler · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","💎 Gizli Cevherler")
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'''<div class="not"><b>Nasıl seçildi?</b><br>Zincirler, kapanmış yerler, alkollü mekanlar ve yemek dışı işletmeler baştan çıkarılır. Yorumu en az 100 (küçük illerde 60) olan, puanı en az 4,5 olan yerler değerlendirilir. İlin en çok yorum alan %15'lik dilimi (herkesin bildiği yerler) ve 500'den fazla yorumlu olanlar dışarıda tutulur; yorumu 100'ün altındaki tam 5,0 puanlılar da elenir. Kalanlar, az yorumlu yerin puanını ortalamaya doğru çeken Güvenilir Skor'un <b>aynı ildeki aynı türden yerlerin ortalamasından farkına</b> göre sıralanır (çiğ köfteci çiğ köftecilerle, kebapçı kebapçılarla kıyaslanır; ilde o türden yeterince yer yoksa Türkiye ortalaması kullanılır; en az +0,2 fark). Büyükşehirlerden en fazla 5, diğer illerden en fazla 3 yer, kategori başına en fazla 20 yer, marka başına 1 şube girer. Veri son taramayı yansıtır; az yorumlu yerler daha kolay kapanabilir, gitmeden önce Haritalar'dan kontrol edin. Ayrıntılar: <a href="puanlama.html#gizli">Puanlama nasıl çalışır?</a></div>'''+S[b:]
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
open('gizli.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
print(len(adaylar),'aday;',len(out),'liste;',len(ic),'il')
for i,x in enumerate(out[:15],1):print(i,x['ad'],'|',x['il'],'|',x['puan'],x['yorum'],x['kat'],x['etiket'])
print(kc.most_common(4),ic.most_common(4))
