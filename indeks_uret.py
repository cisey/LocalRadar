import json,os,re,sys
KLASOR=sys.argv[1] if len(sys.argv)>1 else 'rehberler'
OUT=sys.argv[2] if len(sys.argv)>2 else 'rehber_indeks.json'
AR=re.compile(r'[؀-ۿ]')
def pid(l):
    m=re.search(r'!1s([^!]+)',l or ''); return m.group(1) if m else l
def load(p):
    t=open(p,encoding='utf-8').read()
    i=t.find('const V='); j=t.find(',O=V.O',i)
    if i<0 or j<0: return []
    return [x for x in json.loads(t[i+8:j]).get('I',[]) if x.get('e') is not None and x.get('b') is not None and not x.get('u')]
dos={};
for f in sorted(os.listdir(KLASOR)):
    if not f.lower().endswith(('.html','.htm')): continue
    if re.match(r'^(index|harita|yakinimda|puanlama|bolge)\.html?$',f,re.I): continue
    dos[f]=load(os.path.join(KLASOR,f))
tum={f for f in dos if re.search(r'-Tum-Ilceler',f,re.I)}
bireysel=set()
for f,I in dos.items():
    if f not in tum: bireysel|={pid(x['l']) for x in I}
sonuc=[];ar=0
for f,I in dos.items():
    if not I: continue
    lat=[x['e'] for x in I]; lon=[x['b'] for x in I]
    kap=1.0
    if f in tum:
        ids=[pid(x['l']) for x in I]; kap=sum(i in bireysel for i in ids)/len(ids)
    ar+=sum(bool(AR.search(x['n'])) for x in I)
    try:
        _h=open(os.path.join(KLASOR,f),encoding='utf-8').read(4000)
        _m=re.search(r'<title>([^<]*?)\s*(?:·|$)',_h); ad=_m.group(1).strip() if _m else f
    except Exception: ad=f
    sonuc.append({'f':f,'ad':ad,'n':len(I),'b':[round(min(lat),4),round(min(lon),4),round(max(lat),4),round(max(lon),4)],
                  'k':os.path.getsize(os.path.join(KLASOR,f))//1024,'t':1 if f in tum else 0,'kap':round(kap,3)})
json.dump(sonuc,open(OUT,'w'),ensure_ascii=False,separators=(',',':'))
tm=[s for s in sonuc if s['t']]
print('dosya',len(sonuc),'tum',len(tm),'kapsanmayan tum:',[(s['f'],s['kap']) for s in tm if s['kap']<0.98])
print('arapca isimli kayit',ar)
