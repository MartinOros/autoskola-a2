# Parser PDF "Otázky A2" -> public/questions.json + public/img/*.jpg
# Vektorová geometria tabuliek v PDF je poškodená; spoľahlivé sú obrázky pozadia riadkov
# (celá šírka strany) - každé číslo otázky leží presne v jednom. Z nich sa berú riadky.
import fitz, re, json, os, shutil, statistics, io
from PIL import Image, ImageChops
SRC='/Users/martinoros/Downloads/Otazky_A2_so_spravnymi_odpovedami.pdf'
d=fitz.open(SRC)
shutil.rmtree('public/img',ignore_errors=True); os.makedirs('public/img')
CATS=["Pravidlá cestnej premávky","Uplatňovanie pravidiel prednosti v jazde a rýchlostné obmedzenia","Dopravné značky a dopravné zariadenia","Dopravné situácie na križovatkách","Všeobecné pravidlá správania sa v prípade dopravnej nehody","Teória vedenia vozidla","Predpisy týkajúce sa dokladov požadovaných v premávke vozidla","Podmienky prevádzky vozidiel v premávke na pozemných komunikáciách","Zásady bezpečnej jazdy","Konštrukcia vozidiel a ich údržba"]
SQ=lambda s:re.sub(r'\s+','',s)
def clean(s): return re.sub(r'\s+',' ',(s or '')).strip()
def catof(t):
    t=SQ(t); m=re.match(r'^(\d+)\.(.*)',t)
    if m and 1<=int(m.group(1))<=10 and m.group(2)[:15]==SQ(CATS[int(m.group(1))-1])[:15]: return int(m.group(1))
DPI=170
def image_in(p,rect,textrects):
    """Vyreže obrázok z bunky: vyrenderuje bunku, text prefarbí na pozadie, oreže na obsah."""
    if rect.width<5 or rect.height<5: return None
    pix=p.get_pixmap(clip=rect,dpi=DPI)
    im=Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    sc=DPI/72; bgc=max(im.getcolors(1<<24))[1]
    from PIL import ImageDraw
    m=im.copy(); dr=ImageDraw.Draw(m)
    for t in textrects:
        dr.rectangle([(t.x0-rect.x0)*sc-2,(t.y0-rect.y0)*sc-2,(t.x1-rect.x0)*sc+2,(t.y1-rect.y0)*sc+2],fill=bgc)
    # okraje bunky (mriežka) ignoruj
    dr.rectangle([0,0,m.width,4],fill=bgc); dr.rectangle([0,m.height-5,m.width,m.height],fill=bgc)
    dr.rectangle([0,0,4,m.height],fill=bgc); dr.rectangle([m.width-5,0,m.width,m.height],fill=bgc)
    diff=ImageChops.difference(m,Image.new('RGB',m.size,bgc)).convert('L').point(lambda v:255 if v>40 else 0)
    bb=diff.getbbox()
    if not bb: return None
    w,h=bb[2]-bb[0],bb[3]-bb[1]
    if not ((w>=12 and h>=40) or (w>=40 and h>=25)): return None
    out=im.crop((max(0,bb[0]-4),max(0,bb[1]-4),min(im.width,bb[2]+4),min(im.height,bb[3]+4)))
    # podfarbenie riadku tabuľky (svetlomodré pruhy) -> biela, aby mali všetky obrázky rovnaký podklad
    if bgc!=(255,255,255):
        near=ImageChops.difference(out,Image.new('RGB',out.size,bgc)).convert('L').point(lambda v:255 if v<14 else 0)
        out.paste((255,255,255),mask=near)
    return out
qs=[]; cat=0; nimg=0
for pn,p in enumerate(d):
    xs=[[],[],[]]
    for t in p.find_tables().tables:
        for r in t.rows:
            if len(r.cells)>=4 and all(r.cells[:4]):
                for k in range(3): xs[k].append(r.cells[k+1][0])
    lines=[]
    for b in p.get_text('dict')['blocks']:
        if b['type']==0:
            for l in b['lines']:
                t=''.join(s['text'] for s in l['spans'])
                if t.strip(): lines.append((fitz.Rect(l['bbox']),t))
    bgs=sorted({tuple(round(x,1) for x in i['bbox']) for i in p.get_image_info() if i['bbox'][2]-i['bbox'][0]>480},key=lambda b:b[1])
    bgs=[fitz.Rect(b)&p.rect for b in bgs]
    # nadpisy mimo tabuľky (napr. na vrchu strany)
    events=[(l[0].y0,'line',l) for l in lines if catof(l[1])]
    for b in bgs: events.append((b.y0,'row',b))
    if not xs[0]:
        for e in sorted(events,key=lambda e:e[0]):
            if e[1]=='line': cat=catof(e[2][1])
        continue
    X1,X2,X3=(statistics.median(v) for v in xs)
    for y,kind,obj in sorted(events,key=lambda e:e[0]):
        if kind=='line': cat=catof(obj[1]); continue
        row=obj
        inrow=[l for l in lines if row.contains(fitz.Point((l[0].x0+l[0].x1)/2,(l[0].y0+l[0].y1)/2))]
        full=' '.join(t for _,t in sorted(inrow,key=lambda l:(l[0].y0,l[0].x0)))
        c=catof(full)
        if c: cat=c; continue
        col=lambda lo,hi:[l for l in inrow if lo-2<=(l[0].x0+l[0].x1)/2<hi]
        cn,cq,ca,cg=col(0,X1),col(X1,X2),col(X2,X3),col(X3,9999)
        txt=lambda ls:clean(' '.join(t for _,t in sorted(ls,key=lambda l:(round(l[0].y0),l[0].x0))))
        num=txt(cn)
        if any(h in txt(cq) for h in ('znenie otázky',)): continue
        if not re.match(r'^\d+\.$',num):
            if not num and qs and (cq or ca):   # pokračovanie riadku z predošlej strany
                qs[-1]['q']=clean(qs[-1]['q']+' '+txt(cq)); qs[-1]['a']=clean(qs[-1]['a']+' '+txt(ca))
            continue
        n=int(num[:-1])
        g=clean(re.sub(r'\b\d+\.','',txt(cg))).strip(', ')
        def crop(lo,hi,ls,suffix):
            global nimg
            im=image_in(p,fitz.Rect(lo,row.y0,hi,row.y1),[l[0] for l in ls])
            if im is None: return None
            fn=f'c{cat}-{n}{suffix}.jpg'; im.save('public/img/'+fn,quality=82); nimg+=1
            return fn
        qs.append(dict(id=f'{cat}-{n}',cat=cat,n=n,q=txt(cq),a=txt(ca),g=g,qi=crop(X1,X2,cq,''),ai=crop(X2,X3,ca,'a'),page=pn+1))
open('public/questions.js','w').write('window.QDATA='+json.dumps(dict(cats=CATS,qs=qs),ensure_ascii=False,separators=(',',':'))+';\n')
from collections import Counter
print(len(qs),'img',nimg,sorted(Counter(q['cat'] for q in qs).items()))
print('qi',sorted(Counter(q['cat'] for q in qs if q['qi']).items()),'ai',sum(1 for q in qs if q['ai']))
print('groups',Counter(q['g'] for q in qs))
print('dups',[k for k,v in Counter(q['id'] for q in qs).items() if v>1])
for q in qs:
    if not q['q'] or not q['a']: print('EMPTY',q)
