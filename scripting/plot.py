import matplotlib.pyplot as plt
import os
import pandas as pd

PACKAGE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
LOG_FILE = os.path.join(DATA_DIR, "data.csv")


if __name__=="__main__":
    data_df = pd.read_csv(LOG_FILE)
    data_df.set_index('Unnamed: 0', inplace=True)
    data_df.index.name = "Generation"
    
    max_generation_df = data_df.min(axis=1)
    avg_generation_df = data_df.mean(axis=1)

    max_generation_df.plot()
    avg_generation_df.plot()
    plt.show()