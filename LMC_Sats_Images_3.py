#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 18:02:26 2020

@author: bush
"""

''' important- run: export TANGOS_DB_CONNECTION=/myhome2/users/munshi/Romulus/data_romulus25.working.db
in your shell to ensure that tangos knows where to look for the db.'''

'''This 3rd iteration properly creates cricles around the relevant satellites and hosts to more easily identify them.
In addition, it catches satellites whose particle IDs belong to a larger host instead of the LMC of interest'''

#import necessary modules
import pickle
import pynbody
import matplotlib.pyplot as plt
import numpy as np
import tangos
import pdb



#load up sim dataprint
#these are the relevant satellites
simSats = pickle.load(open('LMCSats.1.sim.pickle','rb'))
#these are the relevant hosts
simHosts = pickle.load(open('LMCs.1.sim.pickle', 'rb'))
relevant_keys = []
for key, value in simHosts.items():
    if len(simHosts[key]['Satellites']) > 0:
        relevant_keys.append(int(key))


#pdb.set_trace()




#load up rom data using z = 0 time stamp.
rom = tangos.get_simulation('cosmo25')[-1]




#load particle data for image creation later
s = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192')
s.physical_units()
#load up halos
h = s.halos(dosort = True)




'''Loop through host halos and their relevant satellites to generate images'''
#define empty list to populate with the problem hosts
Host_1Sats = []
Host_2Sats = []
Host_3Sats = []
Host_4Sats = []
Host_5Sats = []


#loop through the host halos
for key in simHosts.keys():

    #check to see if host has exactly 1 satellite
    if len(simHosts[key]['Satellites']) == 1:
        #load a copy of the halo to avoid too much memory usage
        hmain = h.load_copy(int(key))
        #store center as a variable for later use
        cen = rom[int(key)]['shrink_center']
        #convert halo to more easily interpretable units
        hmain.physical_units()
        #center the snapshot on the host of interest
        hmain['pos'] -= rom[int(key)]['shrink_center']
        #rotate so that the host is faceon
        try:
            pynbody.analysis.angmom.faceon(hmain.s,cen=[0,0,0])
        except:
            pynbody.analysis.angmom.faceon(hmain.s,cen_size="5 kpc",cen=[0,0,0])
        #store virial radius for circle later
        hmain_rvir = rom[int(key)]['max_radius']
        #create a new figure
        f = plt.figure()
        #create a stellar render of the host galaxy. Make the width of the image 2.5 * virial radius of host
        pynbody.plot.stars.render(hmain.s,width = 2.5*hmain_rvir)
        #create a white, unfilled circle, centered on the host with a radius equal to the hosts virial radius
        maincir = plt.Circle((0,0),hmain_rvir,color='w',fill=False)
        #add the circle to the current plot.
        f.gca().add_artist(maincir)
        #create a variable which stores the name of the satellites for plot title purposes.
        title = ', '.join(simHosts[key]['Satellites'])
        #title the plot based on HOST ID and the Satellite ID(s)
        plt.title('Satellite '+title+ ' with associated host '+str(key))
        #loop through satellites to generate circles the virial radii of all satellites.
        for i in simHosts[key]['Satellites']:
            #load up satellite data
            hsat = h.load_copy(int(i))
            #convert satellite data to physical units
            hsat.physical_units()
            #get satellite cooridinates
            hsat_iords = hsat.s['iord']
            #store satellite virial radius
            hsat_rvir = rom[int(i)]['max_radius']
            #check that particles exist in host and satellite. Create array for each host particle True = in host & satellite. False = Not in host and sat
            satstars = np.isin(hmain.s['iord'],hsat_iords)
            #store the shared star particle ids in an array
            shared_stars = hmain.s[satstars]
            if len(shared_stars) != 0:
                #calculate the shrink sphere center
                satcen = pynbody.analysis.halo.hybrid_center(hmain.s[satstars])
                #create circle centered on satellite, color it red.
                satcir = plt.Circle((satcen[0],satcen[1]),radius = hsat_rvir,color='r',fill=False)
                #add circle to current plot.
                f.gca().add_artist(satcir)
            else:
                plt.clf()
                if int(key) not in Host_1Sats:
                    Host_1Sats.append(int(key))

        #save figure to 2 locations.  One in the general location and another in the Number of satellites subdirectory.
        #plt.savefig('LMCHostSatImages/LMC1SatImageFaceOn'+str(key)+'.png')
        plt.savefig('LMCHostSatImages/1Sat/LMC1SatImageFaceOn'+str(key)+'.png')
        #show the plot
        plt.show()
        #Loop through the satellites of the host. Image satellites of host and store in same directory.


    #check to see if the host has exatly 2 satellites
    if len(simHosts[key]['Satellites']) == 2:
        #load a copy of the halo to avoid too much memory usage
        hmain = h.load_copy(int(key))
        #store center as a variable for later use
        cen = rom[int(key)]['shrink_center']
        #convert halo to more easily interpretable units
        hmain.physical_units()
        #center the snapshot on the host of interest
        hmain['pos'] -= rom[int(key)]['shrink_center']
        #rotate so that the host is faceon
        try:
            pynbody.analysis.angmom.faceon(hmain.s,cen=[0,0,0])
        except:
            pynbody.analysis.angmom.faceon(hmain.s,cen_size="5 kpc",cen=[0,0,0])
        #store virial radius for circle later
        hmain_rvir = rom[int(key)]['max_radius']
        #create a new figure
        f = plt.figure()
        #create a stellar render of the host galaxy. Make the width of the image 2.5 * virial radius of host
        pynbody.plot.stars.render(hmain.s,width = 2.5*hmain_rvir)
        #create a white, unfilled circle, centered on the host with a radius equal to the hosts virial radius
        maincir = plt.Circle((0,0),hmain_rvir,color='w',fill=False)
        #add the circle to the current plot.
        f.gca().add_artist(maincir)
        #create a variable which stores the name of the satellites for plot title purposes.
        title = ', '.join(simHosts[key]['Satellites'])
        #title the plot based on HOST ID and the Satellite ID(s)
        plt.title('Satellites '+title+ ' with associated host '+str(key))
        #loop through satellites to generate circles the virial radii of all satellites.
        for i in simHosts[key]['Satellites']:
            #load up satellite data
            hsat = h.load_copy(int(i))
            #convert satellite data to physical units
            hsat.physical_units()
            #get satellite cooridinates
            hsat_iords = hsat.s['iord']
            #store satellite virial radius
            hsat_rvir = rom[int(i)]['max_radius']
            #check that particles exist in host and satellite. Create array for each host particle True = in host & satellite. False = Not in host and sat
            satstars = np.isin(hmain.s['iord'],hsat_iords)
            #store the shared star particle ids in an array
            shared_stars = hmain.s[satstars]
            if len(shared_stars) != 0:
                #calculate the shrink sphere center
                satcen = pynbody.analysis.halo.hybrid_center(hmain.s[satstars])
                #create circle centered on satellite, color it red.
                satcir = plt.Circle((satcen[0],satcen[1]),radius = hsat_rvir,color='r',fill=False)
                #add circle to current plot.
                f.gca().add_artist(satcir)
            else:
                plt.clf()
                if int(key) not in Host_2Sats:
                    Host_2Sats.append(int(key))

        #save figure to 2 locations.  One in the general location and another in the Number of satellites subdirectory.
        #plt.savefig('LMCHostSatImages/LMC1SatImageFaceOn'+str(key)+'.png')
        plt.savefig('LMCHostSatImages/2Sat/LMC2SatImageFaceOn'+str(key)+'.png')
        #show the plot
        plt.show()
        #Loop through the satellites of the host. Image satellites of host and store in same directory.



    #check to see if the host has exatly 3 satellites
    if len(simHosts[key]['Satellites']) == 3:
        #load a copy of the halo to avoid too much memory usage
        hmain = h.load_copy(int(key))
        #store center as a variable for later use
        cen = rom[int(key)]['shrink_center']
        #convert halo to more easily interpretable units
        hmain.physical_units()
        #center the snapshot on the host of interest
        hmain['pos'] -= rom[int(key)]['shrink_center']
        #rotate so that the host is faceon
        try:
            pynbody.analysis.angmom.faceon(hmain.s,cen=[0,0,0])
        except:
            pynbody.analysis.angmom.faceon(hmain.s,cen_size="5 kpc",cen=[0,0,0])
        #store virial radius for circle later
        hmain_rvir = rom[int(key)]['max_radius']
        #create a new figure
        f = plt.figure()
        #create a stellar render of the host galaxy. Make the width of the image 2.5 * virial radius of host
        pynbody.plot.stars.render(hmain.s,width = 2.5*hmain_rvir)
        #create a white, unfilled circle, centered on the host with a radius equal to the hosts virial radius
        maincir = plt.Circle((0,0),hmain_rvir,color='w',fill=False)
        #add the circle to the current plot.
        f.gca().add_artist(maincir)
        #create a variable which stores the name of the satellites for plot title purposes.
        title = ', '.join(simHosts[key]['Satellites'])
        #title the plot based on HOST ID and the Satellite ID(s)
        plt.title('Satellites '+title+ ' with associated host '+str(key))
        #loop through satellites to generate circles the virial radii of all satellites.
        for i in simHosts[key]['Satellites']:
            #load up satellite data
            hsat = h.load_copy(int(i))
            #convert satellite data to physical units
            hsat.physical_units()
            #get satellite cooridinates
            hsat_iords = hsat.s['iord']
            #store satellite virial radius
            hsat_rvir = rom[int(i)]['max_radius']
            #check that particles exist in host and satellite. Create array for each host particle True = in host & satellite. False = Not in host and sat
            satstars = np.isin(hmain.s['iord'],hsat_iords)
            #store the shared star particle ids in an array
            shared_stars = hmain.s[satstars]
            if len(shared_stars) != 0:
                #calculate the shrink sphere center
                satcen = pynbody.analysis.halo.hybrid_center(hmain.s[satstars])
                #create circle centered on satellite, color it red.
                satcir = plt.Circle((satcen[0],satcen[1]),radius = hsat_rvir,color='r',fill=False)
                #add circle to current plot.
                f.gca().add_artist(satcir)
            else:
                plt.clf()
                if int(key) not in Host_3Sats:
                    Host_3Sats.append(int(key))

        #save figure to 2 locations.  One in the general location and another in the Number of satellites subdirectory.
        #plt.savefig('LMCHostSatImages/LMC1SatImageFaceOn'+str(key)+'.png')
        plt.savefig('LMCHostSatImages/3Sat/LMC3SatImageFaceOn'+str(key)+'.png')
        #show the plot
        plt.show()
        #Loop through the satellites of the host. Image satellites of host and store in same directory.

    #check to see if the host has exatly 4 satellites
    if len(simHosts[key]['Satellites']) == 4:
        #load a copy of the halo to avoid too much memory usage
        hmain = h.load_copy(int(key))
        #store center as a variable for later use
        cen = rom[int(key)]['shrink_center']
        #convert halo to more easily interpretable units
        hmain.physical_units()
        #center the snapshot on the host of interest
        hmain['pos'] -= rom[int(key)]['shrink_center']
        #rotate so that the host is faceon
        try:
            pynbody.analysis.angmom.faceon(hmain.s,cen=[0,0,0])
        except:
            pynbody.analysis.angmom.faceon(hmain.s,cen_size="5 kpc",cen=[0,0,0])
        #store virial radius for circle later
        hmain_rvir = rom[int(key)]['max_radius']
        #create a new figure
        f = plt.figure()
        #create a stellar render of the host galaxy. Make the width of the image 2.5 * virial radius of host
        pynbody.plot.stars.render(hmain.s,width = 2.5*hmain_rvir)
        #create a white, unfilled circle, centered on the host with a radius equal to the hosts virial radius
        maincir = plt.Circle((0,0),hmain_rvir,color='w',fill=False)
        #add the circle to the current plot.
        f.gca().add_artist(maincir)
        #create a variable which stores the name of the satellites for plot title purposes.
        title = ', '.join(simHosts[key]['Satellites'])
        #title the plot based on HOST ID and the Satellite ID(s)
        plt.title('Satellites '+title+ ' with associated host '+str(key))
        #loop through satellites to generate circles the virial radii of all satellites.
        for i in simHosts[key]['Satellites']:
            #load up satellite data
            hsat = h.load_copy(int(i))
            #convert satellite data to physical units
            hsat.physical_units()
            #get satellite cooridinates
            hsat_iords = hsat.s['iord']
            #store satellite virial radius
            hsat_rvir = rom[int(i)]['max_radius']
            #check that particles exist in host and satellite. Create array for each host particle True = in host & satellite. False = Not in host and sat
            satstars = np.isin(hmain.s['iord'],hsat_iords)
            #store the shared star particle ids in an array
            shared_stars = hmain.s[satstars]
            if len(shared_stars) != 0:
                #calculate the shrink sphere center
                satcen = pynbody.analysis.halo.hybrid_center(hmain.s[satstars])
                #create circle centered on satellite, color it red.
                satcir = plt.Circle((satcen[0],satcen[1]),radius = hsat_rvir,color='r',fill=False)
                #add circle to current plot.
                f.gca().add_artist(satcir)
            else:
                plt.clf()
                if int(key) not in Host_4Sats:
                    Host_4Sats.append(int(key))

        #save figure to 2 locations.  One in the general location and another in the Number of satellites subdirectory.
        #plt.savefig('LMCHostSatImages/LMC1SatImageFaceOn'+str(key)+'.png')
        plt.savefig('LMCHostSatImages/4Sat/LMC4SatImageFaceOn'+str(key)+'.png')
        #show the plot
        plt.show()


    #check to see if the host has exatly 5 satellites
    if len(simHosts[key]['Satellites']) == 5:
        #load a copy of the halo to avoid too much memory usage
        hmain = h.load_copy(int(key))
        #store center as a variable for later use
        cen = rom[int(key)]['shrink_center']
        #convert halo to more easily interpretable units
        hmain.physical_units()
        #center the snapshot on the host of interest
        hmain['pos'] -= rom[int(key)]['shrink_center']
        #rotate so that the host is faceon
        try:
            pynbody.analysis.angmom.faceon(hmain.s,cen=[0,0,0])
        except:
            pynbody.analysis.angmom.faceon(hmain.s,cen_size="5 kpc",cen=[0,0,0])
        #store virial radius for circle later
        hmain_rvir = rom[int(key)]['max_radius']
        #create a new figure
        f = plt.figure()
        #create a stellar render of the host galaxy. Make the width of the image 2.5 * virial radius of host
        pynbody.plot.stars.render(hmain.s,width = 2.5*hmain_rvir)
        #create a white, unfilled circle, centered on the host with a radius equal to the hosts virial radius
        maincir = plt.Circle((0,0),hmain_rvir,color='w',fill=False)
        #add the circle to the current plot.
        f.gca().add_artist(maincir)
        #create a variable which stores the name of the satellites for plot title purposes.
        title = ', '.join(simHosts[key]['Satellites'])
        #title the plot based on HOST ID and the Satellite ID(s)
        plt.title('Satellites '+title+ ' with associated host '+str(key))
        #loop through satellites to generate circles the virial radii of all satellites.
        for i in simHosts[key]['Satellites']:
            #load up satellite data
            hsat = h.load_copy(int(i))
            #convert satellite data to physical units
            hsat.physical_units()
            #get satellite cooridinates
            hsat_iords = hsat.s['iord']
            #store satellite virial radius
            hsat_rvir = rom[int(i)]['max_radius']
            #check that particles exist in host and satellite. Create array for each host particle True = in host & satellite. False = Not in host and sat
            satstars = np.isin(hmain.s['iord'],hsat_iords)
            #store the shared star particle ids in an array
            shared_stars = hmain.s[satstars]
            if len(shared_stars) != 0:
                #calculate the shrink sphere center
                satcen = pynbody.analysis.halo.hybrid_center(hmain.s[satstars])
                #create circle centered on satellite, color it red.
                satcir = plt.Circle((satcen[0],satcen[1]),radius = hsat_rvir,color='r',fill=False)
                #add circle to current plot.
                f.gca().add_artist(satcir)
            else:
                plt.clf()
                if int(key) not in Host_5Sats:
                    Host_5Sats.append(int(key))

        #save figure to 2 locations.  One in the general location and another in the Number of satellites subdirectory.
        #plt.savefig('LMCHostSatImages/LMC1SatImageFaceOn'+str(key)+'.png')
        plt.savefig('LMCHostSatImages/5Sat/LMC5SatImageFaceOn'+str(key)+'.png')
        #show the plot
        plt.show()

for i in Host_1Sats: #loop through hosts which did not image properly
    #load host (use copy to avoid using too much memory)
    hmain = h.load_copy(int(i))
    #convert to more practical units
    hmain.physical_units()
    #store center of host as a variable
    cen = rom[i]['shrink_center']
    #create transformation which will be later applied to entire region
    vx = pynbody.analysis.angmom.ang_mom_vec(hmain.s)
    mx = pynbody.analysis.angmom.calc_faceon_matrix(vx, up = [0.0, 1.0, 0.0])
    #store id of star particle for later use
    hmain_iords = hmain.s['iord']
    #store host virial radius for later use
    hmain_rvir = rom[i]['max_radius']
    #create region of interest centered on host. Convert particles in region to physical units and center region on center of host
    sptcls = s.s[pynbody.filt.Sphere(2.5*hmain_rvir,cen)].get_index_list(s)
    my_region = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192', take = sptcls)
    my_region.physical_units()
    my_region['pos'] -= cen
    #apply transformation to entire region
    my_region.transform(mx)
    #find the particles belonging to host within region and store as boolean array
    mainstars = np.isin(my_region.s['iord'],hmain_iords)
    #begin figure
    f = plt.figure()
    #create a variable which stores the name of the satellites for plot title purposes.
    title = ', '.join(simHosts[str(i)]['Satellites'])
    #create blank list and convert to array. All the satellite particles will be stored here
    hsat_tot = []
    hsat_tot = np.asarray(hsat_tot)
    for j in simHosts[str(i)]['Satellites']: #loop through satellites of host to add their particles to hsat_tot
        #load up sats using pynbody
        hsat = h.load_copy(int(j))
        #convert sats to meaningful units
        hsat.physical_units()
        #grab virial radius of satellite for circle plotting later
        hsat_rvir = rom[j]['max_radius']
        #grab IDs for star coordinates for sat
        hsat_iords = hsat.s['iord']
        #append IDs for star coordinates to array for plotting later.
        hsat_tot = np.append(hsat_tot,hsat_iords)
    #create boolean array to find particles in region and in all satellites
    hsat_tot = np.isin(my_region.s['iord'],hsat_tot)
    #plot region of interest. only render stars belonging to satellites or host
    pynbody.plot.stars.render(my_region.s[np.ma.mask_or(np.ma.make_mask(hsat_tot),np.ma.make_mask(mainstars))],width = 2.5*hmain_rvir)
    plt.title('Satellites '+title+ ' with associated host '+str(i))
    #create a circle centered on host with radius equal to its virial radius
    maincir = plt.Circle((0,0),hmain_rvir, color = 'w', fill = False)
    f.gca().add_artist(maincir)
    for k in simHosts[str(i)]['Satellites']: #loop through satellites again to create circles around satellites
        #load satellite and convert to meaningful units
        hsat = h.load_copy(int(k))
        hsat.physical_units()
        #store satellite virial radius as variable for later use
        hsat_rvir = rom[k]['max_radius']
        #store satellite star particle IDs
        hsat_iords = hsat.s['iord']
        #find  star particle IDs that exist in region of interest
        satstars = np.isin(my_region.s['iord'],hsat_iords)
        #store center of satellite
        satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #create circle centered on satellite with a radius equal to its virial radius and add it to the current figure
        satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r',fill=False)
        f.gca().add_artist(satcir)
    plt.savefig('LMCHostSatImages/1Sat/LMC1SatImageFaceOn'+str(i)+'.png')
    plt.show()


for i in Host_2Sats: #loop through hosts which did not image properly
    #load host (use copy to avoid using too much memory)
    hmain = h.load_copy(int(i))
    #convert to more practical units
    hmain.physical_units()
    #store center of host as a variable
    cen = rom[i]['shrink_center']
    #create transformation which will be later applied to entire region
    vx = pynbody.analysis.angmom.ang_mom_vec(hmain.s)
    mx = pynbody.analysis.angmom.calc_faceon_matrix(vx, up = [0.0, 1.0, 0.0])
    #store id of star particle for later use
    hmain_iords = hmain.s['iord']
    #store host virial radius for later use
    hmain_rvir = rom[i]['max_radius']
    #create region of interest centered on host. Convert particles in region to physical units and center region on center of host
    sptcls = s.s[pynbody.filt.Sphere(2.5*hmain_rvir,cen)].get_index_list(s)
    my_region = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192', take = sptcls)
    my_region.physical_units()
    my_region['pos'] -= cen
    #apply transformation to entire region
    my_region.transform(mx)
    #find the particles belonging to host within region and store as boolean array
    mainstars = np.isin(my_region.s['iord'],hmain_iords)
    #begin figure
    f = plt.figure()
    #create a variable which stores the name of the satellites for plot title purposes.
    title = ', '.join(simHosts[str(i)]['Satellites'])
    #create blank list and convert to array. All the satellite particles will be stored here
    hsat_tot = []
    hsat_tot = np.asarray(hsat_tot)
    for j in simHosts[str(i)]['Satellites']: #loop through satellites of host to add their particles to hsat_tot
        #load up sats using pynbody
        hsat = h.load_copy(int(j))
        #convert sats to meaningful units
        hsat.physical_units()
        #grab virial radius of satellite for circle plotting later
        hsat_rvir = rom[j]['max_radius']
        #grab IDs for star coordinates for sat
        hsat_iords = hsat.s['iord']
        #append IDs for star coordinates to array for plotting later.
        hsat_tot = np.append(hsat_tot,hsat_iords)
        #create boolean array for particles in my_region of interest and the satellite
        #satstars = np.isin(my_region.s['iord'],hsat_iords)
        #find the center of this satellite
        #satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r', fill=False)
        #f.gca().add_artist(satcir)
        #create circle around satellite and add
    #create boolean array to find particles in region and in all satellites
    hsat_tot = np.isin(my_region.s['iord'],hsat_tot)
    #plot region of interest. only render stars belonging to satellites or host
    pynbody.plot.stars.render(my_region.s[np.ma.mask_or(np.ma.make_mask(hsat_tot),np.ma.make_mask(mainstars))],width = 2.5*hmain_rvir)
    plt.title('Satellites '+title+ ' with associated host '+str(i))
    #create a circle centered on host with radius equal to its virial radius
    maincir = plt.Circle((0,0),hmain_rvir, color = 'w', fill = False)
    f.gca().add_artist(maincir)
    for k in simHosts[str(i)]['Satellites']: #loop through satellites again to create circles around satellites
        #load satellite and convert to meaningful units
        hsat = h.load_copy(int(k))
        hsat.physical_units()
        #store satellite virial radius as variable for later use
        hsat_rvir = rom[k]['max_radius']
        #store satellite star particle IDs
        hsat_iords = hsat.s['iord']
        #find  star particle IDs that exist in region of interest
        satstars = np.isin(my_region.s['iord'],hsat_iords)
        #store center of satellite
        satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #create circle centered on satellite with a radius equal to its virial radius and add it to the current figure
        satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r',fill=False)
        f.gca().add_artist(satcir)
    plt.savefig('LMCHostSatImages/2Sat/LMC2SatImageFaceOn'+str(i)+'.png')
    plt.show()

for i in Host_3Sats: #loop through hosts which did not image properly
    #load host (use copy to avoid using too much memory)
    hmain = h.load_copy(int(i))
    #convert to more practical units
    hmain.physical_units()
    #store center of host as a variable
    cen = rom[i]['shrink_center']
    #create transformation which will be later applied to entire region
    vx = pynbody.analysis.angmom.ang_mom_vec(hmain.s)
    mx = pynbody.analysis.angmom.calc_faceon_matrix(vx, up = [0.0, 1.0, 0.0])
    #store id of star particle for later use
    hmain_iords = hmain.s['iord']
    #store host virial radius for later use
    hmain_rvir = rom[i]['max_radius']
    #create region of interest centered on host. Convert particles in region to physical units and center region on center of host
    sptcls = s.s[pynbody.filt.Sphere(2.5*hmain_rvir,cen)].get_index_list(s)
    my_region = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192', take = sptcls)
    my_region.physical_units()
    my_region['pos'] -= cen
    #apply transformation to entire region
    my_region.transform(mx)
    #find the particles belonging to host within region and store as boolean array
    mainstars = np.isin(my_region.s['iord'],hmain_iords)
    #begin figure
    f = plt.figure()
    #create a variable which stores the name of the satellites for plot title purposes.
    title = ', '.join(simHosts[str(i)]['Satellites'])
    #create blank list and convert to array. All the satellite particles will be stored here
    hsat_tot = []
    hsat_tot = np.asarray(hsat_tot)
    for j in simHosts[str(i)]['Satellites']: #loop through satellites of host to add their particles to hsat_tot
        #load up sats using pynbody
        hsat = h.load_copy(int(j))
        #convert sats to meaningful units
        hsat.physical_units()
        #grab virial radius of satellite for circle plotting later
        hsat_rvir = rom[j]['max_radius']
        #grab IDs for star coordinates for sat
        hsat_iords = hsat.s['iord']
        #append IDs for star coordinates to array for plotting later.
        hsat_tot = np.append(hsat_tot,hsat_iords)
        #create boolean array for particles in my_region of interest and the satellite
        #satstars = np.isin(my_region.s['iord'],hsat_iords)
        #find the center of this satellite
        #satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r', fill=False)
        #f.gca().add_artist(satcir)
        #create circle around satellite and add
    #create boolean array to find particles in region and in all satellites
    hsat_tot = np.isin(my_region.s['iord'],hsat_tot)
    #plot region of interest. only render stars belonging to satellites or host
    pynbody.plot.stars.render(my_region.s[np.ma.mask_or(np.ma.make_mask(hsat_tot),np.ma.make_mask(mainstars))],width = 2.5*hmain_rvir)
    plt.title('Satellites '+title+ ' with associated host '+str(i))
    #create a circle centered on host with radius equal to its virial radius
    maincir = plt.Circle((0,0),hmain_rvir, color = 'w', fill = False)
    f.gca().add_artist(maincir)
    for k in simHosts[str(i)]['Satellites']: #loop through satellites again to create circles around satellites
        #load satellite and convert to meaningful units
        hsat = h.load_copy(int(k))
        hsat.physical_units()
        #store satellite virial radius as variable for later use
        hsat_rvir = rom[k]['max_radius']
        #store satellite star particle IDs
        hsat_iords = hsat.s['iord']
        #find  star particle IDs that exist in region of interest
        satstars = np.isin(my_region.s['iord'],hsat_iords)
        #store center of satellite
        satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #create circle centered on satellite with a radius equal to its virial radius and add it to the current figure
        satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r',fill=False)
        f.gca().add_artist(satcir)
    plt.savefig('LMCHostSatImages/3Sat/LMC3SatImageFaceOn'+str(i)+'.png')
    plt.show()





for i in Host_4Sats: #loop through hosts which did not image properly
    #load host (use copy to avoid using too much memory)
    hmain = h.load_copy(int(i))
    #convert to more practical units
    hmain.physical_units()
    #store center of host as a variable
    cen = rom[i]['shrink_center']
    #create transformation which will be later applied to entire region
    vx = pynbody.analysis.angmom.ang_mom_vec(hmain.s)
    mx = pynbody.analysis.angmom.calc_faceon_matrix(vx, up = [0.0, 1.0, 0.0])
    #store id of star particle for later use
    hmain_iords = hmain.s['iord']
    #store host virial radius for later use
    hmain_rvir = rom[i]['max_radius']
    #create region of interest centered on host. Convert particles in region to physical units and center region on center of host
    sptcls = s.s[pynbody.filt.Sphere(2.5*hmain_rvir,cen)].get_index_list(s)
    my_region = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192', take = sptcls)
    my_region.physical_units()
    my_region['pos'] -= cen
    #apply transformation to entire region
    my_region.transform(mx)
    #find the particles belonging to host within region and store as boolean array
    mainstars = np.isin(my_region.s['iord'],hmain_iords)
    #begin figure
    f = plt.figure()
    #create a variable which stores the name of the satellites for plot title purposes.
    title = ', '.join(simHosts[str(i)]['Satellites'])
    #create blank list and convert to array. All the satellite particles will be stored here
    hsat_tot = []
    hsat_tot = np.asarray(hsat_tot)
    for j in simHosts[str(i)]['Satellites']: #loop through satellites of host to add their particles to hsat_tot
        #load up sats using pynbody
        hsat = h.load_copy(int(j))
        #convert sats to meaningful units
        hsat.physical_units()
        #grab virial radius of satellite for circle plotting later
        hsat_rvir = rom[j]['max_radius']
        #grab IDs for star coordinates for sat
        hsat_iords = hsat.s['iord']
        #append IDs for star coordinates to array for plotting later.
        hsat_tot = np.append(hsat_tot,hsat_iords)
    #create boolean array to find particles in region and in all satellites
    hsat_tot = np.isin(my_region.s['iord'],hsat_tot)
    #plot region of interest. only render stars belonging to satellites or host
    pynbody.plot.stars.render(my_region.s[np.ma.mask_or(np.ma.make_mask(hsat_tot),np.ma.make_mask(mainstars))],width = 2.5*hmain_rvir)
    plt.title('Satellites '+title+ ' with associated host '+str(i))
    #create a circle centered on host with radius equal to its virial radius
    maincir = plt.Circle((0,0),hmain_rvir, color = 'w', fill = False)
    f.gca().add_artist(maincir)
    for k in simHosts[str(i)]['Satellites']: #loop through satellites again to create circles around satellites
        #load satellite and convert to meaningful units
        hsat = h.load_copy(int(k))
        hsat.physical_units()
        #store satellite virial radius as variable for later use
        hsat_rvir = rom[k]['max_radius']
        #store satellite star particle IDs
        hsat_iords = hsat.s['iord']
        #find  star particle IDs that exist in region of interest
        satstars = np.isin(my_region.s['iord'],hsat_iords)
        #store center of satellite
        satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #create circle centered on satellite with a radius equal to its virial radius and add it to the current figure
        satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r',fill=False)
        f.gca().add_artist(satcir)
    plt.savefig('LMCHostSatImages/4Sat/LMC4SatImageFaceOn'+str(i)+'.png')
    plt.show()

for i in Host_5Sats: #loop through hosts which did not image properly
    #load host (use copy to avoid using too much memory)
    hmain = h.load_copy(int(i))
    #convert to more practical units
    hmain.physical_units()
    #store center of host as a variable
    cen = rom[i]['shrink_center']
    #create transformation which will be later applied to entire region
    vx = pynbody.analysis.angmom.ang_mom_vec(hmain.s)
    mx = pynbody.analysis.angmom.calc_faceon_matrix(vx, up = [0.0, 1.0, 0.0])
    #store id of star particle for later use
    hmain_iords = hmain.s['iord']
    #store host virial radius for later use
    hmain_rvir = rom[i]['max_radius']
    #create region of interest centered on host. Convert particles in region to physical units and center region on center of host
    sptcls = s.s[pynbody.filt.Sphere(2.5*hmain_rvir,cen)].get_index_list(s)
    my_region = pynbody.load('/myhome2/users/munshi/Romulus/cosmo25/cosmo25p.768sg1bwK1BHe75.008192', take = sptcls)
    my_region.physical_units()
    my_region['pos'] -= cen
    #apply transformation to entire region
    my_region.transform(mx)
    #find the particles belonging to host within region and store as boolean array
    mainstars = np.isin(my_region.s['iord'],hmain_iords)
    #begin figure
    f = plt.figure()
    #create a variable which stores the name of the satellites for plot title purposes.
    title = ', '.join(simHosts[str(i)]['Satellites'])
    #create blank list and convert to array. All the satellite particles will be stored here
    hsat_tot = []
    hsat_tot = np.asarray(hsat_tot)
    for j in simHosts[str(i)]['Satellites']: #loop through satellites of host to add their particles to hsat_tot
        #load up sats using pynbody
        hsat = h.load_copy(int(j))
        #convert sats to meaningful units
        hsat.physical_units()
        #grab virial radius of satellite for circle plotting later
        hsat_rvir = rom[j]['max_radius']
        #grab IDs for star coordinates for sat
        hsat_iords = hsat.s['iord']
        #append IDs for star coordinates to array for plotting later.
        hsat_tot = np.append(hsat_tot,hsat_iords)
    #create boolean array to find particles in region and in all satellites
    hsat_tot = np.isin(my_region.s['iord'],hsat_tot)
    #plot region of interest. only render stars belonging to satellites or host
    pynbody.plot.stars.render(my_region.s[np.ma.mask_or(np.ma.make_mask(hsat_tot),np.ma.make_mask(mainstars))],width = 2.5*hmain_rvir)
    plt.title('Satellites '+title+ ' with associated host '+str(i))
    #create a circle centered on host with radius equal to its virial radius
    maincir = plt.Circle((0,0),hmain_rvir, color = 'w', fill = False)
    f.gca().add_artist(maincir)
    for k in simHosts[str(i)]['Satellites']: #loop through satellites again to create circles around satellites
        #load satellite and convert to meaningful units
        hsat = h.load_copy(int(k))
        hsat.physical_units()
        #store satellite virial radius as variable for later use
        hsat_rvir = rom[k]['max_radius']
        #store satellite star particle IDs
        hsat_iords = hsat.s['iord']
        #find  star particle IDs that exist in region of interest
        satstars = np.isin(my_region.s['iord'],hsat_iords)
        #store center of satellite
        satcen = pynbody.analysis.halo.center_of_mass(my_region.s[satstars])
        #create circle centered on satellite with a radius equal to its virial radius and add it to the current figure
        satcir = plt.Circle((satcen[0],satcen[1]),hsat_rvir,color = 'r',fill=False)
        f.gca().add_artist(satcir)
    plt.savefig('LMCHostSatImages/5Sat/LMC5SatImageFaceOn'+str(i)+'.png')
    plt.show()
