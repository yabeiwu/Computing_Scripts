#!/bin/bash
# this script can be used in various systems to calculate the lattice changes and
# atomic position displacements after your relaxation due to your chosen functional.
#################################################################################
# Written by Yabei Wu
# Shanghai Univeristy, & Unviversity at Buffalo
#################################################################################

echo "###############################################################"
echo "Reading Your System Information: POSCAR and CONTCAR"
echo "You Should Use Direct/Fractional Coordinates"
a1_in=`awk 'NR==3 {printf $1}' POSCAR`
a2_in=`awk 'NR==3 {printf $2}' POSCAR`
a3_in=`awk 'NR==3 {printf $3}' POSCAR`
b1_in=`awk 'NR==4 {printf $1}' POSCAR`
b2_in=`awk 'NR==4 {printf $2}' POSCAR`
b3_in=`awk 'NR==4 {printf $3}' POSCAR`
c1_in=`awk 'NR==5 {printf $1}' POSCAR`
c2_in=`awk 'NR==5 {printf $2}' POSCAR`
c3_in=`awk 'NR==5 {printf $3}' POSCAR`
a1_fi=`awk 'NR==3 {printf $1}' CONTCAR`
a2_fi=`awk 'NR==3 {printf $2}' CONTCAR`
a3_fi=`awk 'NR==3 {printf $3}' CONTCAR`
b1_fi=`awk 'NR==4 {printf $1}' CONTCAR`
b2_fi=`awk 'NR==4 {printf $2}' CONTCAR`
b3_fi=`awk 'NR==4 {printf $3}' CONTCAR`
c1_fi=`awk 'NR==5 {printf $1}' CONTCAR`
c2_fi=`awk 'NR==5 {printf $2}' CONTCAR`
c3_fi=`awk 'NR==5 {printf $3}' CONTCAR`
echo "Lattice Parameters Before Relaxation are: "
a_in=`echo "sqrt($a1_in*$a1_in+($a2_in*$a2_in)+($a3_in*$a3_in))" | bc -l`
echo "a: $a_in"
b_in=`echo "sqrt($b1_in*$b1_in+($b2_in*$b2_in)+($b3_in*$b3_in))" | bc -l`
echo "b: $b_in"
c_in=`echo "sqrt($c1_in*$c1_in+($c2_in*$c2_in)+($c3_in*$c3_in))" | bc -l`
echo "c: $c_in"
echo "###############################################################"
echo "Lattice Parameters After Relaxation are: "
a_fi=`echo "sqrt($a1_fi*$a1_fi+($a2_fi*$a2_fi)+($a3_fi*$a3_fi))" | bc -l`
echo "a: $a_fi"
b_fi=`echo "sqrt($b1_fi*$b1_fi+($b2_fi*$b2_fi)+($b3_fi*$b3_fi))" | bc -l`
echo "b: $b_fi"
c_fi=`echo "sqrt($c1_fi*$c1_fi+($c2_fi*$c2_fi)+($c3_fi*$c3_fi))" | bc -l`
echo "c: $c_fi"
echo "###############################################################"
echo "Your Lattice Changed by percentage are: "
delta_a=`echo "($a_fi-$a_in)/$a_in*100" | bc -l`
delta_b=`echo "($b_fi-$b_in)/$b_in*100" | bc -l`
delta_c=`echo "($c_fi-$c_in)/$c_in*100" | bc -l`
echo "Delta_a: $delta_a" 
echo "Delta_b: $delta_b" 
echo "Delta_c: $delta_c" 
echo "###############################################################"

# Due to your systems, in my system, only has four atoms
echo "Writing Your Atomic Position Displacement Details In File \"position.txt\" "
echo -e "# No. of atoms \t x_direction_dis \t y_direction_dis \t z_direction_dis \t sum_dis_per/atom \t total_dis_all_atom" > position.txt
sum=0.0
for j in 9 10 11 12
do
atomx_in=`awk -v j="$j" 'NR==j {printf $1}' POSCAR`
atomy_in=`awk -v j="$j" 'NR==j {printf $2}' POSCAR`
atomz_in=`awk -v j="$j" 'NR==j {printf $3}' POSCAR`
atomx_fi=`awk -v j="$j" 'NR==j {printf $1}' CONTCAR`
atomy_fi=`awk -v j="$j" 'NR==j {printf $2}' CONTCAR`
atomz_fi=`awk -v j="$j" 'NR==j {printf $3}' CONTCAR`
disx=`echo "($atomx_fi*$a1_fi+($atomy_fi*$b1_fi)+($atomz_fi*$c1_fi))-(($atomx_in*$a1_in)+($atomy_in*$b1_in)+($atomz_in*$c1_in))" | bc `
disy=`echo "($atomx_fi*$a2_fi+($atomy_fi*$b2_fi)+($atomz_fi*$c2_fi))-(($atomx_in*$a2_in)+($atomy_in*$b2_in)+($atomz_in*$c2_in))" | bc `
disz=`echo "($atomx_fi*$a3_fi+($atomy_fi*$b3_fi)+($atomz_fi*$c3_fi))-(($atomx_in*$a3_in)+($atomy_in*$b3_in)+($atomz_in*$c3_in))" | bc `

vale=`echo "($disx)*($disx)+($disy)*($disy)+($disz)*($disz)" | bc -l `
dis=`echo "sqrt($vale)" | bc -l`
sum=`echo "$sum+$dis" |bc -l`
echo -e "\t$j\t$disx\t$disy\t$disz\t$dis\t$sum" >> position.txt
done

echo "Your total atomic position displacement is: "
echo "$sum"
