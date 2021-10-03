#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 09:50:38 2021

@author: bush
"""

import pickle
import tangos as db
import matplotlib.pyplot as plt
import numpy as np
import sys
import pdb
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
simname = 'cosmo25'



#load up sim dataprint
#these are the relevant satellites
simSats = pickle.load(open('LMCSats.1.sim.pickle','rb'))
#these are the relevant hosts
simHosts = pickle.load(open('LMCs.1.sim.pickle', 'rb'))

#grab isolated LMC IDs with at least 1 sat
relevant_keys = []
for key, value in simHosts.items():
    if len(simHosts[key]['Satellites']) > 1:
        relevant_keys.append(int(key))
relevant_keys.sort()
relevant_sat_keys = []
for num in relevant_keys:
    for sat_key in simHosts[str(num)]['Satellites']:
        relevant_sat_keys.append(int(sat_key))
relevant_sat_keys.sort()
#hid = 123

def wrap(relpos, scale, boxsize=25e3):
    bphys = boxsize*scale
    bad = np.where(np.abs (relpos) > bphys/2.)
    if type(bphys) == np.ndarray:
        relpos[bad] = -1.0 * (relpos[bad] / np.abs(relpos[bad])) * np.abs(bphys[bad] - np.abs(relpos[bad]))
    else:
        relpos[bad] = -1.0 * (relpos[bad] / np.abs(relpos[bad])) * np.abs(bphys - np.abs(relpos[bad]))
    return
#sim = db.get_simulation(simname)
all_tidarr = {}
for haloID in relevant_sat_keys:
    ctr = 123
    sim = db.get_simulation(simname)
    hnum,hcen,time,redshift = sim[123][haloID].calculate_for_progenitors('halo_number()','shrink_center','t()','z()')
    tidarr = [] #tidal indices
    tarr = [] #times
    for i, hc, t, z in zip(hnum,hcen,time,redshift):
        pos,mvir,allid = sim[ctr].calculate_all('shrink_center','Mvir','halo_number()')
        xcen = pos[:,0]
        ycen = pos[:,1]
        zcen = pos[:,2]
        
        [xcen_h,ycen_h,zcen_h] = [hc[0],hc[1],hc[2]]
        xcen = [x-xcen_h for x in xcen]
        ycen = [y-ycen_h for y in ycen]
        zcen = [z-zcen_h for z in zcen]
        
        aval = 1/(1+z)
        relpos = np.vstack((xcen,ycen,zcen))
        wrap(relpos,aval)
        relpos = np.transpose(relpos)
        dist = np.array([np.sqrt(a**2+b**2+c**2) for a,b,c in zip(relpos[:,0],relpos[:,1],relpos[:,2])])
     
        
        den = [m/ ((d/1000)**3) for m,d in zip(mvir[dist>0],dist[dist>0])]
        dp = max(den)
        mpind = np.where(den == dp)
        mp = np.array(allid)[dist > 0][mpind]

        c = -11.75
        tidind = np.log10(dp) + c
        tidarr.append(tidind)
        tarr.append(t)
        ctr = ctr-1
    if len(tidarr) > 0:
        all_tidarr[haloID] = {'Current': tidarr[0], 'Mean': np.mean(tidarr), 'Median': np.median(tidarr), 'NumPoints': len(tidarr)}
    print ('The current length of tidarr is {}'.format(len(all_tidarr)))
pdb.set_trace()
# =============================================================================
# plt.plot(tarr,tidarr,'k.',linestyle='-')
# plt.ylabel('Tidal Index', fontsize = 20)
# plt.xlabel('Age of the Universe (Gyr)',fontsize = 20)
# plt.title('Halo ' + str(hid),fontsize = 20)
# plt.show()
# =============================================================================
