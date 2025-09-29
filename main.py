import pdbreader
import pandas as pd

DATA_FOLDER = "data/"
PDB_FILE = "1BRS"

if __name__ == "__main__":
    pdb_data = pdbreader.read_pdb(DATA_FOLDER + PDB_FILE + ".pdb")
    atom_df = pdb_data['ATOM']
    print(atom_df.head())

