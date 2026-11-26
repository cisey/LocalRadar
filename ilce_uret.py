"""İlçesinin Yıldızları -> ilce.html. Repo kökünden: python3 ilce_uret.py"""
import re,json,glob,collections,statistics
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('rows=[]')])
MIN_N,MAX_N,MIN_P,MIN_Y,PAY=15,200,4.4,100,0.15
ilcel=collections.defaultdict(list);ad={}
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=__import__('os').path.basename(f).replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();v=json.JSONDecoder().raw_decode(h[h.find('const V=')+8:])[0]
    m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);ad[il]=DUZ.get(a,DUZ.get(il,a))
    for x in v['I']:
        if x.get('u') or x.get('S') not in C.POPULER_KATEGORILER or not x.get('l'):continue
        n0=C._PUA.sub('',x['n']).strip();t=C._PUA.sub('',x.get('t') or '')
        if C._zincir_mi(n0) or kara(n0,t) or HARIC.search(C.fold(n0)):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        c=(x.get('c') or '').strip()
        if not c or C.fold(c)=='merkez' or not(0<p<=5) or not x.get('e'):continue
        ilcel[(il,c)].append(dict(il=ad[il],c=c,n=temiz(n0),p=p,y=x.get('y') or 0,S=x['S'],l=x['l'],e=x['e'],b=x['b'],k=marka(n0)))
IZIN={'Istanbul':'sile silivri catalca adalar','Ankara':'beypazari kizilcahamam nallihan ayas gudul sereflikochisar polatli haymana kalecik camlidere elmadag evren bala kahramankazan golbasi akyurt','Izmir':'cesme urla foca seferihisar odemis tire bergama selcuk dikili karaburun beydag kiraz bayindir torbali menderes kinik kemalpasa aliaga'}
out=[];elenen_buyuk=0
for (il,c),L in ilcel.items():
    if len(L)<MIN_N:continue
    if il in IZIN and C.fold(c) not in IZIN[il].split():continue
    if len(L)>MAX_N:elenen_buyuk+=1;continue
    top=sum(r['y'] for r in L);med=statistics.median(r['y'] for r in L) or 1
    Cm=sum(r['p'] for r in L)/len(L)
    best=None
    for r in L:
        pay=r['y']/top if top else 0;kat=r['y']/med
        if r['p']<MIN_P or r['y']<MIN_Y or not(pay>=PAY or kat>=5):continue
        r['G']=(r['y']*r['p']+100*Cm)/(r['y']+100);r['pay']=pay;r['kat']=kat
        if not best or r['G']>best['G']:best=r
    if best:
        r=best;et="İlçedeki yorum payı: %%%d"%round(100*r['pay']) if r['pay']>=PAY else "İlçe ortancasının %d katı"%round(r['kat'])
        out.append(dict(ad=r['n'],il=r['il'],ilce=c,kat=r['S'],puan=r['p'],yorum=r['y'],link=r['l'],etiket=et,e=round(r['e'],4),b=round(r['b'],4),G=r['G'],nn=len(L)))
out.sort(key=lambda x:-x['G'])
for i,x in enumerate(out):x['i']=i;del x['G']
veri=json.dumps(dict(secki=out,zirve=[]),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","İlçesinin Yıldızları · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","⭐ İlçesinin Yıldızları")
S=S.replace('<div class="fl"><select id="il"></select><select id="kat"></select></div>','<div class="fl"><select id="il"></select><button type="button" class="geo" id="geo">📍 Yakından uzağa</button></div>')
S=S.replace('</style>','.ti{color:#fbbf24;font-size:12px;font-weight:800;letter-spacing:.04em;margin-bottom:2px}.geo{background:var(--btn);color:var(--text);border:1px solid var(--line);border-radius:12px;padding:0 12px;font-size:13px;font-weight:700;cursor:pointer;white-space:nowrap}</style>',1)
S=S.replace('<div class="ac" id="ac">','<div class="ac" id="ac">')
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'''<div class="not"><b>Nasıl seçildi?</b><br>İl merkezleri ve büyükşehirlerin kent içi ilçeleri (İstanbul, Ankara, İzmir'de yalnızca kırsal/turistik ilçeler) dışarıda tutulur; yalnızca 15 ile 200 arası yeri taranmış ilçelere bakılır. Her ilçeden, o ilçenin tüm yorumlarının en az %15'ini tek başına alan ya da ilçedeki ortanca yerin 5 katından çok yorumlu olan, puanı en az 4,4 ve yorumu en az 100 olan en iyi bir yer seçilir. Zincirler, kapanmışlar, alkollü mekanlar ve yemek dışı işletmeler çıkarılır. Sıralama Güvenilir Skor'a göredir; "Yakından uzağa" düğmesi konumunu kullanır, konum bilgin cihazından çıkmaz. Ayrıntılar: <a href="puanlama.html#ilce">Puanlama nasıl çalışır?</a></div>'''+S[b:]
j0=S.index('<script>\n');j1=S.index('</script>',j0)
js='''<script>
(function(){
var H={secki:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
var K=H.secki,N=25,ADIM=25,$=function(i){return document.getElementById(i)},elIl=$('il'),geo=false;
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
var il=Array.from(new Set(K.map(function(x){return x.il}))).sort(function(a,b){return a.localeCompare(b,'tr')});
elIl.innerHTML='<option value="">Tüm iller ('+il.length+')</option>'+il.map(function(x){return'<option value="'+esc(x)+'">'+esc(x)+'</option>'}).join('');
$('ac').textContent='İl merkezinden çıkınca sırf yemek için yola çıkmaya değer, kendi ilçesini tek başına taşıyan yerler.';
function km(a,b,c,d){var r=Math.PI/180,x=(d-b)*r*Math.cos((a+c)/2*r),y=(c-a)*r;return 6371*Math.sqrt(x*x+y*y)}
function ciz(){var i=elIl.value,l=K.filter(function(m){return!i||m.il===i});
 $('sf').style.display=i?'inline':'none';$('say').textContent=l.length+' ilçe yıldızı listeleniyor';
 if(!l.length){$('liste').innerHTML='<div class="bos">Bu seçime uygun yer bulunamadı.</div>';$('df').style.display='none';return}
 var lim=i?l.length:Math.min(N,l.length);
 $('liste').innerHTML=l.slice(0,lim).map(function(m,x){
  var d=geo&&m.km!=null?'<span class="et">'+Math.round(m.km)+' km</span> ':'';
  return'<a class="k" href="'+esc(m.link)+'" target="_blank" rel="noopener"><div class="b"><div class="ti">'+esc(m.ilce.toLocaleUpperCase('tr-TR'))+' · '+esc(m.il)+'</div><div class="ad">'+esc(m.ad)+'</div><div class="alt">'+esc(m.kat)+'</div><div class="pu"><b>★ '+Number(m.puan).toFixed(1).replace('.',',')+'</b> · '+Number(m.yorum).toLocaleString('tr-TR')+' yorum '+d+'<span class="et">'+esc(m.etiket)+'</span></div></div><div class="ok">↗</div></a>'}).join('');
 var kalan=l.length-lim;if(!i&&kalan>0){$('df').style.display='block';$('df').textContent='Daha fazla göster ('+kalan+' kaldı)'}else $('df').style.display='none'}
elIl.onchange=function(){N=ADIM;ciz()};$('sf').onclick=function(){elIl.value='';ciz()};$('df').onclick=function(){N+=ADIM;ciz()};
$('geo').onclick=function(){
 if(geo){geo=false;K.sort(function(a,b){return a.i-b.i});$('geo').textContent='📍 Yakından uzağa';N=ADIM;ciz();return}
 if(!navigator.geolocation){alert('Bu cihazda konum desteklenmiyor.');return}
 $('geo').textContent='Konum alınıyor…';
 navigator.geolocation.getCurrentPosition(function(p){K.forEach(function(m){m.km=km(p.coords.latitude,p.coords.longitude,m.e,m.b)});K.sort(function(a,b){return a.km-b.km});geo=true;$('geo').textContent='⭐ Puana göre';N=ADIM;ciz()},function(){$('geo').textContent='📍 Yakından uzağa';alert('Konum alınamadı. Tarayıcıda konum iznini kontrol et.')},{timeout:10000});};
ciz();
(function(){var q=new URLSearchParams(location.search).get('il');if(!q)return;var __f=function(s){return String(s).toLocaleLowerCase('tr').replace(/[çğıöşü]/g,function(c){return{'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u'}[c]})};for(var i=0;i<elIl.options.length;i++){if(__f(elIl.options[i].value)===__f(q)){elIl.value=elIl.options[i].value;ciz();break}}})();
})();
'''
S=S[:j0]+js+S[j1:]
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
open('ilce.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
print(len(ilcel),'ilçe;',sum(1 for L in ilcel.values() if len(L)>=MIN_N),'>=15;',elenen_buyuk,'büyük elendi;',len(out),'yıldız')
c=collections.Counter(x['il'] for x in out);print(len(c),c.most_common(5))
for x in out[:12]:print(x['ad'],'|',x['il'],x['ilce'],x['puan'],x['yorum'],x['etiket'],x['nn'])
