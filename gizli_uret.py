"""Gizli Cevherler -> gizli.html. ulusal_uret.py'nin veri yükleme/temizleme kısmını yeniden kullanır. Repo kökünden: python3 gizli_uret.py"""
import re,json,collections,statistics
src=open('ulusal_uret.py',encoding='utf-8').read();exec(src[:src.index('TR=max(')])
MIN_P,FARK,TOP=4.5,0.3,100
by=collections.defaultdict(list)
for r in rows:by[r['il']].append(r)
adaylar=[]
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
        g=(r['y']*r['p']+100*ort)/(r['y']+100)
        if g-ort>=FARK:adaylar.append((g-ort,r,ort))
adaylar.sort(key=lambda a:-a[0])
out=[];ic=collections.Counter();kc=collections.Counter();br=set()
for f,r,ort in adaylar:
    a=ad[r['il']]
    if ic[a]>=(5 if a in BUY else 3) or kc[r['S']]>=20 or r['k'] in br:continue
    out.append(dict(ad=r['n'],il=a,ilce=r['c'] or 'Merkez',kat=r['S'],puan=r['p'],yorum=r['y'],link=r['l'],etiket='İl ort. +%s'%('%.1f'%f).replace('.',',')))
    ic[a]+=1;kc[r['S']]+=1;br.add(r['k'])
    if len(out)==TOP:break
veri=json.dumps(dict(secki=out,zirve=[]),ensure_ascii=False,separators=(',',':'))
S=open('ulusal_sablon.html',encoding='utf-8').read()
S=re.sub(r'<div class="sek">.*?</div>\n','',S,flags=re.S)
S=S.replace("$('t1').onclick=function(){sek('secki')};$('t2').onclick=function(){sek('zirve')};","")
S=S.replace("$('t1').classList.toggle('a',x==='secki');$('t2').classList.toggle('a',x==='zirve');","")
S=re.sub(r"\$\('ac'\)\.textContent=x==='secki'\?'[^']*':'[^']*';","$('ac').textContent='Herkesin bildiği yerler değil: yorumu azdan ortaya, ama puanı kendi ilinin ortalamasının belirgin üstünde olan yerler.';",S)
S=S.replace("Türkiye'nin En Popüler Yerleri · Local Radar","Gizli Cevherler · Local Radar").replace("🏆 Türkiye'nin En Popüler Yerleri","💎 Gizli Cevherler")
a=S.index('<div class="not">');b=S.index('</div>',a)+6
S=S[:a]+'''<div class="not"><b>Nasıl seçildi?</b><br>Zincirler, kapanmış yerler, alkollü mekanlar ve yemek dışı işletmeler baştan çıkarılır. Yorumu en az 100 (küçük illerde 60) olan, puanı en az 4,5 olan yerler değerlendirilir. İlin en çok yorum alan %15'lik dilimi (herkesin bildiği yerler) ve 500'den fazla yorumlu olanlar dışarıda tutulur; yorumu 100'ün altındaki tam 5,0 puanlılar da elenir. Kalanlar, az yorumlu yerin puanını il ortalamasına doğru çeken Güvenilir Skor'un <b>il ortalamasından farkına</b> göre sıralanır (en az +0,3 fark). Büyükşehirlerden en fazla 5, diğer illerden en fazla 3 yer, kategori başına en fazla 20 yer, marka başına 1 şube girer. Veri son taramayı yansıtır; az yorumlu yerler daha kolay kapanabilir, gitmeden önce Haritalar'dan kontrol edin. Ayrıntılar: <a href="puanlama.html">Puanlama nasıl çalışır?</a></div>'''+S[b:]
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
open('gizli.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
print(len(adaylar),'aday;',len(out),'liste;',len(ic),'il')
for i,x in enumerate(out[:15],1):print(i,x['ad'],'|',x['il'],'|',x['puan'],x['yorum'],x['kat'],x['etiket'])
print(kc.most_common(4),ic.most_common(4))
