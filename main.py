# %% imports
import pandas as pd
import matplotlib.pyplot as plt
import os

# %% read data
data = None
directory = os.path.join("./data")
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".csv"):
            if data is None:
                data = pd.read_csv(os.path.join(
                    directory, file), index_col=False)
            else:
                data = pd.concat([data, pd.read_csv(os.path.join(
                    directory, file), index_col=False)], ignore_index=True)

print(data)

# %% plot the data


def histogram(data, title, xlabel, ylabel, showDensity=False, bins=None):
    plt.hist(data, density=showDensity, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


# %%
def d(date, featureName):
    features = data[data["Date"] == date][featureName]
    title = 'Histogram of ' + featureName + ' on ' + date
    histogram(features, title,
              featureName, 'Density', True)


# %%
date = '1/1/2014'
for featureName in data.columns.values[3:]:
    d(date, featureName)

# %%
