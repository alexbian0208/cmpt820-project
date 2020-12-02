# %% imports
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

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

# %% helper functions


def histogram(data, title, xlabel, ylabel, showDensity=False, bins=None):
    plt.hist(data, density=showDensity, bins=bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


def showHistogramForFeature(date, featureName):
    features = data[data["Date"] == date][featureName]
    title = 'Histogram of ' + featureName + ' on ' + date
    histogram(features, title,
              featureName, 'Density', True)


def showHeatmapForFeature(data, date, featureName):
    pivottedData = data[data["Date"] == date].pivot(
        'Latitude', 'Longitude', featureName)
    plt.imshow(pivottedData, cmap='jet')
    plt.title('Heatmap of ' + featureName + ' on ' + date)
    plt.axis('off')
    plt.show()


# %%
date = '1/1/2014'
for featureName in data.columns.values[3:]:
    showHistogramForFeature(date, featureName)

# %%
date = '1/1/2014'
for featureName in data.columns.values[3:]:
    showHeatmapForFeature(data, date, featureName)

# %% KNN
features = data.columns.values[3:]
date = '2013'
featureName = 'Solar'

dataOnDate = data[data["Date"].str[-4:] == date]

classifier = KNeighborsRegressor(n_neighbors=10)
classifier.fit(
    dataOnDate[features[features != featureName]], dataOnDate[featureName])

date = '7/7/2014'
dataOnDate = data[data["Date"] == date]

showHeatmapForFeature(dataOnDate, date, featureName)

predicted = dataOnDate[['Date', 'Longitude', 'Latitude']]
predicted[featureName] = classifier.predict(
    dataOnDate[features[features != featureName]])
showHeatmapForFeature(predicted, date, featureName)

dataOnDate = data[data["Date"] == date]

offset = dataOnDate[['Date', 'Longitude', 'Latitude']]
offset[featureName] = abs(dataOnDate[featureName] - predicted[featureName])
showHeatmapForFeature(offset, date, featureName)

classifier.score(dataOnDate[features[features != featureName]], dataOnDate[featureName])

# %% Decision Tree
features = data.columns.values[3:]
date = '2013'
featureName = 'Solar'

dataOnDate = data[data["Date"].str[-4:] == date]

classifier = DecisionTreeRegressor()
classifier.fit(
    dataOnDate[features[features != featureName]], dataOnDate[featureName])

date = '7/7/2014'
dataOnDate = data[data["Date"] == date]

showHeatmapForFeature(dataOnDate, date, featureName)

predicted = dataOnDate[['Date', 'Longitude', 'Latitude']]
predicted[featureName] = classifier.predict(
    dataOnDate[features[features != featureName]])
showHeatmapForFeature(predicted, date, featureName)

dataOnDate = data[data["Date"] == date]

offset = dataOnDate[['Date', 'Longitude', 'Latitude']]
offset[featureName] = abs(dataOnDate[featureName] - predicted[featureName])
showHeatmapForFeature(offset, date, featureName)

classifier.score(dataOnDate[features[features != featureName]], dataOnDate[featureName])
# %%
