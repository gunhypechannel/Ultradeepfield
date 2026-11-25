# One Carcinid crab: python3 crc_crab.py <key> <outdir> [voxel]. The knobs match the game's CRC_CRAB, plus the look of each painting.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from crc_lib import *
CRAB = {  # w half-width, l half-length, h height, kk claw size, fg fangs, hn horn pairs, th leg thickness, t tint, extras
    'cscut': dict(w=1.05, l=1.1, h=.5, kk=.85, fg=4, hn=1, th=.85, t='blue', ant=1, coral=2),
    'cspit': dict(w=1.1, l=1.1, h=.55, kk=.75, fg=4, hn=0, th=.95, turret=1, coral=5, t='blue'),
    'charv': dict(w=1.3, l=1.1, h=.45, kk=.7, fg=4, hn=0, th=.9, sacs=1, t='blue'),
    'cguard': dict(w=1.25, l=1.25, h=.95, kk=1.05, fg=6, hn=2, th=1.25, spikes=16, coral=4, barn=5, rows=5, t='blue'),
    'cbrood': dict(w=1.25, l=1.15, h=.6, kk=.8, fg=6, hn=1, th=1.05, abdo=1, t='krak'),
    'cwar': dict(w=1.25, l=1.2, h=.75, kk=1.45, fg=6, hn=3, th=1.15, coral=3, barn=6, spikes=6),
    'ccrys': dict(w=1.15, l=1.15, h=.6, kk=1, fg=4, hn=1, th=1, crys=7, coral=2, t='blue'),
    'clanc': dict(w=.85, l=1.35, h=.6, kk=1.25, fg=4, hn=1, th=.95, tail=1, ant=1, t='blue'),
    'cmolt': dict(w=1.35, l=1.3, h=.85, kk=1.3, fg=8, hn=3, th=1.25, t='pale', molt=1),
    'cmar': dict(w=1.4, l=1.3, h=.85, kk=1.75, fg=8, hn=0, th=1.3, t='red', spikes=16, crest=7, sp=1.3),
    'cmat': dict(w=1.35, l=1.25, h=.75, kk=1.15, fg=6, hn=0, th=1.15, t='pearl', abdo=1, pearls=1),
    'ctyr': dict(w=1.5, l=1.35, h=1.05, kk=1.35, fg=8, hn=1, th=1.35, t='coral', coral=22, spikes=6, barn=8, rows=5),
    'cora': dict(w=1.3, l=1.25, h=.75, kk=1.15, fg=8, hn=0, th=1.15, t='oracle', eye3=1, ant=1),
    'ckor': dict(w=1.55, l=1.35, h=.95, kk=1.7, fg=10, hn=4, th=1.35, t='gold', crown=1, spikes=10, crest=5, sp=1.2),
    'cbeh': dict(w=1.7, l=1.45, h=1.2, kk=1.4, fg=8, hn=1, th=1.45, city=1, coral=8, barn=10, rows=6, t='blue'),
    'ckbr': dict(w=1.4, l=1.3, h=.85, kk=1.6, fg=10, hn=1, th=1.3, t='krak', tent=10),
    'cpal': dict(w=1.4, l=1.3, h=.85, kk=1.55, fg=8, hn=1, th=1.25, t='pale', crys=14, sp=1.3),
    'ccrown': dict(w=1.75, l=1.5, h=1.2, kk=1.8, fg=12, hn=5, th=1.45, t='gold', crown=1, city=1, coral=8, rows=6),
    'ccrownm': dict(w=1.75, l=1.5, h=1.2, kk=1.8, fg=12, hn=5, th=1.45, t='pale', crown=1, molt=1, rows=6),
}
if __name__ == '__main__':
    k = sys.argv[1]; P = dict(CRAB[k]); P['k'] = k; vox = float(sys.argv[3]) if len(sys.argv) > 3 else .035
    ext = 1 + P['kk'] * .5
    M = Model((-P['l'] * (4.2 if P.get('tail') else 2.6 if P.get('abdo') or P.get('tent') else 1.6), -1.1, -(P['w'] + 2.4)), (P['l'] * 1.3 + 2.4 * P['kk'] + .5, 3.6, P['w'] + 2.4), vox)
    crab(M, P); M.bake(sys.argv[2], paint)
