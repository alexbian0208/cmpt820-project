import pandas as pd
import os

data = None
directory = os.path.join("./data")
for root,dirs,files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            if data is None:
                data = pd.read_csv(os.path.join(directory,file),index_col=False)
            else:
                data = pd.concat([data, pd.read_csv(os.path.join(directory,file),index_col=False)],ignore_index=True)

print(data)