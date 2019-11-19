import shutil,os

with open("XDATCAR",'r') as f:
    tmp_lines = f.readlines()

head = []
for i in range(7):
    head.append(tmp_lines[i])
total_atoms = 0
for i in range(len(tmp_lines[6].split())):
    total_atoms += int(tmp_lines[6].split()[i])


total_structures = int((len(tmp_lines)-7)/(total_atoms+1))
if not os.path.exists("./structures"):
    os.mkdir("./structures")
for ii in range(total_structures):
    structure = open("md.vasp",'w')
    new_head = head.copy()
    for jj in range(total_atoms+1):
        tep = tmp_lines[7+ii*(total_atoms+1)].split()[2]
        new_head.append(tmp_lines[7+ii*(total_atoms+1)+jj])
    for kk in range(len(new_head)):
        structure.writelines(new_head[kk])
    structure.close()
    shutil.copy("./md.vasp","./structures/poscar-"+tep+".vasp")
