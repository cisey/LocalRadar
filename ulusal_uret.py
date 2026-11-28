"""Türkiye'nin En Popüler 100 Yeri -> ulusal.html (2 sekme: Türkiye Seçkisi + 81 İlin Zirvesi).
Çalıştır (repo kökünden): python3 ulusal_uret.py   Gerekli: local_radar_core.py (local-radar deposu)."""
import re,json,glob,math,sys,collections
import os
for _d in ('/home/claude/cisey/local-radar','C:/Users/Kahveci/projeler/local-radar'):
    if os.path.isdir(_d):sys.path.insert(0,_d)
import local_radar_core as C
BUY={'İstanbul','Ankara','İzmir'};KOTA_BUY,KOTA_DIGER,KOTA_KAT,TOPLAM=5,3,20,100
MIN_P,MIN_Y,YEDEK_Y=4.2,150,80
DUZ={'Adiyaman':'Adıyaman','Agri':'Ağrı','Aydin':'Aydın','Balikesir':'Balıkesir','Bartin':'Bartın','Bingol':'Bingöl','Canakkale':'Çanakkale','Cankiri':'Çankırı','Corum':'Çorum','Diyarbakir':'Diyarbakır','Duzce':'Düzce','Elazig':'Elazığ','Eskisehir':'Eskişehir','Gumushane':'Gümüşhane','Igdir':'Iğdır','Istanbul':'İstanbul','Izmir':'İzmir','Kahramanmaras':'Kahramanmaraş','Karabuk':'Karabük','Kirikkale':'Kırıkkale','Kirklareli':'Kırklareli','Kirsehir':'Kırşehir','Kutahya':'Kütahya','Mugla':'Muğla','Mus':'Muş','Nevsehir':'Nevşehir','Nigde':'Niğde','Sanliurfa':'Şanlıurfa','Sirnak':'Şırnak','Tekirdag':'Tekirdağ','Usak':'Uşak','Mardin':'Mardin','Antalya':'Antalya','Eskişehir':'Eskişehir','Afyonkarahisar':'Afyonkarahisar','Karaman':'Karaman','Kilis':'Kilis','Osmaniye':'Osmaniye','Hakkari':'Hakkâri','Hakkari':'Hakkâri'}
KARA_AD=re.compile(r'(?<![a-z])(bungalov|glamping|truzim|oksijen|allahuekber|din\W*tes|tahin|armada|kentpark|cepa|panora|ankamall|pazari|cicekci|cicekcilik|hediyelik|rafting|binicilik|termal|dinlenme|petrol|akaryakit|avm|otel|oteli|hotel)(?![a-z])')
KARA_TUR=re.compile(r'bayi|bakkal|peynirci|alisveris|oyun salonu|kamp|nargile|dugun|otel|pansiyon|konaklama|termal|hediyelik|cicek|rafting|binicilik|turizm|market|tesis|bungalow|plaj|havuz|lounge bar|gece kulubu')
YEMEK_TUR=re.compile(r'restoran|lokanta|kebap|pide|kafe|cafe|kahvalti|firin|pastane|tatli|balik|kofte|et yemek|corba|kafeterya')
ALKOL=re.compile(r'(?<![a-z])bar(?![a-z])|(restaurant|restoran|cafe|kafe|lounge|gastro|pub)\s*(&|ve)?\s*bar(?![a-z])|(?<![a-z])(meyhane|meyhanesi|pub|birahane|biraci|taverna|tavern|brewery|brewhouse|cocktails?|kokteyl(?:ler)?|wine|sarap|sarapci|rakici|gece kulubu|nightclub|night club)(?![a-z])')
HARIC=re.compile(r'(?<![a-z])(gezi evi|nostalji gezi)(?![a-z])')   # yemek mekanı olmayanlar (elle eklenir)
ZINCIR_EK=re.compile(r'(?<![a-z])(oses|cigkoftem|espressolab|burger yiyelim)(?![a-z])')
def kara(n,t):
    fa=C.fold(n);ft=C.fold(t)
    if HARIC.search(fa):return True
    if KARA_AD.search(fa) or ALKOL.search(fa) or ZINCIR_EK.search(fa):return True
    return bool(KARA_TUR.search(ft)) and not YEMEK_TUR.search(ft)
def temiz(n):
    n=re.split(r'\s*[|\[(]\s*',n)[0]
    m=re.split(r'\s+[-–]\s+',n)
    if len(m)>1 and len(m[0])>=3:n=m[0]
    if len(n)>30 and ',' in n:n=n.split(',')[0]
    return n.replace('_',' ').strip(' ,-')
GEN=set('restaurant restoran lokantasi lokanta kebap kebab cafe kafe sirkeci sultanahmet pide salonu evi ocakbasi usta ustanin yeri'.split())
def marka(n):
    w=[x for x in re.split(r'[^a-z0-9]+',C._populer_anahtar(n)) if x and x not in GEN]
    return ' '.join(w[:2]) or C._populer_anahtar(n)
rows=[];ilmax={};ad={};elenen=[]
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=os.path.basename(f).replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();i=h.find('const V=')
    try:v=json.JSONDecoder().raw_decode(h[i+8:])[0]
    except Exception:continue
    m=re.search(r'<title>([^<·–-]+)',h);a=(m.group(1).strip() if m else il);ad[il]=DUZ.get(a,DUZ.get(il,a))
    L=[]
    for x in v.get('I',[]):
        if x.get('S') not in C.POPULER_KATEGORILER or x.get('u') or not x.get('l'):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        n0=C._PUA.sub('',x.get('n') or '').strip();t=C._PUA.sub('',x.get('t') or '');y=x.get('y') or 0
        if not(0<p<=5) or C._zincir_mi(n0) or re.search(r'dinlenme|petrol|avm|otel',C.fold(n0+' '+t)):continue
        if kara(n0,t):
            if p>=MIN_P and y>=MIN_Y:elenen.append('%s | %s | %s | %s yorum | %s'%(n0,ad[il],t,y,p))
            continue
        L.append(dict(il=il,n=temiz(n0),p=p,y=y,S=x['S'],c=x.get('c') or '',k=marka(n0),l=x['l'],e=x.get('e'),b=x.get('b')))
    if L:
        ys=sorted((a['y'] for a in L),reverse=True)
        ilmax[il]=ys[1] if len(ys)>1 and ys[0]>3*ys[1] else ys[0]
        rows+=L
TR=max(ilmax.values());Cm=sum(r['p'] for r in rows)/len(rows)
for r in rows:
    r['G']=(r['y']*r['p']+250*Cm)/(r['y']+250)
    rel=lambda m:min(1,math.log(r['y']+1)/math.log(m+1))
    r['sk']=(0.6*rel(ilmax[r['il']])+0.4*rel(TR))*(r['G']-3.5)
ok=sorted([r for r in rows if MIN_P<=r['p']<=5 and r['y']>=MIN_Y],key=lambda r:-r['sk'])
out=[];ic=collections.Counter();kc=collections.Counter();br=set()
for r in ok:
    if ic[ad[r['il']]]>=(KOTA_BUY if ad[r['il']] in BUY else KOTA_DIGER) or kc[r['S']]>=KOTA_KAT or r['k'] in br:continue
    out.append(r);ic[ad[r['il']]]+=1;kc[r['S']]+=1;br.add(r['k'])
    if len(out)==TOPLAM:break
def o(r,et=''):
    return dict(ad=r['n'],il=ad[r['il']],ilce=r['c'] or 'Merkez',kat=r['S'],puan=r['p'],yorum=r['y'],link=r['l'],etiket=et)
secki=[o(r) for r in out]
PLAKA={C.fold(n):'{:02d}'.format(i+1) for i,n in enumerate(['Adana', 'Adıyaman', 'Afyonkarahisar', 'Ağrı', 'Amasya', 'Ankara', 'Antalya', 'Artvin', 'Aydın', 'Balıkesir', 'Bilecik', 'Bingöl', 'Bitlis', 'Bolu', 'Burdur', 'Bursa', 'Çanakkale', 'Çankırı', 'Çorum', 'Denizli', 'Diyarbakır', 'Edirne', 'Elazığ', 'Erzincan', 'Erzurum', 'Eskişehir', 'Gaziantep', 'Giresun', 'Gümüşhane', 'Hakkâri', 'Hatay', 'Isparta', 'Mersin', 'İstanbul', 'İzmir', 'Kars', 'Kastamonu', 'Kayseri', 'Kırklareli', 'Kırşehir', 'Kocaeli', 'Konya', 'Kütahya', 'Malatya', 'Manisa', 'Kahramanmaraş', 'Mardin', 'Muğla', 'Muş', 'Nevşehir', 'Niğde', 'Ordu', 'Rize', 'Sakarya', 'Samsun', 'Siirt', 'Sinop', 'Sivas', 'Tekirdağ', 'Tokat', 'Trabzon', 'Tunceli', 'Şanlıurfa', 'Uşak', 'Van', 'Yozgat', 'Zonguldak', 'Aksaray', 'Bayburt', 'Karaman', 'Kırıkkale', 'Batman', 'Şırnak', 'Bartın', 'Ardahan', 'Iğdır', 'Yalova', 'Karabük', 'Kilis', 'Osmaniye', 'Düzce'])}
zirve=[]
for il in sorted(ilmax,key=lambda a:ad[a].replace('İ','I').lower()):
    L=[r for r in rows if r['il']==il];n=len(L)
    for (mp,my,ek) in ((MIN_P,MIN_Y,''),(MIN_P,YEDEK_Y,' · 80+ yorum'),(4.0,30,' · az yorumlu')):
        c=[r for r in L if r['p']>=mp and r['y']>=my]
        if c:break
    else:c=L;ek=' · az yorumlu'
    z=o(max(c,key=lambda r:r['sk']),'{:,} yerden #1'.format(n).replace(',','.')+ek);z['plaka']=PLAKA.get(C.fold(ad[il]),'');zirve.append(z)
veri=json.dumps(dict(secki=secki,zirve=zirve),ensure_ascii=False,separators=(',',':'))
T=open('puanlama.html',encoding='utf-8').read();gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
S=open('ulusal_sablon.html',encoding='utf-8').read()
open('ulusal.html','w',encoding='utf-8').write(S.replace('__GTAG__',gt).replace('__VERI__',veri))
open('ulusal_elenenler.txt','w',encoding='utf-8').write('\n'.join(sorted(set(elenen))))
print(len(secki),'seçki',len(ic),'il;',len(zirve),'il zirve;',len(elenen),'kara listeye takılan aday')
print(collections.Counter(z['etiket'] for z in zirve))
print([ (s['ad'],s['il']) for s in secki[:10]])
