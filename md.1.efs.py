from ase.io import read,write
import numpy as np

atoms_list = read("vasprun.xml",index='0::1')
with open('energies.dat','w') as e,open('forces.dat','w') as f,open('stress.dat','w') as s:
    for ii,atoms in enumerate(atoms_list):
        energy = atoms.get_total_energy()
        forces = atoms.get_forces()
        stress = atoms.get_stress()
        x,y = np.shape(forces)
        f.writelines(f"# {ii+1}\n")
        # energy
        e.writelines(f"{ii:4d}{energy:20.8f}\n")
        # forces
        for jj in range(x):
            for kk in range(y):
                f.writelines(f"{forces[jj][kk]:20.13f}\t")
            f.writelines(f"\n")
        # stress    
        for kk in range(6):
            s.writelines(f"{stress[kk]:20.13f}\t")
        s.writelines(f"\n")
        print(f"{ii+1} done")
