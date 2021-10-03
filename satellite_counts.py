#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 18:02:26 2020

@author: bush
"""

#import necessary modules
import pickle
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import pdb

#load up sim data
simData = pickle.load(open('LMCs.1.sim.pickle','rb'))
pdb.set_trace()

#create blank list to append number of satellites for each halo for plotting
plotting_list = []
#loop over every single key in the "larger" dictionary (i.e. the list of relevant halos)
for key, n_info in simData.items():
    #go through each of the relevant halos and lookd specifically at the 'satellite' key'.
    #append the length of the key to the list (this tells you how many satellites there are for a halo)
    plotting_list.append(len(n_info['Satellites']))

#determine the frequency of the most commonly occuring element and store it as an integer using Counter
#this may be useful for scaling the histogram
max_freq = Counter(plotting_list).most_common(1)[0][1]

#plot the dummy list as a histogram.  Center it on the half integers to make formatting cleaner
plt.hist(plotting_list,np.arange(-.5,11.5,1),color="black")

#set the number of x ticks based on data
plt.xticks(ticks = np.arange(10))

#plot labels
plt.xlabel(r'$N_{Sat}$')
plt.ylabel('Number of Halos')
plt.show()
