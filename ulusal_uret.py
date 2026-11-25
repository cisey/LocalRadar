"""Türkiye'nin en popüler 100 yeri -> ulusal.html. Çalıştır: python3 ulusal_uret.py  (repo kökünden; local_radar_core yolu aşağıda)"""
import re,json,glob,math,sys,collections,html
sys.path.insert(0,'/home/claude/cisey/local-radar')
import local_radar_core as C
BUY={'Istanbul','Ankara','Izmir'}
GEN=set('restaurant restoran lokantasi lokanta kebap kebab cafe kafe sirkeci sultanahmet pide salonu evi ocakbasi usta ustanin yeri'.split())
def marka(n):
    w=[x for x in re.split(r'[^a-z0-9]+',C._populer_anahtar(n)) if x and x not in GEN]
    return ' '.join(w[:2]) or C._populer_anahtar(n)
rows=[];ilmax={};ad={}
for f in sorted(glob.glob('rehberler/*-Tum-Ilceler.html')):
    il=f.split('/')[-1].replace('-Tum-Ilceler.html','')
    h=open(f,encoding='utf-8').read();i=h.find('const V=')
    try:v=json.JSONDecoder().raw_decode(h[i+8:])[0]
    except Exception:continue
    m=re.search(r'<title>([^<·–-]+)',h);ad[il]=(m.group(1).strip() if m else il)
    L=[]
    for x in v.get('I',[]):
        if x.get('S') not in C.POPULER_KATEGORILER or x.get('u') or not x.get('l'):continue
        try:p=float(str(x['p']).replace(',','.'))
        except:continue
        n=C._PUA.sub('',x.get('n') or '').strip();y=x.get('y') or 0
        if not(0<p<=5) or C._zincir_mi(n) or re.search(r'dinlenme|petrol|avm|otel',C.fold(n+' '+(x.get('t') or ''))):continue
        L.append(dict(il=il,n=n,p=p,y=y,S=x['S'],c=x.get('c') or '',k=marka(n),l=x['l']))
    if len(L)>=50:
        ys=sorted((a['y'] for a in L),reverse=True)
        ilmax[il]=ys[1] if len(ys)>1 and ys[0]>3*ys[1] else ys[0]
        rows+=L
TR=max(ilmax.values());Cm=sum(r['p'] for r in rows)/len(rows)
for r in rows:
    r['G']=(r['y']*r['p']+250*Cm)/(r['y']+250)
    rel=lambda m:min(1,math.log(r['y']+1)/math.log(m+1))
    r['sk']=(0.6*rel(ilmax[r['il']])+0.4*rel(TR))*(r['G']-3.5)
ok=sorted([r for r in rows if 4.2<=r['p']<=5 and r['y']>=150],key=lambda r:-r['sk'])
out=[];ic=collections.Counter();kc=collections.Counter();br=set()
for r in ok:
    if ic[r['il']]>=(5 if r['il'] in BUY else 3) or kc[r['S']]>=20 or r['k'] in br:continue
    out.append(r);ic[r['il']]+=1;kc[r['S']]+=1;br.add(r['k'])
    if len(out)==100:break
eksik=[]
for il in sorted(ilmax,key=lambda a:ad[a]):
    if ic[il]:continue
    c=sorted([r for r in rows if r['il']==il and r['p']>=4.2 and r['y']>=80 and r['k'] not in br],key=lambda r:-r['G'])
    if c:eksik.append(c[0])
def kart(r,i=None):
    return ('<a class="k" href="%s" target="_blank" rel="noopener"><div class="no">%s</div><div class="b"><div class="ad">%s</div>'
     '<div class="alt">%s%s · %s</div><div class="pu"><b>★ %s</b> · %s yorum</div></div></a>')%(
     html.escape(r['l'],True),i or '·',html.escape(r['n']),html.escape(ad[r['il']]),(' / '+html.escape(r['c'])) if r['c'] else '',html.escape(r['S']),
     str(r['p']).replace('.',','),f"{r['y']:,}".replace(',','.'))
ilopt=''.join('<option>%s</option>'%html.escape(a) for a in sorted({ad[r['il']] for r in out}))
katopt=''.join('<option>%s</option>'%html.escape(a) for a in sorted({r['S'] for r in out}))
kartlar=''.join(kart(r,i).replace('<a class="k"','<a class="k" data-il="%s" data-kat="%s"'%(html.escape(ad[r['il']],True),html.escape(r['S'],True)),1) for i,r in enumerate(out,1))
ek=''.join(kart(r) for r in eksik)
T=open('puanlama.html',encoding='utf-8').read()
gt=T[T.find('<!-- Google tag'):T.find('<meta charset')]
page=f'''<!DOCTYPE html>
<html lang="tr"><head>
{gt}<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<title>Türkiye'nin En Popüler 100 Yeri · Local Radar</title>
<style>
:root{{--bg:#0b0f17;--card:rgba(26,32,44,.7);--line:rgba(255,255,255,.08);--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--gold:#fbbf24}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.5;padding-bottom:48px}}
.wrap{{max-width:640px;margin:0 auto;padding:16px}}
.back{{display:inline-block;color:var(--muted);text-decoration:none;font-size:13px;background:rgba(255,255,255,.05);padding:6px 12px;border-radius:20px;border:1px solid var(--line);margin-bottom:14px}}
h1{{font-size:24px;font-weight:800;line-height:1.25;margin-bottom:6px}}h2{{font-size:17px;font-weight:800;margin:26px 0 8px;color:var(--gold)}}
p{{color:#cbd5e1;font-size:14px;margin:8px 0}}.fl{{display:flex;gap:8px;margin:14px 0}}
select{{flex:1;min-width:0;background:#1a202c;color:var(--text);border:1px solid var(--line);border-radius:12px;padding:10px;font-size:14px}}
.k{{display:flex;gap:12px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;margin:8px 0;text-decoration:none;color:inherit}}
.no{{min-width:34px;text-align:center;font-weight:800;font-size:16px;color:var(--gold)}}.ad{{font-weight:700;font-size:15px}}
.alt{{color:var(--muted);font-size:12.5px}}.pu{{font-size:13px;color:#cbd5e1;margin-top:2px}}.pu b{{color:var(--gold)}}
.not{{font-size:12.5px;color:var(--muted);background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:12px 0}}.not a{{color:var(--accent)}}
</style></head><body><div class="wrap">
<a class="back" href="index.html">← Ana sayfa</a>
<h1>🏆 Türkiye'nin En Popüler 100 Yeri</h1>
<p>Hem çok yorum alan hem yüksek puanlı, zincir olmayan yerler. Yorum sayısı il ölçeğine göre dengelenir; bu yüzden küçük illerin klasikleri de listeye girebilir.</p>
<div class="fl"><select id="il"><option value="">Tüm iller</option>{ilopt}</select><select id="kat"><option value="">Tüm kategoriler</option>{katopt}</select></div>
<div id="liste">{kartlar}</div>
<h2>📍 Listede yeri olmayan illerin en iyisi</h2>
<p>Bu illerde 150 yorum ve 4,2 puanı birlikte geçen yer ya çok az ya da yok. Burada eşik 80 yoruma indirildi.</p>
{ek}
<div class="not">Skorlar il ölçeğine göre dengelenmiştir; son tarama verisini yansıtır, taranmamış ilçeleri kapsamaz. Kuralların ayrıntısı için <a href="puanlama.html">Puanlama nasıl çalışır?</a> sayfasına bakın. Büyükşehirler (İstanbul, Ankara, İzmir) en fazla 5, diğer iller en fazla 3 yerle yer alır. Kategori başına en fazla 20 yer, marka başına 1 şube.</div>
</div><script>
var il=document.getElementById('il'),kat=document.getElementById('kat');
function f(){{document.querySelectorAll('#liste .k').forEach(function(e){{e.style.display=((!il.value||e.dataset.il==il.value)&&(!kat.value||e.dataset.kat==kat.value))?'':'none'}})}}
il.onchange=kat.onchange=f;
</script></body></html>'''
open('ulusal.html','w',encoding='utf-8').write(page)
print(len(out),'liste',len(ic),'il',len(eksik),'eksik il ek',len(page)//1024,'KB')
for i,r in enumerate(out[:12],1):print(i,r['n'],r['il'],r['c'])
print([ (r['n'],ad[r['il']]) for r in eksik[:6]])
