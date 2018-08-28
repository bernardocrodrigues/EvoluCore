
import numpy as np
import seaborn as sns; sns.set()
from matplotlib import pyplot as plt
plt.figure(figsize=(19, 10))

class eidetic(object):

    @staticmethod
    def plot(data: list, types= None, file= "output.png", labels = False, tittle = "", xlabel="", ylabel=""):

        grouped = []
        hue = []
        colors = len(data)

        if types != None:
            for datum, label in zip(data, types):
                if len(datum) != 0:
                    hue = hue + [label]*datum.shape[0]
                    grouped.append(datum)
                else:
                    colors -= 1
        else:
            for i, datum in enumerate(data):
                if len(datum) != 0:
                    hue = hue + [i]*datum.shape[0]
                    grouped.append(datum)
                else:
                    colors -= 1

        grouped = np.vstack(grouped)

        sns_plot = sns.scatterplot(
            x= grouped[:,1],
            y= grouped[:,2],
            hue=hue,
            legend= "brief",
            palette=sns.color_palette( n_colors=colors),
        )

        if labels:
            for datum in data:
                for k in datum:
                    sns_plot.text(k[1],
                                  k[2],
                                  "{0:.0f}".format(k[0]),
                                  family='sans-serif',
                                  textcoords='offset points',
                                  fontsize=18)

        sns_plot = sns_plot.get_figure()

        plt.title(tittle)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        sns_plot.savefig(file)
        sns_plot.clf()
        plt.clf()





if __name__ == "__main__":

    import libs.librarian.librarian
    import libs.paretoFrontier.paretoFrontier as pf
    lib_ = libs.librarian.librarian.librarian()

    data = lib_.get_data(20)
    fittest, dominated = pf.get_pareto_fittest(data, 10)

    # print(fittest, dominated)

    # frontiers, _ = pf.get_frontiers(data, 15)
    # print(frontiers)


    eidetic.plot(data= [fittest, dominated],
                 types= ["fittest", "dominated"],
                 file= "output.png",
                 labels=False,
                 tittle="UHUL")

    # eidetic.plot(data=frontiers,
    #              file="output2.png")




