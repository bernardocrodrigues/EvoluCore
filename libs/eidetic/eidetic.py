import seaborn as sns
import numpy as np


import pandas as pd
# %matplotlib inline
import random
import matplotlib.pyplot as plt
import seaborn as sns

class eidetic(object):

    @staticmethod
    def plot(data: list, labels: list):

        grouped = []
        hue = []
        for i, item in enumerate(data):
            hue = hue + [labels[i-1]]*item.shape[0]
            grouped.append(item)
        grouped = np.vstack(grouped)

        # print(grouped, hue)


        sns_plot = sns.scatterplot(
            x= grouped[:,1],
            y= grouped[:,2],
            hue=hue,
            legend= "brief",
            palette=sns.color_palette( n_colors=2)
        ).get_figure()

        sns_plot.savefig("output.png")




if __name__ == "__main__":

    import libs.librarian.librarian
    lib_ = libs.librarian.librarian.librarian()
    # print(lib_.get_data(3))

    eidetic.plot([lib_.get_data(5), lib_.get_data(2)], ["aaa", "bbb"])

