#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 18:02:26 2020

@author: bush
"""

#import necessary modules
import pickle
import matplotlib.pyplot as plt
#from collections import Counter
import numpy as np
import pdb

#load up sim data
simSats = pickle.load(open('LMCSats.1.sim.pickle','rb'))
simHosts = pickle.load(open('LMCs.1.sim.pickle','rb'))



#create blank list to append number of satellites for each halo for plotting
plotting_list = []


#loop over every single key in the "larger" dictionary (i.e. the list of relevant halos)
for key, n_info in simSats.items():
    #go through each of the relevant halos and lookd specifically at the 'satellite' key'.
    #append the length of the key to the list (this tells you how many satellites there are for a halo)
    if n_info['Mvir'] < 2.5e11:
        plotting_list.append((n_info['Mvir'])/1e10)



#find which satellite has a mass of interest. Only useful if specifically asked to identify a specific satellite. Uncomment and modify in this case
'''max = 0
for key, x in simSats.items():
    print(x['Mvir'],x['Host'])
    if x['Mvir'] > max and x['Mvir'] < 3e12:
        max = x['Mvir']
print ('the maximum mass is',max)
pdb.set_trace()'''


#max_freq = Counter(plotting_list).most_common(1)[0][1]
#plot the dummy list as a histogram.  Center it on the half integers to make formatting cleaner
plt.hist(plotting_list,np.arange(-.5,7.5,1),color="k")
#set the number of x ticks based on data
#plt.xticks(ticks = np.arange(10))
#plt.yticks(range(0,max_freq+2))

#plot labels

plt.xlabel(r'$M_{\odot}*10^{10}$')
plt.ylabel('Number of Satellites')
plt.show()
