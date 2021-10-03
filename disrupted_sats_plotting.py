#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 10:51:50 2021

@author: bush
"""

#import necessary modules
import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import pdb

def data_check(dictionary):
    '''checks that there are more than 10 data points in passed dictionary'''
    #dict to be returned later
    new_dict = {}
    #loop through keys, each key has an associated dictionary as a value. Loop through values as well
    for key, dic in dictionary.items():
        #loop through keys in inner dictionary
        for k2 in dic:
            #check that the NumPoints value is >10, if so, append to new_dict
            if k2 == 'NumPoints' and dic['NumPoints'] > 10:
                new_dict[key] = dic
    #let user know how many datapoints were removed
    total_removed = len(dictionary) - len(new_dict)
    print ('{total_removed} entries removed from dictionary due to insufficieint number of data points'.format(total_removed = str(total_removed)))
    return new_dict



#load up dictionary data from pkl files
tidal_data_file = open("tidal_ind_data.pkl", "rb")
tidal_data = pickle.load(tidal_data_file)
tidal_data_file.close()

tidal_data_file2 = open("mult_sats.pkl", "rb")
tidal_data_2 = pickle.load(tidal_data_file2)
tidal_data_file2.close()

#clean data and merge dictionaries
tidal_data_2 = data_check(tidal_data_2)
tidal_data.update(tidal_data_2)

#grab keys from merged dictionary. These are a list of the satellite keys relevant to analysis
relevant_keys = list(tidal_data.keys())


#load up sim dataprint
#these are the relevant satellites
simSats = pickle.load(open('LMCSats.1.sim.pickle','rb'))
#these are the relevant hosts
simHosts = pickle.load(open('LMCs.1.sim.pickle', 'rb'))


# =============================================================================
# xlen = np.arange(len(simSats['346']['CumSFH'])) / 100
# ylen = simSats['2178']['CumSFH']
# ax = plt.subplot()
# ax.set_xticks(np.arange(1,15,2))
# plt.xlabel('Time [Gyr]')
# plt.ylabel('Cumulative Fractional SFH')
# plt.title('Satellite 2178 SFH vs. Time')
# plt.plot(xlen,ylen)
# plt.show()
# =============================================================================




cbar_values = []
cmap = mpl.cm.cool
fig, ax = plt.subplots()
ax.set_xticks(np.arange(1,15,2))
for num in relevant_keys:
    cbar_values.append(simSats[str(num)]['Mstar'])
norm = mpl.colors.LogNorm(vmin = min(cbar_values), vmax = max(cbar_values))
#fig.colorbar(mpl.cm.ScalarMappable(norm = norm, cmap = cmap), orientation = 'vertical', label = r'Stellar Mass [$M_\odot$]')
#pdb.set_trace()
for num in relevant_keys:
    xlen = np.arange(len(simSats[str(num)]['CumSFH'])) / 100
    ylen = simSats[str(num)]['CumSFH']
    #cbar_values.append(simSats[str(num)]['Mstar'])
    plt.plot(xlen,ylen, linestyle = 'dashed')
    #plt.plot(xlen,ylen, linestyle = 'dashed', color = cmap(norm(simSats[str(num)]['Mstar'])))
plt.xlabel('Time [Gyr]')
plt.ylabel('Cumulative Fractional SFH')
plt.title('SFH vs. Time')

plt.show()
