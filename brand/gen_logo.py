# Generates the Elastic Endeavors "straddle E" mark: stem=hips, top/bottom bars=legs,
# middle bar=torso reaching forward, round head at its end. Run from repo root.
from PIL import Image, ImageDraw, ImageFont
A,B,BG=(0x7c,0xf0,0xd0),(0x9a,0x7c,0xff),(7,8,11)
W=9  # bold stroke on a 64 grid
BARS=[(13,13,22,51),(13,13,47,22),(13,42,47,51),(13,27.5,38,36.5)]  # stem, legs, torso
HEAD=(47,32,6.5)
def svg():
    r=W/2; bars="".join(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" rx="{r}"/>' for x0,y0,x1,y1 in BARS)
    cx,cy,hr=HEAD
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="#7cf0d0"/><stop offset="1" stop-color="#9a7cff"/></linearGradient></defs><rect width="64" height="64" rx="14" fill="#07080b"/>'
      f'<g fill="url(#g)">{bars}<circle cx="{cx}" cy="{cy}" r="{hr}"/></g></svg>')
def grad(n):
    g=Image.new("RGB",(n,n)); px=g.load()
    for y in range(n):
        for x in range(n):
            t=(x+y)/(2*n-2); px[x,y]=tuple(int(A[i]+(B[i]-A[i])*t) for i in range(3))
    return g
def mark(n,bg_round=True):
    S=8; N=n*S; k=N/64
    m=Image.new("L",(N,N)); d=ImageDraw.Draw(m)
    for x0,y0,x1,y1 in BARS: d.rounded_rectangle([x0*k,y0*k,x1*k,y1*k],radius=W/2*k,fill=255)
    cx,cy,hr=HEAD; d.ellipse([(cx-hr)*k,(cy-hr)*k,(cx+hr)*k,(cy+hr)*k],fill=255)
    bm=Image.new("L",(N,N)); ImageDraw.Draw(bm).rounded_rectangle([0,0,N-1,N-1],radius=(14*k if bg_round else 0),fill=255)
    img=Image.new("RGBA",(N,N),(0,0,0,0)); img.paste(Image.new("RGB",(N,N),BG),mask=bm)
    img.paste(grad(N//4).resize((N,N)),mask=m)
    return img.resize((n,n),Image.LANCZOS)
if __name__=="__main__":
    s=svg(); open("favicon.svg","w").write(s); open("brand/mark.svg","w").write(s)
    mark(256).save("favicon.ico",sizes=[(16,16),(32,32),(48,48),(64,64)])
    mark(180,False).convert("RGB").save("apple-touch-icon.png")
    mark(192).save("brand/icon-192.png"); mark(512).save("brand/icon-512.png")
    og=Image.new("RGB",(1200,630),BG); m=mark(280); og.paste(m,(120,175),m)
    fp="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try: f=ImageFont.truetype(fp,64); f2=ImageFont.truetype(fp.replace("-Bold",""),30)
    except Exception: f=f2=ImageFont.load_default()
    d=ImageDraw.Draw(og); d.text((450,240),"ELASTIC ENDEAVORS",font=f,fill=(240,242,245))
    d.text((452,330),"Deep tech x consumer.",font=f2,fill=(150,155,165))
    og.save("brand/og.png")
    mark(16).resize((128,128),Image.NEAREST).save("/tmp/logo/check16.png")
