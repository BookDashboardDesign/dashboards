import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs


# generate random normal distributed data for x and y and store it in a pandas DataFrame (for plot 1,2 und 5)
def generate_random_data(seed=8):
    np.random.seed(seed)
    df = pd.DataFrame({'y': np.random.normal(loc=0,
                                             scale=10,
                                             size=1000),
                       'x': np.random.normal(loc=10,
                                             scale=2,
                                             size=1000)})
    return df


def generate_random_cluster_data():
    # generic cluster data (for plot 3 und 4)
    X, y = make_blobs(n_samples=7500,
                      centers=3,
                      n_features=2,
                      random_state=0,
                      cluster_std=0.75)

    cluster_df = pd.DataFrame(data=X, columns=["X", "Y"])
    cluster_df['cluster'] = [str(i) for i in y]
    return cluster_df


def update_selected_data(cluster_df, selected_data):
    if selected_data is None or (isinstance(selected_data, dict) and 'xaxis.range[0]' not in selected_data):
        cluster_dff = cluster_df
    else:
        cluster_dff = cluster_df[(cluster_df['X'] >= selected_data.get('xaxis.range[0]')) &
                                 (cluster_df['X'] <= selected_data.get('xaxis.range[1]')) &
                                 (cluster_df['Y'] >= selected_data.get('yaxis.range[0]')) &
                                 (cluster_df['Y'] <= selected_data.get('yaxis.range[1]'))]
    return cluster_dff