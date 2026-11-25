"""Tek İşin Ustaları -> ustalar.html. ulusal_uret.py'nin temizleme kısmını kullanır. Repo kökünden: python3 ustalar_uret.py"""
import re,json,glob,collections
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('rows=[]')])
GR=[('Çorba',r'corba|iskembe|paca'),('Ciğer',r'ciger'),('Tantuni',r'tantuni'),('Kokoreç',r'kokorec'),('Katmer',r'katmer'),('Künefe',r'kunefe'),('Baklava',r'baklava'),('Lahmacun',r'lahmacun'),('Mantı',r'manti'),('Börek',r'borek'),('Köfte',r'kofte(?!.*cig)|kofteci'),('Pide',r'pide|pideci'),('Kebap',r'kebap|kebab|ocakbasi'),('Döner',r'doner'),('Balık',r'balik'),('Kahvaltı',r'kahvalti'),('Dondurma',r'dondurma'),('Tavuk',r'tavuk|pilic'),('Kumpir & Waffle',r'kumpir|waffle'),('Simit & Poğaça',r'simit|pogaca')]
GR=[(k,re.compile(v)) for k,v in GR]
MIN_Y,MIN_P,TOP,ILKOTA,MINGRUP=50,4.3,60,10,20
hamg=collections.defaultdict(list);ad={}
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=f.split('/')[-1].replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();v=json.JSONDecoder().raw_decode(h[h.find('const V=')+8:])[0]
    m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);ad[il]=DUZ.get(a,DUZ.get(il,a))
    for x in v['I']:
        if x.get('u') or x.get('S') not in C.POPULER_KATEGORILER or not x.get('l'):continue
        n0=C._PUA.sub('',x['n']).strip();t=C._PUA.sub('',x.get('t') or '')
        if C._zincir_mi(n0) or kara(n0,t) or HARIC.search(C.fold(n0)):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        y=x.get('y') or 0
        if not(MIN_P<=p<=5) or y<MIN_Y:continue
        fa=C.fold(n0)+' | '+C.fold(t);hit=[k for k,r in GR if r.search(fa)]
        if len(hit)==1:hamg[hit[0]].append(dict(il=ad[il],n=temiz(n0),p=p,y=y,S=x['S'],c=x.get('c') or 'Merkez',l=x['l'],k=marka(n0)))
gruplar=[]
for k,_ in GR:
    L=hamg.get(k,[])
    if len(L)<MINGRUP:continue
    Cm=sum(r['p'] for r in L)/len(L)
    for r in L:r['G']=(r['y']*r['p']+100*Cm)/(r['y']+100)
    L.sort(key=lambda r:-r['G']);ic=collections.Counter();br=set();out=[]
    for r in L:
        if ic[r['il']]>=ILKOTA or r['k'] in br:continue
        ic[r['il']]+=1;br.add(r['k']);out.append(dict(ad=r['n'],il=r['il'],ilce=r['c'],kat=r['S'],puan=r['p'],yorum=r['y'],link=r['l']))
        if len(out)==TOP:break
    gruplar.append(dict(ad=k,toplam=len(L),liste=out))
veri=json.dumps(dict(gruplar=gruplar),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
S=re.sub(r'<div class="sek">.*?</div>\n','<div class="chips" id="chips"></div>\n',S,flags=re.S)
S=S.replace('</style>','.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}.ch{background:rgba(255,255,255,.05);border:1px solid var(--line);color:var(--muted);font-size:13px;font-weight:700;padding:7px 12px;border-radius:20px;cursor:pointer}.ch.a{background:#1e293b;color:var(--text);border-color:var(--gold)}</style>',1)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","Tek İşin Ustaları · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","🍽️ Tek İşin Ustaları")
S=S.replace('<div class="fl"><select id="il"></select><select id="kat"></select></div>','<div class="fl"><select id="il"></select></div>')
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'''<div class="not"><b>Nasıl seçildi?</b><br>Adında ya da türünde tek bir yemek geçen yerler o yemeğin grubuna girer; birden fazla yemek geçenler (ör. "Kebap & Pizza") sayılmaz. Zincirler, kapanmışlar, alkollü mekanlar ve yemek dışı işletmeler çıkarılır. Puanı en az 4,3 ve yorumu en az 50 olanlar değerlendirilir, her yemekte Güvenilir Skor'a göre ilk 60 gösterilir. Bir ilden en fazla 10 yer, aynı markadan 1 şube girer. Grup adı mekanın ad ve türünden tahmin edilir, küçük sapmalar olabilir. Ayrıntılar: <a href="puanlama.html#ustalar">Puanlama nasıl çalışır?</a></div>'''+S[b:]
# JS: gruplar mantığı
j0=S.index('<script>\n');j1=S.index('</script>',j0)
js='''<script>
(function(){
var H={gruplar:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
var G=H.gruplar,gi=0,N=25,ADIM=25,$=function(i){return document.getElementById(i)},elIl=$('il');
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function chips(){$('chips').innerHTML=G.map(function(g,i){return'<button type="button" class="ch'+(i===gi?' a':'')+'" data-i="'+i+'">'+esc(g.ad)+'</button>'}).join('')}
function doldur(){var k=G[gi].liste,o=elIl.value,il=Array.from(new Set(k.map(function(x){return x.il}))).sort(function(a,b){return a.localeCompare(b,'tr')});
 elIl.innerHTML='<option value="">Tüm iller ('+il.length+')</option>'+il.map(function(x){return'<option value="'+esc(x)+'">'+esc(x)+'</option>'}).join('');if(il.indexOf(o)>-1)elIl.value=o}
function ciz(){var g=G[gi],i=elIl.value,l=g.liste.filter(function(m){return!i||m.il===i});
 $('ac').textContent=g.ad+' ustaları: Türkiye genelinde bu işe odaklanan '+g.toplam+' yerden en iyi '+g.liste.length+' tanesi.';
 $('sf').style.display=i?'inline':'none';$('say').textContent=l.length+' mekan listeleniyor';
 if(!l.length){$('liste').innerHTML='<div class="bos">Bu seçime uygun mekan bulunamadı.</div>';$('df').style.display='none';return}
 var lim=i?l.length:Math.min(N,l.length);
 $('liste').innerHTML=l.slice(0,lim).map(function(m){var s=g.liste.indexOf(m)+1;
  return'<a class="k" href="'+esc(m.link)+'" target="_blank" rel="noopener"><div class="no'+(s<=3?' t':'')+'">'+s+'</div><div class="b"><div class="ad">'+esc(m.ad)+'</div><div class="alt">'+esc(m.il)+' / '+esc(m.ilce)+' · '+esc(m.kat)+'</div><div class="pu"><b>★ '+Number(m.puan).toFixed(1).replace('.',',')+'</b> · '+Number(m.yorum).toLocaleString('tr-TR')+' yorum</div></div><div class="ok">↗</div></a>'}).join('');
 var kalan=l.length-lim;if(!i&&kalan>0){$('df').style.display='block';$('df').textContent='Daha fazla göster ('+kalan+' kaldı)'}else $('df').style.display='none'}
$('chips').onclick=function(e){var b=e.target.closest('.ch');if(!b)return;gi=+b.dataset.i;N=ADIM;elIl.value='';chips();doldur();ciz()};
elIl.onchange=function(){N=ADIM;ciz()};$('sf').onclick=function(){elIl.value='';ciz()};$('df').onclick=function(){N+=ADIM;ciz()};
chips();doldur();ciz();
})();
'''
S=S[:j0]+js+S[j1:]
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
open('ustalar.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
print(len(gruplar),'grup',[(g['ad'],len(g['liste'])) for g in gruplar])
