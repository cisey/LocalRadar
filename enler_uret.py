"""Türkiye'nin En'leri -> enler.html. Repo kökünden: python3 enler_uret.py"""
import re,json,glob,collections,statistics,os
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('rows=[]')])
KISMI=300
yer=[];ad={}
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=os.path.basename(f).replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();v=json.JSONDecoder().raw_decode(h[h.find('const V=')+8:])[0]
    m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);a=DUZ.get(a,DUZ.get(il,a));ad[il]=a
    for x in v['I']:
        if x.get('u') or x.get('S') not in C.POPULER_KATEGORILER or not x.get('l'):continue
        n0=C._PUA.sub('',x['n']).strip();t=C._PUA.sub('',x.get('t') or '')
        if C._zincir_mi(n0) or kara(n0,t) or HARIC.search(C.fold(n0)):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        if not(0<p<=5):continue
        yer.append(dict(ad=temiz(n0),il=a,ilce=(x.get('c') or '').strip() or 'Merkez',p=p,y=x.get('y') or 0,S=x['S'],l=x['l'],k=marka(n0)))
Cm=sum(r['p'] for r in yer)/len(yer)
for r in yer:r['G']=(r['y']*r['p']+250*Cm)/(r['y']+250)
def fmt(x):return str(round(x,1)).replace('.',',')
def bin_(n):return format(n,',').replace(',','.')
def yrow(r,sol=''):return dict(sol=sol,ad=r['ad'],alt=r['il']+' / '+r['ilce']+' · '+r['S'],sag='★ '+fmt(r['p'])+' · '+bin_(r['y'])+' yorum',l=r['l'])
def tek(L):   # aynı markadan tek şube
    g=set();o=[]
    for r in L:
        if r['k'] in g:continue
        g.add(r['k']);o.append(r)
    return o
B=[]
B.append(dict(b='En çok yorum alan 10 yer',a='Zincirler hariç, Türkiye genelinde Haritalar\'da en çok yorum alan işletmeler.',s=[yrow(r,str(i+1)) for i,r in enumerate(tek(sorted(yer,key=lambda r:-r['y']))[:10])]))
B.append(dict(b='En yüksek puanlı 10 yer',a='2.000+ yorumu olan yerler arasından Güvenilir Skor\'a göre. Çok yorumla yüksek puanı bir arada tutmak zordur.',s=[yrow(r,str(i+1)) for i,r in enumerate(tek(sorted([r for r in yer if r['y']>=2000],key=lambda r:-r['G']))[:10])]))
kat=[]
for k in sorted({r['S'] for r in yer}):
    c=[r for r in yer if r['S']==k and r['y']>=500]
    if c:
        r=max(c,key=lambda r:r['G']);d=yrow(r,'');d['sol']='';d['ad']=r['ad'];d['alt']=k+' · '+r['il']+' / '+r['ilce'];kat.append(d)
B.append(dict(b='Kategorilerin şampiyonları',a='Her kategoride 500+ yorumlu yerler arasından Güvenilir Skor\'u en yüksek olan.',s=kat))
# il rekorları
il_k=collections.defaultdict(collections.Counter);il_p=collections.defaultdict(list);il_y=collections.defaultdict(list)
for r in yer:il_k[r['il']][r['S']]+=1;il_p[r['il']].append(r['p']);il_y[r['il']].append(r['y'])
T=[i for i in il_k if sum(il_k[i].values())>=KISMI];tum=collections.Counter()
for c in il_k.values():tum.update(c)
N=sum(tum.values())
pay=lambda i,k:100*il_k[i][k]/sum(il_k[i].values())
def ilrow(baslik,i,deg):return dict(sol='',ad=baslik+': '+i,alt=deg,sag='',l='dna.html?il1='+i)
def zi(k):
    i=max(T,key=lambda i:pay(i,k));return i
ls=[]
for k,bs in (('Fırın & Tatlı','Tatlı & fırın'),('Döner & Kebap','Kebap/döner'),('Balık & Deniz Ürünleri','Balık'),('Kafe & Kahve','Kafe/kahve'),('Çiğ Köfte','Çiğ köfte'),('Pide & Lahmacun','Pide/lahmacun'),('Kahvaltı','Kahvaltı')):
    i=zi(k);ls.append(ilrow(bs+' payı en yüksek il',i,'%'+fmt(pay(i,k))+' (Türkiye ortalaması %'+fmt(100*tum[k]/N)+')'))
i=max(T,key=lambda i:statistics.median(il_p[i]));ls.append(ilrow('En cömert puan veren il',i,'ortanca puan '+str(round(statistics.median(il_p[i]),2)).replace('.',',')))
i=min(T,key=lambda i:statistics.median(il_p[i]));ls.append(ilrow('En zor beğenen il',i,'ortanca puan '+str(round(statistics.median(il_p[i]),2)).replace('.',',')))
i=max(T,key=lambda i:statistics.median(il_y[i]));ls.append(ilrow('En çok yorum yazılan il',i,'ortanca '+str(int(statistics.median(il_y[i])))+' yorum'))
i=max(il_k,key=lambda i:sum(il_k[i].values()));ls.append(ilrow('En çok mekanı olan il',i,bin_(sum(il_k[i].values()))+' mekan'))
B.append(dict(b='İl rekorları',a='Yalnızca 300+ yeri taranmış iller karşılaştırılır (mekan sayısı satırı hariç). Satıra dokununca ilin DNA sayfası açılır.',s=ls))
# ilçe rekorları
ic=collections.defaultdict(list)
for r in yer:ic[(r['il'],r['ilce'])].append(r)
BUY=[k for k,L in ic.items() if len(L)>=100]
def irow(k,deg):return dict(sol='',ad=k[1]+' · '+k[0],alt=deg,sag='',l='gizli.html?il='+k[0])
s=[]
for k in sorted(ic,key=lambda k:-len(ic[k]))[:3]:s.append(irow(k,bin_(len(ic[k]))+' mekan · en kalabalık ilçelerden'))
k=max(BUY,key=lambda k:statistics.median(r['p'] for r in ic[k]));s.append(irow(k,'ortanca puan '+str(round(statistics.median(r['p'] for r in ic[k]),2)).replace('.',',')+' · en cömert ilçe (100+ mekan)'))
k=min(BUY,key=lambda k:statistics.median(r['p'] for r in ic[k]));s.append(irow(k,'ortanca puan '+str(round(statistics.median(r['p'] for r in ic[k]),2)).replace('.',',')+' · en zor beğenen ilçe (100+ mekan)'))
k=max(BUY,key=lambda k:statistics.median(r['y'] for r in ic[k]));s.append(irow(k,'ortanca '+str(int(statistics.median(r['y'] for r in ic[k])))+' yorum · en çok yorum yazılan ilçe (100+ mekan)'))
B.append(dict(b='İlçe rekorları',a='100\'den çok mekanı olan ilçeler arasından. Satıra dokununca o ilin gizli cevherleri açılır.',s=s))
veri=json.dumps(dict(bolumler=B),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","Türkiye'nin En'leri · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","🏅 Türkiye'nin En'leri")
a=S.index('<div class="fl">');b=S.index('</div>',a)+6;S=S[:a]+S[b:]
S=S.replace('</style>','details.bol{margin:10px 0;background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}details.bol>summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;padding:14px 16px;font-size:16px;font-weight:800}details.bol>summary::-webkit-details-marker{display:none}details.bol>summary:after{content:"›";font-size:22px;color:var(--muted);transition:transform .2s}details.bol[open]>summary:after{transform:rotate(90deg);color:var(--accent)}details.bol .ic{padding:0 14px 12px}.ic .tn{font-size:12.5px;color:var(--muted);margin:0 2px 8px}.er{display:flex;gap:10px;align-items:flex-start;padding:9px 0;border-top:1px solid var(--line);color:var(--text);text-decoration:none}.er .no{min-width:22px;color:var(--gold);font-weight:800}.er .ad{font-weight:700;font-size:14.5px}.er .al{font-size:12px;color:var(--muted)}.er .sg{font-size:12.5px;color:var(--soft);margin-top:1px}</style>',1)
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'<div class="not"><b>Nasıl hesaplandı?</b><br>Zincirler, kapanmışlar, alkollü mekanlar ve yemek dışı işletmeler çıkarılmış tüm yerler üzerinden hesaplanır. Yer sıralamalarında aynı markadan tek şube sayılır; Güvenilir Skor\'daki K 250\'dir. İl karşılaştırmalarında 300+ yeri taranmış iller esas alınır. Ayrıntılar: <a href="puanlama.html">Puanlama nasıl çalışır?</a></div>'+S[b:]
j0=S.index('<script>\n');j1=S.index('</script>',j0)
js='''<script>
(function(){var H={bolumler:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
var $=function(i){return document.getElementById(i)};
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
$('ac').textContent='Zirvedekiler, rekorlar ve ilginç karşılaştırmalar: tek sayfada Türkiye\\'nin en\\'leri.';
$('say').textContent='';var sf=$('sf');if(sf)sf.style.display='none';var df=$('df');if(df)df.style.display='none';
$('liste').innerHTML=H.bolumler.map(function(b,i){return'<details class="bol"'+(i<2?' open':'')+'><summary>'+esc(b.b)+'</summary><div class="ic"><div class="tn">'+esc(b.a)+'</div>'+b.s.map(function(r){var no=r.sol?'<div class="no">'+esc(r.sol)+'</div>':'';var ext=/^https?:/.test(r.l);return'<a class="er" href="'+esc(r.l)+'"'+(ext?' target="_blank" rel="noopener"':'')+'>'+no+'<div><div class="ad">'+esc(r.ad)+'</div><div class="al">'+esc(r.alt)+'</div>'+(r.sag?'<div class="sg">'+esc(r.sag)+'</div>':'')+'</div></a>'}).join('')+'</div></details>'}).join('');
})();
'''
S=S[:j0]+js+S[j1:]
T_=open('puanlama.html',encoding='utf-8').read();gt=T_[T_.find('<!-- Google tag'):T_.find('<meta charset')]
open('enler.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
for b in B:print(b['b'],len(b['s']),b['s'][0]['ad'][:50],b['s'][0].get('sag'))
