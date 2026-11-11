# Renders docs/music_conv.mp3 (the Convergence theme) from docs/music.mp3: run in a folder holding songst.wav (ffmpeg -i docs/music.mp3 -ar 44100 -ac 2 songst.wav), then
# ffmpeg -i conv_raw.wav -af "acompressor=threshold=-16dB:ratio=3:attack=15:release=250:makeup=2,loudnorm=I=-10:TP=-1:LRA=8" -c:a libmp3lame -b:a 128k music_conv.mp3
import numpy as np, scipy.io.wavfile as w, scipy.signal as sg, sys
sr,x=w.read('songst.wav'); x=x.astype(np.float32)/32768
K=0.84                      # play at 84% speed: 3 semitones deeper, slower
A0,A1=58.0,178.0            # the loud part of the song, after the build
seg=x[int(A0*sr):int(A1*sr)]
# deepen: resample so it plays slower and lower (like asetrate)
n_out=int(len(seg)/K); seg=sg.resample_poly(seg, 100, 84, axis=0).astype(np.float32)
L=len(seg); T=L/sr; t=np.arange(L)/sr; rng=np.random.default_rng(7)
# low band onsets of the slowed song (kick) to time hits
b,a=sg.butter(4,140/(sr/2)); lo=sg.filtfilt(b,a,seg.mean(1)); env=np.abs(sg.hilbert(lo)); hop=256; e=sg.medfilt(env[::hop],5); fps=sr/hop
d=np.maximum(0,np.diff(e)); pk,_=sg.find_peaks(d,height=np.percentile(d,97),distance=int(fps*.35)); kicks=pk/fps
print('kicks',len(kicks), np.round(np.diff(kicks)[:20],2))
out=seg.copy()*0.9
# reverb: a long dark hall
ir_n=int(3.8*sr); it=np.arange(ir_n)/sr; irs=[]
for ch in range(2):
    nz=rng.standard_normal(ir_n).astype(np.float32)*np.exp(-it/1.05)
    bb,aa=sg.butter(2,3800/(sr/2)); nz=sg.lfilter(bb,aa,nz); nz[:int(.02*sr)]*=np.linspace(0,1,int(.02*sr)); irs.append(nz/np.sqrt((nz**2).sum()))
wet=np.stack([sg.fftconvolve(seg[:,c],irs[c])[:L] for c in range(2)],1)
out+=wet*0.55
mt=lambda m:440*2**((m-69)/12)
root=66-3-24                # the song's A drops to F#: F#1 = midi 30
# sub drone: F#1 + F#2 + C#3, slow breathing swell
dr=np.zeros(L,np.float32)
for m,v in [(root,.22),(root+12,.10),(root+19,.05)]:
    ph=2*np.pi*mt(m)*t+0.3*np.sin(2*np.pi*.07*t); dr+=v*np.sin(ph)
dr*= (0.75+0.25*np.sin(2*np.pi*t/16))*np.minimum(1,t/4)
out+=np.stack([dr,dr],1)
def saw(f,tt,det): s=0
# braam: detuned saw stack through a lowpass that opens and closes
def braam(at,dur=3.4,v=.30):
    i0=int(at*sr); n=int(dur*sr); tt=np.arange(n)/sr; s=np.zeros(n,np.float32)
    for m,g in [(root,1),(root+12,.8),(root+19,.55),(root+24,.35)]:
        for dt in (-.08,0,.09): s+=g*sg.sawtooth(2*np.pi*mt(m+dt)*tt+rng.random()*6)
    envl=np.minimum(1,tt/.09)*np.exp(-np.maximum(0,tt-.3)/1.3)
    # time-varying lowpass: process in blocks
    y=np.zeros(n,np.float32); blk=1024; zi=None
    for k in range(0,n,blk):
        fc=180+900*np.exp(-tt[k]/0.6)+200*np.exp(-tt[k]/2); bb,aa=sg.butter(2,min(.99,fc/(sr/2)))
        if zi is None: zi=sg.lfilter_zi(bb,aa)*0
        y[k:k+blk],zi=sg.lfilter(bb,aa,s[k:k+blk],zi=zi)
    y*=envl*v/6; i1=min(L,i0+n); out[i0:i1]+=np.stack([y[:i1-i0]]*2,1)
def taiko(at,v=.55,f0=62):
    i0=int(at*sr); n=int(1.1*sr); tt=np.arange(n)/sr
    body=np.sin(2*np.pi*(f0*tt-(f0-38)*0.06*(1-np.exp(-tt/0.06))))*np.exp(-tt/.32)
    nz=rng.standard_normal(n)*np.exp(-tt/.03); bb,aa=sg.butter(2,900/(sr/2)); nz=sg.lfilter(bb,aa,nz)
    y=(body+.35*nz)*v; i1=min(L,i0+n); out[i0:i1,0]+=y[:i1-i0]; out[i0:i1,1]+=y[:i1-i0]*.92
# place braams on strong kicks at least 11 s apart, taiko on kicks at least 1.6 s apart, both off in the first 3 s
last_b=-99; last_t=-99
for k in kicks:
    if k<3 or k>T-5: continue
    if k-last_b>=11: braam(k); last_b=k; taiko(k,.7,58)
    elif k-last_t>=1.6: taiko(k,.42,66); last_t=k
# master: gentle glue, then limit to -1 dBFS
y=out/np.max(np.abs(out))*0.98
# loop: crossfade the last 4 s into the first 4 s
X=int(4*sr); fade=np.linspace(0,1,X)[:,None]; y[:X]=y[:X]*fade+y[-X:]*(1-fade); y=y[:-X]
w.write('conv_raw.wav',sr,(y*32767).astype(np.int16)); print('len',len(y)/sr)
