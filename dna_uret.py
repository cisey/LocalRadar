"""İllerin Lezzet DNA'sı -> dna.html. Repo kökünden: python3 dna_uret.py"""
import re,json,glob,collections,statistics
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('rows=[]')])
KISMI=300
il_k=collections.defaultdict(collections.Counter);il_p=collections.defaultdict(list);il_y=collections.defaultdict(list);ad={}
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=__import__('os').path.basename(f).replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();v=json.JSONDecoder().raw_decode(h[h.find('const V=')+8:])[0]
    m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);ad[il]=DUZ.get(a,DUZ.get(il,a))
    for x in v['I']:
        if x.get('u') or x.get('S') not in C.POPULER_KATEGORIES if False else (x.get('u') or x.get('S') not in C.POPULER_KATEGORILER):continue
        n0=C._PUA.sub('',x['n']).strip();t=C._PUA.sub('',x.get('t') or '')
        if C._zincir_mi(n0) or kara(n0,t) or HARIC.search(C.fold(n0)):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        if not(0<p<=5):continue
        il_k[il][x['S']]+=1;il_p[il].append(p);il_y[il].append(x.get('y') or 0)
tum=collections.Counter()
for c in il_k.values():tum.update(c)
N=sum(tum.values());kats=[k for k,_ in tum.most_common()]
trpay={k:tum[k]/N for k in kats}
trp=statistics.median([p for L in il_p.values() for p in L]);try_=statistics.median([y for L in il_y.values() for y in L])
iller=[]
for il in sorted(il_k,key=lambda a:ad[a].replace('İ','I').lower()):
    n=sum(il_k[il].values())
    if n<20:continue
    pay={k:round(100*il_k[il][k]/n,1) for k in kats}
    iller.append(dict(f=il,il=ad[il],n=n,kismi=n<KISMI,pay=pay,endeks={k:round(pay[k]/100/trpay[k],2) for k in kats},p=round(statistics.median(il_p[il]),2),y=int(statistics.median(il_y[il]))))
veri=json.dumps(dict(kats=kats,tr=dict(pay={k:round(100*trpay[k],1) for k in kats},p=round(trp,2),y=int(try_),n=N),iller=iller),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
CSS='''.sec{display:flex;gap:8px;margin-bottom:12px}.kr{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin:10px 0}
.kr a{color:var(--accent);text-decoration:none}.kr h2{font-size:16px;margin-bottom:4px}.ozet{font-size:13px;color:#cbd5e1;margin:4px 0 8px}.ozet b{color:var(--gold)}
.sat{display:grid;grid-template-columns:96px 1fr;gap:8px;align-items:center;font-size:12px;margin:6px 0}.sat .kn{color:var(--muted);line-height:1.2}
.bar{height:9px;border-radius:5px;background:rgba(255,255,255,.07);position:relative;overflow:hidden;margin:2px 0}.bar i{display:block;height:100%;border-radius:5px;background:var(--accent)}.bar.b2 i{background:var(--gold)}
.sy{font-size:11px;color:#cbd5e1}.kis{font-size:11px;color:#fbbf24;background:rgba(251,191,36,.12);border-radius:6px;padding:1px 7px;margin-left:6px}
.mt{display:flex;gap:14px;flex-wrap:wrap;font-size:12.5px;color:#cbd5e1;margin-top:6px}.mt b{color:var(--gold)}.lg{display:flex;gap:12px;font-size:12px;color:var(--muted);margin:2px 0 6px}.lg span:before{content:"";display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:5px;background:var(--accent)}.lg span.l2:before{background:var(--gold)}
'''
S=S.replace('</style>',CSS+'</style>',1)
S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","İllerin Lezzet DNA'sı · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","🧬 İllerin Lezzet DNA'sı")
S=S.replace('<p class="ac" id="ac"></p>','<p class="ac" id="ac">Bir ilin yemek kültürü hangi kategoride yoğunlaşıyor? Bir il seç, istersen ikinci bir ille karşılaştır.</p>')
S=S.replace('<div class="fl"><select id="il"></select><select id="kat"></select></div>','<div class="sec"><select id="il1"></select><select id="il2"></select></div>')
a=S.index('<div class="dr">');b=S.index('<div class="not">')
S=S[:a]+'<div id="kart"></div>\n<div id="rek"></div>\n'+S[b:]
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'''<div class="not"><b>Nasıl hesaplandı?</b><br>Her ilde taranan yerlerin (zincirler, kapanmışlar, alkollü ve yemek dışı yerler çıkarılmış) kategori dağılımı hesaplanır. Çubuklar ilin payını, "Türkiye'ye göre" değeri bu payın Türkiye ortalamasının kaç katı olduğunu gösterir (ör. 1,8× = ortalamanın 1,8 katı). Ortanca puan ve ortanca yorum, il içindeki yerlerin tam ortadaki değeridir. Taranan yeri 300'ün altında olan illerde oranlar sapabilir, bu illerde "kısmi veri" etiketi görünür. Ayrıntılar: <a href="puanlama.html#dna">Puanlama nasıl çalışır?</a></div>'''+S[b:]
j0=S.index('<script>\n');j1=S.index('</script>',j0)
js='''<script>
(function(){
var H={kats:[],tr:{pay:{}},iller:[]};try{H=JSON.parse(document.getElementById('veri').textContent)}catch(e){}
var $=function(i){return document.getElementById(i)},I=H.iller;
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function f1(n){return String(n).replace('.',',')}
function ilOpt(ilk){return (ilk?'':'<option value="">Karşılaştır… (isteğe bağlı)</option>')+I.map(function(x,i){return'<option value="'+i+'">'+esc(x.il)+'</option>'}).join('')}
$('il1').innerHTML=ilOpt(true);$('il2').innerHTML=ilOpt(false);
var mx=Math.max.apply(null,I.map(function(x){return Math.max.apply(null,H.kats.map(function(k){return x.pay[k]}))}).concat([30]));
function ozet(x){var s=H.kats.slice().sort(function(a,b){return x.endeks[b]-x.endeks[a]}),u=s[0],z=s[s.length-1];
 var t='En baskın: <b>'+esc(u)+'</b> (Türkiye ortalamasının '+f1(x.endeks[u])+' katı). En az: '+esc(z)+' ('+f1(x.endeks[z])+'×).';
 t+='<div class="mt"><span>Taranan yer: <b>'+x.n.toLocaleString('tr-TR')+'</b></span><span>Ortanca puan: <b>'+f1(x.p.toFixed(2))+'</b> <small>(TR '+f1(H.tr.p.toFixed(2))+')</small></span><span>Ortanca yorum: <b>'+x.y+'</b> <small>(TR '+H.tr.y+')</small></span></div>';return t}
function bar(v,c){return'<div class="bar'+(c?' b2':'')+'"><i style="width:'+Math.round(100*v/mx)+'%"></i></div>'}
function ciz(){var a=I[+$('il1').value],bi=$('il2').value,b=bi===''?null:I[+bi],h='';
 var kis=function(x){return x.kismi?'<span class="kis">kısmi veri</span>':''};
 h+='<div class="kr"><h2>'+esc(a.il)+kis(a)+'</h2><div class="ozet">'+ozet(a)+'</div></div>';
 if(b)h+='<div class="kr"><h2>'+esc(b.il)+kis(b)+'</h2><div class="ozet">'+ozet(b)+'</div></div>';
 h+='<div class="kr"><div class="lg"><span>'+esc(a.il)+'</span>'+(b?'<span class="l2">'+esc(b.il)+'</span>':'')+'</div>';
 H.kats.slice().sort(function(x,y){return a.endeks[y]-a.endeks[x]}).forEach(function(k){
  h+='<div class="sat"><div class="kn">'+esc(k)+'<div class="sy">TR %'+f1(H.tr.pay[k])+'</div></div><div>'+bar(a.pay[k])+'<div class="sy">%'+f1(a.pay[k])+' · '+f1(a.endeks[k])+'×'+'</div>'+(b?bar(b.pay[k],1)+'<div class="sy">%'+f1(b.pay[k])+' · '+f1(b.endeks[k])+'×</div>':'')+'</div></div>'});
 h+='</div>';var q=encodeURIComponent(a.il);
 h+='<div class="kr"><div class="ozet"><b>'+esc(a.il)+'</b> için: <a href="gizli.html?il='+q+'">💎 Gizli cevherler</a> · <a href="ulusal.html?il='+q+'">🏆 En popülerler</a> · <a href="ilce.html?il='+q+'">⭐ İlçe yıldızları</a> · <a href="rehberler/'+esc(a.f)+'-Tum-Ilceler.html">📖 İl rehberi</a></div></div>';
 $('kart').innerHTML=h;try{var u=new URLSearchParams(location.search);u.set('il1',a.il);if(b)u.set('il2',b.il);else u.delete('il2');history.replaceState(null,'','?'+u.toString())}catch(e){}}
function rekor(){var T=I.filter(function(x){return!x.kismi}),r=[];
 function en(t,fn,asc,fmt){var s=T.slice().sort(function(a,b){return asc?fn(a)-fn(b):fn(b)-fn(a)})[0];r.push('<div class="ozet"><b>'+t+':</b> '+esc(s.il)+' <small>('+fmt(s)+')</small></div>')}
 en('Tatlı yoğunluğu en yüksek il',function(x){return x.endeks['Fırın & Tatlı']},0,function(x){return f1(x.endeks['Fırın & Tatlı'])+'× TR'});
 en('Kebap/döner payı en yüksek il',function(x){return x.pay['Döner & Kebap']},0,function(x){return '%'+f1(x.pay['Döner & Kebap'])});
 en('Balık payı en yüksek il',function(x){return x.pay['Balık & Deniz Ürünleri']},0,function(x){return '%'+f1(x.pay['Balık & Deniz Ürünleri'])});
 en('En cömert puan veren il',function(x){return x.p},0,function(x){return 'ortanca '+f1(x.p.toFixed(2))});
 en('En zor beğenen il',function(x){return x.p},1,function(x){return 'ortanca '+f1(x.p.toFixed(2))});
 en('En çok yorum yazılan il',function(x){return x.y},0,function(x){return 'ortanca '+x.y+' yorum'});
 $('rek').innerHTML='<div class="kr"><h2>Türkiye\\'nin en\\'leri</h2>'+r.join('')+'<div class="sy">Yalnızca 300+ yeri taranmış iller karşılaştırılır.</div></div>'}
$('rek')&&rekor();
$('il1').onchange=$('il2').onchange=ciz;
var __f=function(s){return String(s).toLocaleLowerCase('tr').replace(/[çğıöşü]/g,function(c){return{'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u'}[c]})};
var qs=new URLSearchParams(location.search),q1=qs.get('il1'),q2=qs.get('il2');
var g=I.findIndex(function(x){return q1?__f(x.il)===__f(q1):x.il==='Gaziantep'});if(g<0)g=I.findIndex(function(x){return x.il==='Gaziantep'});$('il1').value=g>-1?g:0;
if(q2){var g2=I.findIndex(function(x){return __f(x.il)===__f(q2)});if(g2>-1)$('il2').value=g2}ciz();
})();
'''
S=S[:j0]+js+S[j1:]
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
open('dna.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
print(len(iller),'il;',sum(i['kismi'] for i in iller),'kısmi;',kats)
for i in iller[:0]:pass
print(sorted([(i['n'],i['il']) for i in iller])[:8])
