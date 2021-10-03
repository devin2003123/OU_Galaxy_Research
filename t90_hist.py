#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 21:47:27 2021

@author: bush
"""


#import necessary modules
import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import pdb


#load up sim dataprint
#these are the relevant satellites
simSats = pickle.load(open('LMCSats.1.sim.pickle','rb'))
#these are the relevant hosts
simHosts = pickle.load(open('LMCs.1.sim.pickle', 'rb'))

def calculate_t90(dic):
    ''' calculates t90 for a given halo. Sets t90 to 14.5 Byr if halo is not quenched '''
    for key in dic:
        if dic[key]['Quenched'] == False:
            dic[key]['t90'] = 14.5
        else:
            #loop through cumSFR and pull out t90
            for index, value in enumerate(dic[key]['CumSFH']):
                if value < 0.90:
                    pass
                else:
                    dic[key]['t90'] = index / 100.
                    break
    return dic
simSats = calculate_t90(simSats)

#create a list to store the t90 values for plotting
lst = []
for key in simSats:
    lst.append(simSats[key]['t90'])

#create histogram of t90 distribution
fig, ax = plt.subplots()
ax.set_xticks(np.arange(1,15,2))
ax.set_yticks(np.arange(0,20,4))
plt.xlabel(r'$t_{90}$ [Gyr]',fontsize = 16)
plt.ylabel('Count')
plt.title('Time untill 90% star formation')
plt.hist(lst, bins = 15, range = (0,15))
plt.show()
