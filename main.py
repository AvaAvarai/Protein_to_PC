import pdbreader
import pandas as pd
import matplotlib.pyplot as plt

DATA_FOLDER = "data/"
PDB_FILE = "1BRS"

if __name__ == "__main__":
    pdb_data = pdbreader.read_pdb(DATA_FOLDER + PDB_FILE + ".pdb")
    atom_df = pdb_data['ATOM']
    atom_df_numeric = atom_df.select_dtypes(include=['number'])
    atom_df_numeric = atom_df_numeric.drop(['model_id', 'id'], axis=1)
    print(atom_df_numeric.head())
    pd.plotting.parallel_coordinates(atom_df_numeric, 'resid')
    plt.show()

