"""local_radar_core.py'ye 'alkollü mekan + yemek dışı tür' ayıklamasını ekler. Bilgisayarda:
   python3 pc_yama_alkol.py C:\\yol\\local_radar_core.py      (yedeğini .bak olarak alır; iki kez çalıştırsan zarar vermez)
Sonra programdan rehberleri yeniden üret (yemek_disi_temizle devreye girer) ve yeni HTML'leri repoya yükle."""
import sys,shutil
yol=sys.argv[1];s=open(yol,encoding='utf-8').read()
if 'ALKOL_AD' in s:raise SystemExit('Yama zaten uygulanmış.')
shutil.copy(yol,yol+'.bak')
a='''r"danisman|egitim merkezi|parti planlay|organizasyon|toptanci")'''
b='''r"danisman|egitim merkezi|parti planlay|organizasyon|toptanci|"
                             r"bayi|bakkal|peynirci|alisveris|oyun salonu|nargile salonu|kamp alani|dugun salonu|konaklama|"
                             r"termal|hediyelik|cicekci|rafting|binicilik|plaj kulubu|gece kulubu")
ALKOL_AD = re.compile(r"(?<![a-z])(meyhane|meyhanesi|pub|birahane|biraci|taverna|tavern|brewery|brewhouse|cocktail|"
                      r"kokteyl|wine|sarap|sarapci|rakici|gece kulubu|nightclub|night club)(?![a-z])")'''
assert a in s;s=s.replace(a,b,1)
a='''def yemek_disi_mi(tur):
    """Google türü yemek dışı bir işletmeyi gösteriyorsa True (Kahve/Şarküteri/Mangal mağazası ELENMEZ)."""
    return bool(_YEMEK_DISI_TUR.search(fold(tur or "")))'''
b='''def yemek_disi_mi(tur, ad=""):
    """Google türü yemek dışı bir işletmeyi ya da adı alkollü mekanı (meyhane, pub...) gösteriyorsa True
    (Kahve/Şarküteri/Mangal mağazası ELENMEZ; 'sıra gecesi' mekanları kalır)."""
    return bool(_YEMEK_DISI_TUR.search(fold(tur or "")) or ALKOL_AD.search(fold(ad or "")))'''
assert a in s;s=s.replace(a,b,1)
a='yeni = [x for x in eski if not yemek_disi_mi(x.get("t", ""))]'
b='yeni = [x for x in eski if not yemek_disi_mi(x.get("t", ""), x.get("n", ""))]'
assert a in s;s=s.replace(a,b,1)
open(yol,'w',encoding='utf-8').write(s);print('Yama uygulandı. Yedek:',yol+'.bak')
