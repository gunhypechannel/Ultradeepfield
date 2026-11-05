# Flagship Command material economy model (v298). Mirrors fsLootPB / fsLootGather / fsRecipe / fsDrop in docs/index.html.
# Usage: python3 tools/flagship_econ.py [daily_cap=70] [tier_divisor=8]. Prints days to forge a full 8-slot set per tier and player type.
import random, sys
CAP=int(sys.argv[1]) if len(sys.argv)>1 else 60
D=int(sys.argv[2]) if len(sys.argv)>2 else 8
SLOTS={'weapon':('circuit','cube'),'shield':('crystal','cube'),'armor':('alloy','bio'),'reactor':('crystal','void'),
 'bridge':('circuit','bio'),'engine':('alloy','crystal'),'computer':('circuit','crystal'),'artifact':('void','cube')}
def cl(v,a,b): return max(a,min(b,v))
def drops(kind,L,rally=False):
    r=random.random
    if kind=='boss':
        t=cl(1+L//7,2,5); return [('cube',t,2+L//10+(1 if rally else 0)),('void',t,1+(1 if r()<(.5 if rally else .25) else 0)),('cube',min(6,t+1),1 if r()<.1 else 0)]
    if kind=='mon':
        t=cl(1+L//D,1,5); return [('bio',t,1+L//8),('void',t,1 if r()<.35 else 0),('cube',t,1 if r()<.08 else 0),('bio',min(6,t+1),1 if r()<.1 else 0)]
    if kind=='pir':
        t=cl(1+L//D,1,5); return [('circuit',t,1+L//5),('alloy',t,1+L//8),('circuit',min(6,t+1),1 if r()<.12 else 0)]
    if kind=='gath':
        t=cl(1+L//D,1,5); m=random.choice(['crystal','alloy']); return [(m,t,3),(m,min(6,t+1),1 if r()<.12 else 0)]
def day(profile):
    got={}; n=0
    for kind,L,cnt,rally in profile:
        for _ in range(int(cnt)+(1 if random.random()<cnt%1 else 0)):
            for m,t,k in drops(kind,L,rally):
                for _ in range(k):
                    if n>=CAP and random.random()>0.5**(1+(n-CAP)/15): continue
                    got[m]=got.get(m,0)+5**(t-1); n+=1
    return got,n
def need(t):
    tot={}
    for p,s in SLOTS.values():
        tot[p]=tot.get(p,0)+3*5**(t-1); tot[s]=tot.get(s,0)+2*5**(t-1); tot['alloy']=tot.get('alloy',0)+5*5**(max(1,t-1)-1)
    return tot
P={'casual':[('pir',10,6,0),('mon',10,2,0),('gath',10,4,0),('boss',11,0.33,1)],
   'active':[('pir',15,14,0),('mon',22,6,0),('gath',20,10,0),('boss',21,1,1)],
   'hardcore':[('pir',15,60,0),('mon',28,30,0),('gath',28,30,0),('boss',28,4,1)]}
random.seed(7)
for name,prof in P.items():
    days=[day(prof) for _ in range(300)]; avg={}
    for g,_ in days:
        for k,v in g.items(): avg[k]=avg.get(k,0)+v/len(days)
    out=[]
    for t,nm in [(3,'Rare'),(4,'Epic'),(5,'Legendary'),(6,'Mythic')]:
        nd=need(t); b=max(nd,key=lambda k:nd[k]/avg.get(k,1e-9)); d=nd[b]/avg.get(b,1e-9); out.append(f'{nm} {d:.0f}d({b})')
    print(f'{name:9s} {sum(n for _,n in days)/len(days):4.0f} drops/day  '+'  '.join(out))
