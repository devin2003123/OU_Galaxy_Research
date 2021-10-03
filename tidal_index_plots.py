#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 14:17:03 2021

@author: bush
"""
#import necessary modules
import pickle
import numpy as np
from matplotlib import pyplot as plt
import pdb


def data_check(dictionary):
    '''checks that there are more than 10 data points in passed dictionary'''
    new_dict = {}
    for key, dic in dictionary.items():
        for k2 in dic:
            if k2 == 'NumPoints' and dic['NumPoints'] > 10:
                new_dict[key] = dic
    total_removed = len(dictionary) - len(new_dict)
    print ('{total_removed} entries removed from dictionary due to insufficieint number of data points'.format(total_removed = str(total_removed)))
    return new_dict

def mean_plot_generator(dictionary):
    '''make a histogram of the means of the disruption indices'''
    lst = []
    greatest = 0
    for key, dic in dictionary.items():
        for k2, value in dic.items():
            if k2 == 'Mean':
                lst.append(value)
        for k2, value in dic.items():
            if k2 == 'Mean' and value > greatest:
                greatest = value
    print(greatest)
    mean = np.mean(lst)
    std = np.std(lst)
    final_plot = plt.hist(lst, bins = np.arange(0, np.ceil(greatest) + 1), alpha = 0.8)
    plt.xlabel('Tidal Disruption Index')
    plt.ylabel('Count')
    plt.axvline(mean, color = 'g', label = 'Average')
    plt.axvline(mean + 3 * std, color = 'k', label = '+3 Stds')
    plt.axvline(mean - 3 * std, color = 'r', label = '-3 Stds')
    plt.title('Tidal Disruption Index Means')
    plt.legend()
    return final_plot

def medians_plot_generator(dictionary):
    '''make a histogram of the medians of the disruption indices'''
    lst = []
    greatest = 0
    for key, dic in dictionary.items():
        for k2, value in dic.items():
            if k2 == 'Median':
                lst.append(value)
        for k2, value in dic.items():
            if k2 == 'Median' and value > greatest:
                greatest = value
    print(greatest)
    mean = np.mean(lst)
    std = np.std(lst)
    final_plot = plt.hist(lst, bins = np.arange(0, np.ceil(greatest) + 1), alpha = 0.8)
    plt.xlabel('Tidal Disruption Index')
    plt.ylabel('Count')
    plt.axvline(mean, color = 'g', label = 'Average')
    plt.axvline(mean + 3 * std, color = 'k', label = '+3 Stds')
    plt.axvline(mean - 3 * std, color = 'r', label = '-3 Stds')
    plt.title('Tidal Disruption Index Medians')
    plt.legend()
    return final_plot

def current_plot_generator(dictionary):
    '''make a histogram of the current values of the disruption indices'''
    lst = []
    greatest = 0
    for key, dic in dictionary.items():
        for k2, value in dic.items():
            if k2 == 'Current':
                lst.append(value)
        for k2, value in dic.items():
            if k2 == 'Current' and value > greatest:
                greatest = value
    print(greatest)
    mean = np.mean(lst)
    std = np.std(lst)
    final_plot = plt.hist(lst, bins = np.arange(0, np.ceil(greatest) + 1), alpha = 0.8)
    plt.xlabel('Tidal Disruption Index')
    plt.ylabel('Count')
    plt.axvline(mean, color = 'g', label = 'Average')
    plt.axvline(mean + 3 * std, color = 'k', label = '+3 Stds')
    plt.axvline(mean - 3 * std, color = 'r', label = '-3 Stds')
    plt.title('Tidal Disruption Index Current values')
    plt.legend()
    return final_plot



tidal_data_file = open("tidal_ind_data.pkl", "rb")
tidal_data = pickle.load(tidal_data_file)
tidal_data_file.close()

tidal_data_file2 = open("mult_sats.pkl", "rb")
tidal_data_2 = pickle.load(tidal_data_file2)
tidal_data_file2.close()



tidal_data_2 = data_check(tidal_data_2)
print(len(tidal_data))

tidal_data.update(tidal_data_2)

plt1 = mean_plot_generator(tidal_data)
plt.show()
plt.clf()

plt2 = medians_plot_generator(tidal_data)
plt.show()
plt.clf()

plt3 = current_plot_generator(tidal_data)
plt.show()
plt.clf()

# =============================================================================
# pdb.set_trace()
# currents = []
# means = []
# meds = []
#
# for key, dic in tidal_data.items():
#     for k2, value in dic.items():
#         if k2 == 'Current':
#             currents.append(value)
#         if k2 == 'Mean':
#             means.append(value)
#         if k2 == 'Median':
#             meds.append(value)
#
#
# means_mean = np.mean(means)
# means_std = np.std(means)
# plt.hist(means, bins = np.arange(0, 5), alpha = 0.5)
# plt.xlabel('Tidal Disruption Index')
# plt.ylabel('Count')
# plt.axvline(means_mean, color = 'r', label = 'Average')
# plt.axvline(means_mean + 3 * means_std, color = 'g', label = '3 Stds')
# plt.axvline(means_mean - 3 * means_std, color = 'g', label = '3 Stds')
# plt.title('Tidal Disruption Means')
# plt.legend()
# plt.show()
# =============================================================================
