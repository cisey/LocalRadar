"""Yürünebilir Lezzet Kümeleri -> kumeler.html. Repo kökünden: python3 kumeler_uret.py"""
import re,json,glob,collections,math,os
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('rows=[]')])
R,MIN_N,MIN_KAT,MIN_P,MIN_Y=0.25,5,2,4.3,100       # yarıçap km, kümede en az mekan, en az kategori
KOTA={'İstanbul':15,'Ankara':10,'İzmir':10};KOTA_D=5;MAXY=8
yer=[];ad={}
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=os.path.basename(f).replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();v=json.JSONDecoder().raw_decode(h[h.find('const V=')+8:])[0]
    m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);a=DUZ.get(a,DUZ.get(il,a))
    for x in v['I']:
        if x.get('u') or x.get('S') not in C.POPULER_KATEGORILER or not x.get('l') or not x.get('e'):continue
        n0=C._PUA.sub('',x['n']).strip();t=C._PUA.sub('',x.get('t') or '')
        if C._zincir_mi(n0) or kara(n0,t) or HARIC.search(C.fold(n0)) or x['S']=='Fast food & Burger & Pizza' or re.search(r'bufe|buffet|(?<![a-z])tost',C.fold(n0)):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        y=x.get('y') or 0
        if MIN_P<=p<=5 and y>=MIN_Y:yer.append(dict(il=a,ilce=(x.get('c') or '').strip(),ad=temiz(n0),p=p,y=y,S=x['S'],l=x['l'],e=x['e'],b=x['b'],k=marka(n0)))
Cm=sum(r['p'] for r in yer)/len(yer)
for r in yer:r['G']=(r['y']*r['p']+250*Cm)/(r['y']+250);r['v']=max(0.05,r['G']-4.0)
def km(a,b,c,d):
    r=math.pi/180;x=(d-b)*r*math.cos((a+c)/2*r);y=(c-a)*r;return 6371*math.hypot(x,y)
byil=collections.defaultdict(list)
for r in yer:byil[r['il']].append(r)
kume=[]
MAXKUME=25
def bol(M):
    """25'ten büyük kümeyi k-means ile parçalara ayır; her parça kuralı sağlamalı."""
    if len(M)<=MAXKUME:return [M]
    k=-(-len(M)//MAXKUME);ms=[(m['e'],m['b']) for m in M]
    c=[ms[0]]
    while len(c)<k:c.append(max(ms,key=lambda p:min(km(p[0],p[1],q[0],q[1]) for q in c)))
    for _ in range(12):
        g=[[] for _ in c]
        for m,p in zip(M,ms):g[min(range(k),key=lambda t:km(p[0],p[1],c[t][0],c[t][1]))].append(m)
        c=[(sum(m['e'] for m in x)/len(x),sum(m['b'] for m in x)/len(x)) if x else c[t] for t,x in enumerate(g)]
    return [x for x in g if len(x)>=MIN_N and len({m['S'] for m in x})>=MIN_KAT]
def ekle(M):
    e=sum(m['e'] for m in M)/len(M);b=sum(m['b'] for m in M)/len(M)
    ic=collections.Counter(m['ilce'] for m in M if m['ilce']).most_common(1)
    kat=collections.Counter(m['S'] for m in M)
    M.sort(key=lambda m:-m['G'])
    kume.append(dict(il=il,ilce=ic[0][0] if ic else 'Merkez',e=round(e,4),b=round(b,4),n=len(M),kat=dict(kat.most_common()),puan=sum(sorted((m['v'] for m in M),reverse=True)[:12]),
        mekan=[dict(ad=m['ad'],p=m['p'],y=m['y'],kat=m['S'],l=m['l']) for m in M[:MAXY+4]]))

for il,L in byil.items():
    cell=collections.defaultdict(list)
    for i,r in enumerate(L):cell[(int(r['e']*100),int(r['b']*100))].append(i)
    def komsu(i):
        r=L[i];ci,cj=int(r['e']*100),int(r['b']*100)
        return [j for a in(-1,0,1) for b in(-1,0,1) for j in cell.get((ci+a,cj+b),[]) if km(r['e'],r['b'],L[j]['e'],L[j]['b'])<=R]
    N={i:komsu(i) for i in range(len(L))}
    sk=lambda i:sum(sorted((L[j]['v'] for j in N[i]),reverse=True)[:12])
    sira=sorted(range(len(L)),key=lambda i:-sk(i))
    kullan=set()
    for i in sira:
        if i in kullan:continue
        uyeler=[j for j in N[i] if j not in kullan]
        # aynı markadan tek şube
        gor=set();u2=[]
        for j in sorted(uyeler,key=lambda j:-L[j]['G']):
            if L[j]['k'] in gor:continue
            gor.add(L[j]['k']);u2.append(j)
        if len(u2)<MIN_N or len({L[j]['S'] for j in u2})<MIN_KAT:continue
        M0=[L[j] for j in u2];kullan.update(uyeler)
        for M in bol(M0):
            ekle(M)
        continue
kume.sort(key=lambda k:-k['puan'])
sayac=collections.Counter();out=[]
for k in kume:
    if sayac[k['il']]>=KOTA.get(k['il'],KOTA_D):continue
    sayac[k['il']]+=1;del k['puan'];out.append(k)
veri=json.dumps(dict(kumeler=out),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","Yürünebilir Lezzet Kümeleri · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","🚶 Yürünebilir Lezzet Kümeleri")
S=S.replace('<div class="fl"><select id="il"></select><select id="kat"></select></div>','<div class="fl"><select id="il"></select><button type="button" class="geo" id="geo">📍 Yakından uzağa</button></div>')
S=S.replace('</style>','.geo{background:var(--btn);color:var(--text);border:1px solid var(--line);border-radius:12px;padding:0 12px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}.kc{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin:8px 0}.kc .ti{color:var(--gold);font-size:12px;font-weight:800;letter-spacing:.04em}.kc .bs{font-weight:800;font-size:16px;margin:2px 0}.kc .kt{color:var(--muted);font-size:12.5px}.kc ol{margin:8px 0 0 18px;font-size:13.5px}.kc li{margin:3px 0}.kc li a{color:var(--text);text-decoration:none;font-weight:600}.kc li small{color:var(--muted)}.kc li b{color:var(--gold)}.bt{display:flex;gap:8px;margin-top:10px}.bt a,.bt button{flex:1;text-align:center;background:var(--btn);color:var(--text);border:1px solid var(--line);border-radius:10px;padding:9px 6px;font:inherit;font-size:13px;font-weight:700;text-decoration:none;cursor:pointer}</style>',1)
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'''<div class="not"><b>Nasıl seçildi?</b><br>Zincirler, kapanmış yerler, alkollü mekanlar, büfe/tost/fast food ve yemek dışı işletmeler çıkarılır; puanı en az 4,3 ve yorumu en az 100 olan yerler değerlendirilir. Bir mekanın 250 metre çevresinde, aynı markadan tek şube sayılarak en az 5 kaliteli mekan ve en az 2 farklı kategori varsa o nokta bir küme olur (5 çiğ köfteci yan yana küme sayılmaz). Birbirine geçen kümelerden yalnızca kalite toplamı yüksek olan kalır; 25'ten çok mekanı olan büyük kümeler konuma göre iki ya da daha fazla yürünebilir parçaya bölünür. Büyükşehirlerden en fazla 15 (İstanbul) ya da 10 (Ankara, İzmir), diğer illerden 5 küme gösterilir. "Bölgeye yol tarifi", kümedeki mekanların ortalama konumunu Haritalar'da açar; park yerini oraya yakın seçersin. Ayrıntılar: <a href="puanlama.html#kumeler">Puanlama nasıl çalışır?</a></div>'''+S[b:]
j0=S.index('<script>\n');j1=S.index('</script>',j0)
js='''<script>
(function(){
var H={kumeler:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
var K=H.kumeler,N=25,ADIM=25,$=function(i){return document.getElementById(i)},elIl=$('il'),geo=false,ac={};
K.forEach(function(k,i){k.i=i});
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
var il=Array.from(new Set(K.map(function(x){return x.il}))).sort(function(a,b){return a.localeCompare(b,'tr')});
elIl.innerHTML='<option value="">Tüm iller ('+il.length+')</option>'+il.map(function(x){return'<option value="'+esc(x)+'">'+esc(x)+'</option>'}).join('');
$('ac').textContent='Arabayı bir kez park et, yürüyerek birkaç iyi mekana ulaş: 250 metre içinde farklı türlerde en az 5 kaliteli mekan.';
function km(a,b,c,d){var r=Math.PI/180,x=(d-b)*r*Math.cos((a+c)/2*r),y=(c-a)*r;return 6371*Math.sqrt(x*x+y*y)}
function kisa(s){return s.replace(' & ','/').replace('Türk/Aile Restoranı','Aile Restoranı')}
function ciz(){var i=elIl.value,l=K.filter(function(m){return!i||m.il===i});
 $('sf').style.display=i?'inline':'none';$('say').textContent=l.length+' küme listeleniyor';
 if(!l.length){$('liste').innerHTML='<div class="bos">Bu seçime uygun küme bulunamadı.</div>';$('df').style.display='none';return}
 var lim=i?l.length:Math.min(N,l.length);
 $('liste').innerHTML=l.slice(0,lim).map(function(k){var acik=ac[k.i],m=acik?k.mekan:k.mekan.slice(0,5);
  var kt=Object.keys(k.kat).map(function(c){return k.kat[c]+' '+esc(kisa(c))}).join(' · ');
  var d=geo&&k.km!=null?'<span class="et">'+Math.round(k.km)+' km</span> ':'';
  return'<div class="kc"><div class="ti">'+esc(k.ilce.toLocaleUpperCase('tr-TR'))+' · '+esc(k.il)+'</div><div class="bs">'+k.n+' iyi mekan '+d+'</div><div class="kt">'+kt+'</div><ol>'+m.map(function(x){return'<li><a href="'+esc(x.l)+'" target="_blank" rel="noopener">'+esc(x.ad)+'</a> <b>★ '+Number(x.p).toFixed(1).replace('.',',')+'</b> <small>'+Number(x.y).toLocaleString('tr-TR')+' yorum · '+esc(kisa(x.kat))+'</small></li>'}).join('')+'</ol>'+
  '<div class="bt"><a href="https://www.google.com/maps/dir/?api=1&destination='+k.e+','+k.b+'" target="_blank" rel="noopener">🧭 Bölgeye yol tarifi</a><button type="button" data-i="'+k.i+'">'+(acik?'Daha az göster':'En iyi '+k.mekan.length+' mekan')+'</button></div></div>'}).join('');
 var kalan=l.length-lim;if(!i&&kalan>0){$('df').style.display='block';$('df').textContent='Daha fazla göster ('+kalan+' kaldı)'}else $('df').style.display='none'}
$('liste').onclick=function(e){var b=e.target.closest('button[data-i]');if(!b)return;var i=+b.dataset.i;ac[i]=!ac[i];ciz()};
elIl.onchange=function(){N=ADIM;ciz()};$('sf').onclick=function(){elIl.value='';ciz()};$('df').onclick=function(){N+=ADIM;ciz()};
$('geo').onclick=function(){
 if(geo){geo=false;K.sort(function(a,b){return a.i-b.i});$('geo').textContent='📍 Yakından uzağa';N=ADIM;ciz();return}
 if(!navigator.geolocation){alert('Bu cihazda konum desteklenmiyor.');return}
 $('geo').textContent='Konum alınıyor…';
 navigator.geolocation.getCurrentPosition(function(p){K.forEach(function(m){m.km=km(p.coords.latitude,p.coords.longitude,m.e,m.b)});K.sort(function(a,b){return a.km-b.km});geo=true;$('geo').textContent='⭐ Kaliteye göre';N=ADIM;ciz()},function(){$('geo').textContent='📍 Yakından uzağa';alert('Konum alınamadı. Tarayıcıda konum iznini kontrol et.')},{timeout:10000})};
(function(){var q=new URLSearchParams(location.search).get('il');if(!q)return;var f=function(s){return String(s).toLocaleLowerCase('tr').replace(/[çğıöşü]/g,function(c){return{'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u'}[c]})};for(var i=0;i<elIl.options.length;i++){if(f(elIl.options[i].value)===f(q)){elIl.value=elIl.options[i].value;break}}})();
ciz();
})();
'''
S=S[:j0]+js+S[j1:]
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
open('kumeler.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
print(len(yer),'aday;',len(out),'küme;',len(byil),'il;',len(veri)//1024,'KB')
for k in out[:8]:print(k['il'],k['ilce'],k['n'],k['kat'],[m['ad'] for m in k['mekan'][:3]])
