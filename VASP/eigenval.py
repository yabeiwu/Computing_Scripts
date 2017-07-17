#######################################################################################################
# Copyright @ Yabei Wu,
# Shanghai University; University at Buffalo, the State University of New York
# E-mail: yabeiwu@buffalo.edu;
#         yabeiwu@163.com
#######################################################################################################
# This is python code to extracting eigenvalues from vasprun.xml file
#######################################################################################################
from array import *
from operator import itemgetter
import numpy as np
import re
import datetime
import math
#import kpoint.py
starttime = datetime.datetime.now()
print "------------------------------------------------------------------------------------------------"
print "initializing..."
with open('vasprun.xml','r') as f:
    lines = f.readlines()
    number_of_lines = len([l for l in lines if l.strip(' \n') != ''])
f.close()
print """Read the system information: fermi energy, number of kpoints, number of bands
       number of atoms, and number of division of the high symmetry lines"""
for i in range(number_of_lines):
        fermi_lines_initial = re.findall("<i name=\"efermi\"> .*", lines[i], re.M)
        kpoint_lines_initial = re.findall("<set comment=\"kpoint .*\">", lines[i], re.M)
        nbands_lines_initial = re.findall("<i type=\"int\" name=\"NBANDS\"> .*", lines[i], re.M)
        division_lines_initial = re.findall("<i name=\"divisions\" .* ", lines[i], re.M)
        atoms_lines_initial = re.findall("<atoms> .*<\/atoms>", lines[i], re.M)
        spin_lines_initial = re.findall("<i type=\"int\" name=\"ISPIN\"> .*", lines[i], re.M)
        if len(fermi_lines_initial) != 0:
            fermi_lines = fermi_lines_initial
        if len(kpoint_lines_initial) != 0:
            kpoint_lines = kpoint_lines_initial
        if len(nbands_lines_initial) != 0:
            nbands_lines = nbands_lines_initial
        if len(division_lines_initial) != 0:
            division_lines = division_lines_initial
        if len(atoms_lines_initial) != 0:
            atoms_lines = atoms_lines_initial
        if len(spin_lines_initial) != 0:
            spin_lines = spin_lines_initial
fermi_energy = float(fermi_lines[0].split()[2])
number_of_bands = int(float(nbands_lines[0].split()[3].split("<")[0]))
number_of_kpoints = int(float(kpoint_lines[-1].split()[2].split("\"")[0]))
number_of_division = int(float(division_lines[0].split()[3]))
spin = int(spin_lines[0].split()[3].split("<")[0])
print "Reading system information done..."

#######################################################################################################
# Section 1: kpoints position part
print "------------------------------------------------------------------------------------------------"
print "Determing the reciprocal lattice constant"
reciprocal_lattice = []
with open('vasprun.xml','r') as f:
    copy = False                                                 
    for line in f:
        if line.strip() == '<varray name=\"rec_basis\" >':
            copy = True
        elif line.strip() == '</varray>':
            copy = False
        elif copy:
            reciprocal_lattice.append(line)
f.close()
b = np.zeros((3,3))
for i in range(3):
    for j in range(3):
        b[i][j] = float(reciprocal_lattice[i].split()[j+1])
print "Reciprocal Lattice read done..."
print "------------------------------------------------------------------------------------------------"
print "k point list for plotting generating"
kpoint_lists = []
with open('vasprun.xml','r') as f:
    copy = False                                                 
    for line in f:
        if line.strip() == '<generation param=\"listgenerated\">':
            copy = True
        elif line.strip() == '</generation>':
            copy = False
        elif copy:
            kpoint_lists.append(line)
f.close()
number_of_highsymmetry_kpoints = len(kpoint_lists)-1
k_position_initial = np.zeros((number_of_highsymmetry_kpoints,3))
for i in range(number_of_highsymmetry_kpoints):
    for j in range(3):
        k_position_initial[i][j] = float(kpoint_lists[i+1].split()[j+1])
k_position = np.dot(k_position_initial,b)
line_step = np.zeros(number_of_highsymmetry_kpoints-1)
for i in range(number_of_highsymmetry_kpoints-1):
    line_step[i] = math.sqrt((k_position[i+1][0]-k_position[i][0])**2+\
                             (k_position[i+1][1]-k_position[i][1])**2+\
                             (k_position[i+1][2]-k_position[i][2])**2)/(number_of_division-1)
kpoint_position = []
for i in range(96):
    final = 0.0
    for j in range(number_of_highsymmetry_kpoints-1):
        for k in range(number_of_division):
            position = final+line_step[j]*k
            position = str("%.10f" % position)
            kpoint_position.append(position)
        final = float(position)
print "k point list generating done..."
print "------------------------------------------------------------------------------------------------"
#######################################################################################################

#######################################################################################################
# Section 2: vaspband part 
print "------------------------------------------------------------------------------------------------"
print "write the band structure data to file vaspband.dat"
vaspband = open("vaspband.dat",'w')
eigenval_initial = []
if spin == 1:
    with open('vasprun.xml','r') as f:
        copy = False
        for line in f:
            if line.strip() == '<set comment=\"spin 1\">':
                copy = True
            elif line.strip() == '<set comment=\"spin 2\">':
                copy = False
            elif copy:
                eigenval_initial.append(line)
    f.close()
    total_lines = (number_of_bands+2)*number_of_kpoints
    tmp = eigenval_initial[1:total_lines]   # this part should be changed
    tmp = [item for item in tmp if len(item.split()) == 4]
    band = []
    vaspband.writelines("# band \t k \t positions \t energy \n")
    for i in range(number_of_bands):
    	for j in range(number_of_kpoints):
    		vaspband.writelines(str(i+1))
    		vaspband.writelines('\t')
    		vaspband.writelines(str(j+1))
    		vaspband.writelines('\t')
    		band.append(tmp[i+j*number_of_bands].split()[1])
    		vaspband.writelines(str(kpoint_position[j]))
    		vaspband.writelines('\t')
    		vaspband.writelines(str(float(band[j+i*number_of_kpoints])-fermi_energy))
    		vaspband.writelines('\n')
    	vaspband.writelines('\n')
    vaspband.close()
    print 'Job is done!'
elif spin == 2:
    # spin up
    eigenval_initial_up = []
    with open('vasprun.xml','r') as f:
        copy = False
        for line in f:
            if line.strip() == '<set comment=\"spin 1\">':
                copy = True
            elif line.strip() == '<set comment=\"spin 2\">':
                copy = False
            elif copy:
                eigenval_initial_up.append(line)
    f.close()
    # spin down
    eigenval_initial_dn = []
    with open('vasprun.xml','r') as f:
        copy = False
        for line in f:
            if line.strip() == '<set comment=\"spin 2\">':
                copy = True
            elif line.strip() == '<set comment=\"spin 1\">':
                copy = False
            elif copy:
                eigenval_initial_dn.append(line)
    f.close()
    
    total_lines = (number_of_bands+2)*number_of_kpoints
    tmp_up = eigenval_initial_up[1:total_lines]   
    tmp_up = [item for item in tmp_up if len(item.split()) == 4]
    tmp_dn = eigenval_initial_dn[1:total_lines]   
    tmp_dn = [item for item in tmp_dn if len(item.split()) == 4]
    band_up = []
    band_dn = []
    vaspband.writelines("# band \t k \t positions \t energy_up \t energy_dn \n")
    for i in range(number_of_bands):
    	for j in range(number_of_kpoints):
    		vaspband.writelines(str(i+1))
    		vaspband.writelines('\t')
    		vaspband.writelines(str(j+1))
    		vaspband.writelines('\t')
    		band_up.append(tmp_up[i+j*number_of_bands].split()[1])
    		band_dn.append(tmp_dn[i+j*number_of_bands].split()[1])
    		vaspband.writelines(str(kpoint_position[j]))
    		vaspband.writelines('\t')
    		vaspband.writelines(str(float(band_up[j+i*number_of_kpoints])-fermi_energy))
    		vaspband.writelines('\t')
    		vaspband.writelines(str(float(band_dn[j+i*number_of_kpoints])-fermi_energy))
    		vaspband.writelines('\n')
    	vaspband.writelines('\n')
    print 'Job is done!'
    vaspband.close()
endtime = datetime.datetime.now()
print "Total run time is: ",float((endtime-starttime).seconds)," s"
#######################################################################################################
