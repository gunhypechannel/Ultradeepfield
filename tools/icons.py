import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
out=sys.argv[1]
def make(N, pad=0.0, bgfull=True):
    S=N*4
    im=Image.new("RGB",(S,S),(5,9,15))
    d=ImageDraw.Draw(im)
    # radial glow
    glow=Image.new("RGB",(S,S),(0,0,0)); g=ImageDraw.Draw(glow)
    for r in range(int(S*.75),0,-6):
        t=r/(S*.75); c=(int(15+30*(1-t)),int(34+70*(1-t)),int(48+90*(1-t)))
        g.ellipse([S/2-r,S/2-r,S/2+r,S/2+r],fill=c)
    im=Image.blend(im,glow,.85); d=ImageDraw.Draw(im)
    rnd=random.Random(7)
    for _ in range(int(S*S/9000)):
        x,y=rnd.random()*S,rnd.random()*S; r=rnd.choice([1,1,1,1,2])*S/900
        b=rnd.randint(120,255); d.ellipse([x-r,y-r,x+r,y+r],fill=(b,b,min(255,b+20)))
    # spiral galaxy
    gal=Image.new("RGBA",(S,S),(0,0,0,0)); gd=ImageDraw.Draw(gal)
    sc=S*(1-2*pad)/2
    for arm in range(2):
        for i in range(4200):
            t=i/4200; a=arm*math.pi+t*3.0*math.pi; rr=t*sc*.98
            x=S/2+math.cos(a)*rr+rnd.gauss(0,sc*.035*(.4+t)); y=S/2+math.sin(a)*rr*.62+rnd.gauss(0,sc*.03*(.4+t))
            col=(85,214,232) if rnd.random()<.6 else (255,211,107)
            rad=S/220*(1.6-t); al=int(200*(1-t*.7))
            gd.ellipse([x-rad,y-rad,x+rad,y+rad],fill=col+(al,))
    gal=gal.filter(ImageFilter.GaussianBlur(S/400))
    im=im.convert("RGBA"); im.alpha_composite(gal)
    core=Image.new("RGBA",(S,S),(0,0,0,0)); cd=ImageDraw.Draw(core)
    for r in range(int(sc*.28),0,-2):
        t=r/(sc*.28); cd.ellipse([S/2-r,S/2-r*.7,S/2+r,S/2+r*.7],fill=(255,240,200,int(255*(1-t)**1.6)))
    im.alpha_composite(core.filter(ImageFilter.GaussianBlur(S/120)))
    # ring frame
    fr=ImageDraw.Draw(im)
    if not bgfull:
        pass
    return im.convert("RGB").resize((N,N),Image.LANCZOS)
make(512).save(f"{out}/icon-512.png")
make(192).save(f"{out}/icon-192.png")
make(180).save(f"{out}/apple-touch-icon.png")
make(512,pad=.12).save(f"{out}/icon-maskable-512.png")
make(32).save(f"{out}/favicon-32.png")
print("ok")
