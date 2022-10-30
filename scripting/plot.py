import glob
import matplotlib.pyplot as plt
import os
import pandas as pd

PACKAGE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
DATA_DIR = os.path.join(PACKAGE_DIR, "data")


if __name__=="__main__":

    os.chdir(DATA_DIR)
    for file in glob.glob("*.csv"):
        ext_start_idx = file.find(".csv")
        percent_used = file[5:ext_start_idx]
        
        fig, axis = plt.subplots(2, figsize=(13,8))

        # distance vs generation
        data_df = pd.read_csv(file)
        data_df.set_index('Unnamed: 0', inplace=True)
        data_df.index.name = "Generation"
        axis[0].plot(data_df.min(axis=1), label="Min")
        axis[0].plot(data_df.mean(axis=1), label="Average")
        axis[0].set_xlabel("Generation")
        axis[0].set_ylabel("Distance")
        axis[0].set_title(percent_used + " crossover (Generation v Distance)")
        axis[0].legend(loc="center right")

        # fitness vs genreration
        data_df_fitness = data_df.apply(lambda row : 1000-row, axis=1)
        axis[1].plot(data_df_fitness.max(axis=1), label="Max", color='g')
        axis[1].plot(data_df_fitness.mean(axis=1), label="Average", color='orange')
        axis[1].set_xlabel("Generation")
        axis[1].set_ylabel("Fitness")
        axis[1].set_title(percent_used + " crossover (Generation v Fitness)")
        axis[1].legend(loc="center right")

        fig.tight_layout()
        plt.savefig(percent_used + '.png')
        #plt.show()