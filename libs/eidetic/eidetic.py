
import numpy as np
import seaborn as sns; sns.set()
import plotly.offline as py
import plotly.graph_objs as go

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

    @staticmethod
    def plot_3D(data: list, types=None, file="output.png", labels=False, tittle="", xlabel="", ylabel="", zlabel=""):

        traces = []
        marker = [ "circle" ,  "square"]

        for idx, datum in enumerate(data):
            if idx == 0:
                traces.append(
                    go.Scatter3d(
                        text=datum[:, 4],
                        x=datum[:,1],
                        y=datum[:,2],
                        z=datum[:,3],
                        mode='markers',

                        marker=dict(
                            colorbar = dict(thickness=50, x=0.2),
                            symbol = marker[idx],
                            size=5,
                            color=datum[:, 7],  # set color to an array/list of desired values
                            # colorscale='Viridis',
                            line=dict(
                                color='black',
                                width=0.2
                            ),
                            opacity=0.7
                        )
                    ))
            else:
                traces.append(
                    go.Scatter3d(
                        text=datum[:, 4],
                        x=datum[:, 1],
                        y=datum[:, 2],
                        z=datum[:, 3],
                        mode='markers',

                        marker=dict(
                            colorbar=dict(thickness=50, x=0.2),
                            symbol=marker[idx],
                            size=5,
                            color=datum[:, 7],  # set color to an array/list of desired values
                            # colorscale='Viridis',
                            # line=dict(
                            #     color='black',
                            #     width=0.1
                            # ),
                            opacity=0.7
                        )
                    ))

        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )
        fig = go.Figure(data=traces, layout=layout)
        py.plot(fig, filename='simple-3d-scatter')




        # print(data[:,0])

        # for datum in data:
        #     print(datum)
        #     traces.append()

    @staticmethod
    def plot_3Din2D(data: list, types=None, file="output.png", labels=False, tittle="", xlabel="", ylabel=""):
        fig, ax = plt.subplots(figsize=(20, 10), ncols=2, nrows=1)

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

        sns.scatterplot(
            x= grouped[:,1],
            y= grouped[:,2],
            hue=hue,
            legend= "brief",
            palette=sns.color_palette( n_colors=colors),
            ax=ax[0]
        )


        for datum in data:
            for k in datum:
                ax[0].text(k[1],
                           k[2],
                           "{0:.0f}".format(k[0]),
                           family='sans-serif',
                           fontsize=15)
                ax[1].text(k[1],
                           k[3],
                           "{0:.0f}".format(k[0]),
                           family='sans-serif',
                           fontsize=15)

        sns.scatterplot(
            x= grouped[:,1],
            y= grouped[:,3],
            hue=hue,
            legend= "brief",
            palette=sns.color_palette( n_colors=colors),
            ax=ax[1]
        )



        plt.savefig(file)
        plt.clf()





if __name__ == "__main__":

    import libs.librarian.librarian
    import libs.paretoFrontier.paretoFrontier as pf
    lib_ = libs.librarian.librarian.librarian()

    data = lib_.get_benchmark_data(benchmark="adpcm", metrics=["quicksort", "sobel", "vecsum", "dotprod", "memory", "ram", "alm"])
    # data = lib_.get_data(20)

    # frontiers, _ = pf.get_frontiers(data, 2)



    # eidetic.plot_3D([data[0:100], data[101:200]])
    # eidetic.plot_3D(frontiers)



    fittest, dominated = pf.get_pareto_fittest(data, 500)
    eidetic.plot_3D([fittest, dominated])

    # print(fittest, dominated)

    # frontiers, _ = pf.get_frontiers(data, 15)
    # print(frontiers)


    # eidetic.plot(data= [fittest, dominated],
    #              types= ["fittest", "dominated"],
    #              file= "output.png",
    #              labels=False,
    #              tittle="UHUL")

    # eidetic.plot(data=frontiers,
    #              file="output2.png")

    # eidetic.plot_3Din2D(data=frontiers,
    #                     file="output2.png")




