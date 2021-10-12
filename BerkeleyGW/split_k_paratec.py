## this script is used to split the number of kpoints in the PARATEC calculation to solve the calculation problem with too many kpoints in a single calculation.

import numpy as np
import math
import os, shutil

def read_kpoints(kpointsfile):
    with open("kpoints.dat",'r') as f:
        lines = f.readlines()
    total_nkpoints = int(lines[0].split()[0])
    kparts = math.ceil(total_nkpoints/seperation)
    return lines,kparts

def write_file(filename,klist):
    with open(f"{filename}",'w') as f:
        f.write(f"{len(klist):10d}\n")
        for mm in range(len(klist)):
            f.write(f"{klist[mm]}")

def prepare_files(filename):
    os.system(f"ln -s ../N_POT.DAT {filename}/")
    os.system(f"ln -s ../CD {filename}/")
    os.system(f"ln -s ../wfnselect.inp {filename}/")
    #shutil.copy("Mo_POT.DAT",f"{filename}/")
    #shutil.copy("Si_POT.DAT",f"{filename}/")
    #shutil.copy("N_POT.DAT",f"{filename}/")
    shutil.copy("input",f"{filename}/")
    shutil.copy("job.paratec",f"{filename}/")

if __name__ == '__main__':
    seperation = 900    # define as your own

    lines, kparts = read_kpoints("kpoints.dat")

    print(kparts)
    for ii in range(kparts+1):
        if not os.path.exists(f"tmp_{ii+1}"):
            os.mkdir(f"tmp_{ii+1}")
        if ii != kparts:
            klist = lines[int(seperation*ii+1):int(seperation*(ii+1)+1)]
        else:
            klist = lines[int(seperation*(kparts-1)+1):]
        write_file(f"tmp_{ii+1}/KPOINTS",klist)
        prepare_files(f"tmp_{ii+1}")