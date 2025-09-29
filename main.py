import pdbreader
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

DATA_FOLDER = "data/"
PDB_FILE = "1BRS"

if __name__ == "__main__":
    # parse whole pdb file
    pdb_data = pdbreader.read_pdb(DATA_FOLDER + PDB_FILE + ".pdb")

    # The ATOM records present the atomic coordinates for standard amino acids and nucleotides. They also present the occupancy and temperature factor for each atom. Non-polymer chemical coordinates use the HETATM record type. The element symbol is always present on each ATOM record; charge is optional.
    # Record Format
    # COLUMNS        DATA  TYPE    FIELD        DEFINITION
    # -------------------------------------------------------------------------------------
    #  1 -  6        Record name   "ATOM  "
    #  7 - 11        Integer       serial       Atom  serial number.
    # 13 - 16        Atom          name         Atom name.
    # 17             Character     altLoc       Alternate location indicator.
    # 18 - 20        Residue name  resName      Residue name.
    # 22             Character     chainID      Chain identifier.
    # 23 - 26        Integer       resSeq       Residue sequence number.
    # 27             AChar         iCode        Code for insertion of residues.
    # 31 - 38        Real(8.3)     x            Orthogonal coordinates for X in Angstroms.
    # 39 - 46        Real(8.3)     y            Orthogonal coordinates for Y in Angstroms.
    # 47 - 54        Real(8.3)     z            Orthogonal coordinates for Z in Angstroms.
    # 55 - 60        Real(6.2)     occupancy    Occupancy.
    # 61 - 66        Real(6.2)     tempFactor   Temperature  factor.
    # 77 - 78        LString(2)    element      Element symbol, right-justified.
    # 79 - 80        LString(2)    charge       Charge  on the atom.
    
    # extract just the atom entries
    atom_df = pdb_data['ATOM']
   
    # print column names
    print(list(atom_df.columns))

    # extract residue names
    names_df = atom_df['resname']

    atom_df_numeric = atom_df.select_dtypes(include=['number'])
    atom_df_numeric = atom_df_numeric.drop(['model_id', 'id', 'resid'], axis=1)
    atom_df_numeric = (atom_df_numeric - atom_df_numeric.min())/(atom_df_numeric.max() - atom_df_numeric.min())
    atom_df_numeric = atom_df_numeric.join(names_df)

    print(atom_df_numeric.head())
    print("Number of entries:", len(atom_df_numeric))
    print("Unique number of entries:", len(atom_df_numeric['resname'].unique()))
    
    pd.plotting.parallel_coordinates(atom_df_numeric, 'resname')
    plt.show()

    # plot x,y,z scatterplot cube
    atom_df_numeric = atom_df_numeric.drop(['occupancy', 'b_factor'], axis=1)
    
    cube = plt.figure().add_subplot(projection='3d')
    unique_labels = atom_df_numeric['resname'].unique()
    colors = plt.cm.get_cmap('viridis', len(unique_labels))
    for i, label in enumerate(unique_labels):
        subset = atom_df_numeric[atom_df_numeric['resname'] == label]
        cube.scatter(subset['x'], subset['y'], subset['z'], color=colors(i), label=label, s=50)


    #cube.scatter(atom_df_numeric['x'], atom_df_numeric['y'], atom_df_numeric['z'])
    plt.show()

