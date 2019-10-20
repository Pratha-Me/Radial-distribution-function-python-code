# -*- coding: utf-8 -*-
"""
Created on Tue May 15 10:18:57 2018

@author: pramosh
"""

'''! IMPORTANT NOTE BELOW
! THIS PROGRAM IS A MODULE AND WILL CALCULATE RDF FROM DL_POLY OUTPUT HISTORY FILE

! VARIABLES AND PARAMETER DECLARATIONS---------------------------------------------------'''

import numpy as np

def rdfs(data_na, data_cr, data_cw,data_cl):

    # THE CALCULATION OF CENTER OF RING
    nacw_zipped = zip(data_na,data_cw); ring_cent = []; i = 0
    #print nacw_zipped
    for x in data_cr:

        (a1,b1) = nacw_zipped[i]; (a2,b2) = nacw_zipped[i+1]
        ring_cent.append(a1/5.+a2/5.+b1/5.+b2/5.+x/5.)

        i += 2
    '''print a1,b1,a2,b2,ring_cent
    sys.exit('ON TEST')'''
    #-----------------------------------------------------------------------------------

    # THE CALCULATION OF GLOBAL/GENERAL DENSITY IN A SPHERE WITH RADIUS EQUAL TO THE CUT-OFF
    atom_cent = 0
    c = 15.752448/2. # The CUT-OFF length, This can be taken equal to the dimension of the box used in dl_poly

    for b in ring_cent:
        (x_cent,y_cent,z_cent) = b

        for e in data_cl:
            (x_cl,y_cl,z_cl) = e

            bl4 = np.sqrt((x_cent-x_cl)**2 +(y_cent-x_cl)**2 +(z_cent-x_cl)**2)
            if bl4 <= c:
               atom_cent += 1

    dens_cent_cl = (3*atom_cent)/(4*np.pi*(c**3))

    #print dens_cent_cl, dens_hcw_cl, dens_h1_cl , dens_hcr_cl
    #------------------------------------------------------------------------------------------

    # THE CALCULATION OF SHELL DENSITY WITH FUNCTION OF RADIUS IN A SPHERE WITH RADIUS EQUAL TO THE CUT-OFF
    dr = 0.1; r = dr; dn_cent = 0
    rad_dens_cent = []
    while r <= c:
        for b in ring_cent:
            (x_cent,y_cent,z_cent) = b

            for d in data_cl:
                (x_cl,y_cl,z_cl) = d

                blc = np.sqrt((x_cent-x_cl)**2 +(y_cent-y_cl)**2 +(z_cent-z_cl)**2)
                if r < blc and blc < r +dr:
                    dn_cent += 1

        rad_dens_cent.append(dn_cent/((4*np.pi*r**2*dr)*dens_cent_cl))

        dn_cent = 0
        r += dr

    #------------------------------------------------------------------------------------------
    #print rad_dens_hcr,rad_dens_hcw,rad_dens_h1

    return(rad_dens_cent)
