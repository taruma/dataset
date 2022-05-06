from pathlib import Path
import pandas as pd
import numpy as np

PATH_DATA_BMKG = Path(r'D:\02 Employment or Job\dataset_bmkg_2021\data_bmkg_2021_pandas.h5')
PATH_DATA_BMKG_COMPLETENESS = Path(r'D:\02 Employment or Job\dataset_bmkg_2021\completeness_data_bmkg.h5')
PATH_DUMMY_DATA = Path("dummy_data.h5")
PATH_DUMMY_COMPLETENESS = Path("dummy_completeness.h5")

with pd.HDFStore(PATH_DATA_BMKG, mode='r') as store:
    metadata_files = store.get('/metadata/files')

N = 42

shuffler = metadata_files.sample(N)

df_dummy = pd.read_csv('name_gen.txt')
df_dummy = df_dummy.sample(N).reset_index(drop=True)
df_dummy['ID WMO'] = np.random.choice(np.arange(96000, 97981), N, replace=False)
df_dummy['Lintang'] = shuffler.Lintang.to_numpy() + (np.random.rand(N) / 1e2 * np.random.choice([-1, 1], N))
df_dummy['Bujur'] = shuffler.Bujur.to_numpy() + (np.random.rand(N) / 1e2 * np.random.choice([-1, 1], N))
df_dummy['Elevasi'] = shuffler.Elevasi.to_numpy() + ((np.random.randint(1, 100, N)))
df_dummy = df_dummy.set_index('ID WMO')

original_stat_id = metadata_files.index.to_numpy()

# fmt: off
with pd.HDFStore(PATH_DUMMY_DATA, mode="w", complevel=1) as store_data, \
    pd.HDFStore(PATH_DUMMY_COMPLETENESS, mode="w", complevel=1) as store_comp, \
    pd.HDFStore(PATH_DATA_BMKG, mode="r") as read_data, \
    pd.HDFStore(PATH_DATA_BMKG_COMPLETENESS, mode="r") as read_comp:

# fmt: on
    store_data.put("/metadata/files", value=df_dummy)

    for stat_id in df_dummy.index:
        np.random.shuffle(original_stat_id)
        stat_picker = np.random.choice(original_stat_id)
        try:
            df_data = read_data.get(f'/stations/sta{stat_picker}')
            df_comp = read_comp.get(f'/stations/sta{stat_picker}')
            
            store_data.put(f'/stations/sta{stat_id}', value=df_data, format='table')
            store_comp.put(f'/stations/sta{stat_id}', value=df_comp, format='table')
        except:
            print('ERROR')
            break
        
        