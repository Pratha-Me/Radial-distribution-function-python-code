# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 14:11:25 2018

@author: pramosh
"""

'''! IMPORTANT NOTE BELOW
! THIS PROGRAM WILL READ CALL MODULE IN ORDER TO CALCULATE RDF FROM DL_POLY OUTPUT HISTORY FILE

! VARIABLES AND PARAMETER DECLARATIONS---------------------------------------------------'''

import sys
import numpy as np
import matplotlib.pyplot as plt
import lib_rdf
file = open('HISTORY.txt', 'r')

data=[]
for line in file:
    data.append(line.split())

# STARTING THE COUNT FROM 0 THE FILE HAS BEEN ENUMERATED LINE AFTER LINE
enu_data = list(enumerate(data))
'''for i,row in enu_data:
    if (i-2)%684 ==0:
        print i, row
sys.exit()'''

c = 15.752448/2. # THE CUT-OFF LENGTH, THIS CAN BE TAKEN EQUAL TO THE DIMENSION OF THE BOX USED IN DL_POLY
dr = 0.1 # THE RADIAL STEPS FOR THE CALCULATION OF RADIAL DISTRIBUTIION
r_sp = np.arange(dr,c,dr)

# LIST CREATION
data_na= []; data_cr = []; data_cw = []; data_cl= []

# MAKE DUMMY NUMPY ARRAYS FOR ALL OF THE RADIAL DENS LIST
rad_l = int(c/dr)
tot_dens_cent = np.zeros(rad_l)
#--------------------------------------------------------------------

#---------------------------------------------------------------
'''
 The values of Init_config and last_config are integers
 The value for init_config should be greater or equal to => 0 <=
 The value for last_config should be lesser or equal to => 2499 <=
'''
Init_config = 0; last_config =500
#---------------------------------------------------------------

con_range = last_config - Init_config; tot_config = 2500

k = 0; l = 0; p = 0
for (i,row) in enu_data: # i is the line number and row is the data in that line

    # LOOP GYMNASTICS
    if i < 6:
        continue

    if (i-2)%684 ==0:
        p = i; k +=1
        continue

    if i in range(p+1,p+4):
        continue
    #-----------------------------------------------------------

    # THE RANGE OF CONFIGURATION FOR WHICH R.D.F WILL BE AVERAGED
    if k in range(0,Init_config):
        continue
    elif k == Init_config:
        pass
    #------------------------------------------------------------

    # AT THE LAST CONFIGURATION, CALCULATE THE AVERAGE HERE
    # AND THEN BREAK THE LOOP IF K IS IN THE RANGE OF THE DESIRED NUMBER OF CONFIGURATION
    if k == last_config:

        # tot_dens_hcw IS A PYTHON LIST TYPE
        tot_dens_cent[:] = [x / con_range  for x in tot_dens_cent]

	break
    # FOR THE LAST CONFIGURATION OF THE SYSTEM
    if k == tot_config -1:
	k += 1
	pass
    #----------------------------------------------------------------------------------

    if Init_config+1 == k:
        #print 'Configuration number', k

        #CONVERSION OF LIST INTO NUMPY ARRAY
        data_na = np.asarray(data_na);data_cr = np.asarray(data_cr);data_cw = np.asarray(data_cw)
        data_cl = np.asarray(data_cl)
        #-----------------------------------------------------------------------------
        '''print len(data_na),len(data_cr),len(data_cw),len(data_cl),len(data_h1)
        sys.exit()'''

        rad_dens_cent = lib_rdf.rdfs(data_na, data_cr, data_cw, data_cl)

        # COLLECT THE DATA BEFORE RETROSPECTIVELY DELETING IT
        tot_dens_cent = [x + y for x, y in zip(tot_dens_cent, rad_dens_cent)]

        # CONVERT NUMPY ARRAY TO LIST
        data_na = []; data_cr= []; data_cw= []
        data_cl = []

        Init_config += 1
    #-------------------------------------------------------------------

    # SEARCHES FOR THE ATOM NAME AND SKIPS IF IT'S C1 ATOM
    if i % 2 == 0:
        at_nam = row[0] # PICKS THE ATOM NAME ONLY
        if at_nam not in ('C1', 'HCW', 'H1', 'HCR'):
            #print (k, at_nam) #PRINTS THE ATOM NAME IF IT IS NOT C1 ATOM
            continue # SKIPS THE LOOP FROM HERE IF C1 ATOM IS NOT DETECTED
        elif at_nam in ('C1', 'HCW', 'H1', 'HCR'):
            l = i

    if i in range(l,l+1):
        continue # SKIPS THE LOOP FROM HERE IF C1 ATOM IS DETECTED
# SKIPS THE LOOP FROM HERE IF C1 ATOM IS DETECTED

    # CO-ORDINATE DATA COLLECTION IN A LIST
    if at_nam == 'NA':
        a = float(row[0]);b = float(row[1]);c = float(row[2])
        add = [a,b,c]
        data_na.append(add)

    if at_nam == 'CR':
        a = float(row[0]);b = float(row[1]);c = float(row[2])
        add = [a,b,c]
        data_cr.append(add)

    if at_nam == 'CW':
        a = float(row[0]);b = float(row[1]);c = float(row[2])
        add = [a,b,c]
        data_cw.append(add)

    if at_nam == 'Cl':
        a = float(row[0]);b = float(row[1]);c = float(row[2])
        add = [a,b,c]
        data_cl.append(add)
    #--------------------------------------------------------------------------

print "THE RANGE OF CONFIGURATIONS WAS %i" %con_range
# PLOTTING THE DATA------------------------------------------------------------
plt.plot(r_sp, tot_dens_cent, '-', color = 'b',markersize=8)

plt.legend('R_{CENTER}-Cl')

plt.xlabel('Radius (in $\AA$)',fontsize=27,style='italic',color = '#8A0FE2')
plt.ylabel('R.D.F',fontsize=27,style='italic',color = '#8A0FE2')
plt.title('THE IONIC LIQUID',fontsize=38,fontweight='bold',color = 'r')

plt.show()
#plt.savefig('1.pdf', bbox_inches='tight')
#--------------------------------------------------------------------------------

