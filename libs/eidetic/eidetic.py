
import numpy as np
import seaborn as sns; sns.set()
import plotly.offline as py
import plotly.graph_objs as go
from pygmo import *
import statistics
import time

from matplotlib import pyplot as plt
plt.figure(figsize=(19, 10))

adpcm = (3765610, 985694)
vecsum = (244420, 64688)
sobel = (6299933, 1175491)
dotprod = (1620481, 54343)
quicksort = (6426917, 1175472)
alm = (2018, 1131)
memory = (964608, 811264)





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
            x= grouped[:,0],
            y= grouped[:,1],
            hue=hue,
            legend= "brief",
            palette=sns.color_palette( n_colors=colors),
        )

        if labels:
            for datum in data:
                for k in datum:
                    sns_plot.text(k[0],
                                  k[1],
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
    def plot_3D_with_colorbar(data: list, types=None, file="output.png", labels=False, title="", xlabel="", ylabel="", zlabel="",barlabel=""):

        traces = []
        marker = [ "circle" ,  "cross"]

        for idx, datum in enumerate(data):
            if idx == 0:
                traces.append(
                    go.Scatter3d(
                        text=datum[:, (datum.shape[1]-1)],
                        x=datum[:,1],
                        y=datum[:,2],
                        z=datum[:,3],
                        mode='markers',

                        marker=dict(
                            colorbar = dict(thickness=50, x=0.75, len=0.5, title=barlabel),
                            symbol = marker[idx],
                            size=5,
                            color=datum[:, (datum.shape[1]-1)],  # set color to an array/list of desired values
                            colorscale='Viridis',
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
                            symbol=marker[idx],
                            size=5,
                            color=datum[:, 4],  # set color to an array/list of desired values
                            # colorscale='Viridis',
                            # line=dict(
                            #     color='black',
                            #     width=0.1
                            # ),
                            opacity=0.7,
                            colorscale = 'Viridis',

                )
                    ))

        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
            title=title,
            scene=dict(
                xaxis=dict(
                    title=xlabel,
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title=ylabel,
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                zaxis=dict(
                    title=zlabel,
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
        )
        fig = go.Figure(data=traces, layout=layout)
        py.plot(fig, filename='simple-3d-scatter')




        # print(data[:,0])

        # for datum in data:
        #     print(datum)
        #     traces.append()

    @staticmethod
    def plot_3D(data: list, types=None, file="output.png", labels=False, title="", xlabel="", ylabel="", zlabel="",barlabel=""):

        traces = []

        for idx, datum in enumerate(data):
            traces.append(
                go.Scatter3d(
                    # text=datum[:, (datum.shape[1]-1)],
                    x=datum[:,1],
                    y=datum[:,2],
                    z=datum[:,3],
                    mode='markers',

                    marker=dict(
                        # colorbar = dict(thickness=50, x=0.75, len=0.5, title=barlabel),
                        # symbol = marker[idx],
                        size=5,
                        # color=datum[:, (datum.shape[1]-1)],  # set color to an array/list of desired values
                        colorscale='Viridis',
                        line=dict(
                            color='black',
                            width=0.2
                        ),
                        opacity=0.7
                    )
                ))


        layout = go.Layout(
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            ),
            title=title,
            scene=dict(
                xaxis=dict(
                    title=xlabel,
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                yaxis=dict(
                    title=ylabel,
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                ),
                zaxis=dict(
                    title=zlabel,
                    titlefont=dict(
                        family='Courier New, monospace',
                        size=18,
                        color='#7f7f7f'
                    )
                )
            )
        )
        fig = go.Figure(data=traces, layout=layout)
        py.plot(fig, filename='simple-3d-scatter')




        # print(data[:,0])

        # for datum in data:
        #     print(datum)
        #     traces.append()

    @staticmethod
    def plot_3D_no_id(data: list, types=None, file="output.png", labels=False, title="", xlabel="", ylabel="", zlabel="",barlabel=""):

        traces = []
        marker = [ "circle" ,  "cross"]

        for idx, datum in enumerate(data):

            traces.append(
                go.Scatter3d(
                    # text=datum[:, (datum.shape[1]-1)],
                    x=datum[:,0],
                    y=datum[:,1],
                    z=datum[:,2],
                    mode='markers',

                    marker=dict(
                        # colorbar = dict(thickness=50, x=0.75, len=0.5, title=barlabel),
                        size=5,
                        line=dict(
                            color='black',
                            width=0.2
                        ),
                        opacity=0.7
                    )
                ))


        # layout = go.Layout(
        #     margin=dict(
        #         l=0,
        #         r=0,
        #         b=0,
        #         t=0
        #     ),
        #     title=title,
        #     scene=dict(
        #         xaxis=dict(
        #             title=xlabel,
        #             titlefont=dict(
        #                 family='Courier New, monospace',
        #                 size=35,
        #                 color='#7f7f7f'
        #             )
        #         ),
        #         yaxis=dict(
        #             title=ylabel,
        #             titlefont=dict(
        #                 family='Courier New, monospace',
        #                 size=35,
        #                 color='#7f7f7f'
        #             )
        #         ),
        #         zaxis=dict(
        #             title=zlabel,
        #             titlefont=dict(
        #                 family='Courier New, monospace',
        #                 size=35,
        #                 color='#7f7f7f'
        #             )
        #         )
        #     )
        # )

        layout = go.Layout(
            scene=dict(
                xaxis=dict(
                    backgroundcolor="rgb(200, 200, 230)",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    # title=xlabel,
                    zerolinecolor="rgb(255, 255, 255)",
                    tickfont=dict(
                        size=15
                    ),
                    showaxeslabels = True,
                    titlefont = dict(
                        size = 20
                    )
                ),
                yaxis=dict(
                    backgroundcolor="rgb(230, 200,230)",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    # title=ylabel,
                    zerolinecolor="rgb(255, 255, 255)",
                    tickfont=dict(
                        size=15
                    ),
                    showaxeslabels=True,
                    titlefont=dict(
                        size=20
                    )
                ),
                zaxis=dict(
                    backgroundcolor="rgb(230, 230,200)",
                    gridcolor="rgb(255, 255, 255)",
                    showbackground=True,
                    # title=zlabel,
                    zerolinecolor="rgb(255, 255, 255)",
                    tickfont=dict(
                        size=15
                    ),
                    showaxeslabels=True,
                    titlefont=dict(
                        size=20
                    )
                )
            ),
            margin=dict(
                r=10, l=10,
                b=10, t=10),
            width=800,
            height=600
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

    #plotly methods
    @staticmethod
    def plot_mean_experiment_statistic(experiment, metric):

        means = []
        for generation in experiment:
            means.append(eidetic.get_mean(generation, metric))


        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=means
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

        return range(len(experiment)), means

    @staticmethod
    def plot_sum_experiment_statistic(experiment, metric):

        sums = []
        for generation in experiment:
            sums.append(eidetic.get_sum(generation, metric))


        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

        return range(len(experiment)), sums

    @staticmethod
    def plot_area_experiment_statistic(experiment, metrics):

        areas = []

        norm_data = {}
        for metric in metrics:
            norm_data[metric] = eidetic.get_min_max(experiment, metric)

        for generation in experiment:
            areas.append(eidetic.get_area(generation, norm_data))


        print(norm_data)


        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=areas
        )
        #
        data = [trace]
        py.plot(data, filename='basic-scatter')
        #
        # return range(len(experiment)), sums

    @staticmethod
    def plot_max_experiment_statistic(experiment, metric):

        sums = []
        for generation in experiment:
            sums.append(eidetic.get_max(generation, metric))


        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

        return range(len(experiment)), sums

    @staticmethod
    def plot_min_experiment_statistic(experiment, metric):

        sums = []
        for generation in experiment:
            sums.append(eidetic.get_min(generation, metric))


        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

        return range(len(experiment)), sums

    @staticmethod
    def get_mean(generation, metric):
        mean = 0
        for core in generation:
            mean += core[metric]
        return mean/len(generation)

    @staticmethod
    def get_sum(generation, metric):
        sum = 0
        for core in generation:
            sum += core[metric]
        return sum

    @staticmethod
    def get_area(generation, norm_data):

        area = 0
        metrics = norm_data.keys()

        print(metrics)

        for core in generation:
            mult_aux = 0
            for metric in metrics:
                value = float(core[metric])
                denominator = norm_data[metric][1] - norm_data[metric][0]
                normalized = (value - norm_data[metric][0])/denominator
                mult_aux += normalized
            area += mult_aux
        return area




        # print(np.amax(generation[12].astype(np.float)))

    @staticmethod
    def get_max(generation, metric):

        generation = np.array(generation)

        metric = generation.T[metric]
        metric = metric.astype(np.float)
        max = np.amax(metric)
        # min = np.amin(metric)

        return max

    @staticmethod
    def get_min(generation, metric):

        generation = np.array(generation)

        metric = generation.T[metric]
        metric = metric.astype(np.float)
        # max = np.amax(metric)
        min = np.amin(metric)

        return min

    @staticmethod
    def get_min_max(experiment, metric_idx):

        generation = np.array(experiment[0])

        metric = generation.T[metric_idx]
        metric = metric.astype(np.float)
        max = np.amax(metric)
        min = np.amin(metric)

        for generation in experiment[1:]:

            generation = np.array(generation)
            metric = generation.T[metric_idx]
            metric = metric.astype(np.float)
            max_aux = np.amax(metric)
            min_aux = np.amin(metric)

            if max_aux > max:
                max = max_aux
            if min_aux < min:
                min = min_aux

        return min, max

    @staticmethod
    def get_hypervolume(experiment, objective_num):

        experiment = np.array(experiment)

        traits = experiment[:,:12]
        objetives = experiment[:,12:12 + objective_num].astype(float)

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(traits,objetives)

        tranposed = objective_frontier.T[0]
        indexes = tranposed.argsort()
        ordered = objective_frontier[indexes]

        r = [ordered[-1, 0]]

        for i in range(1,ordered.shape[1]):
            r.append(ordered[0, i])


        hypervolume = 0
        # print(ordered)


        for idx, item in enumerate(ordered):

            f_x0 = r[1]
            f_xi = item[1]
            xi = item[0]
            try:
                xi_1 = ordered[idx+1][0]
            except IndexError:
                xi_1 = r[0]
            hypervolume += (xi_1-xi) * (f_x0 - f_xi)

        return hypervolume

    @staticmethod
    def get_hypervolume_normalized(experiment, objective_num, norm_data):

        experiment = np.array(experiment)

        traits = experiment[:, :12]
        objetives = experiment[:, 12:12 + objective_num].astype(float)

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(traits,
                                                                                                              objetives)
        tranposed = objective_frontier.T[0]
        indexes = tranposed.argsort()
        ordered = objective_frontier[indexes]

        r = []

        for value in norm_data.values():
            r.append(value[1])

        hypervolume = 0

        for idx, item in enumerate(ordered):

            xi = item[0]
            try:
                xi_1 = ordered[idx + 1][0]
            except IndexError:
                xi_1 = r[0]

            aux = (xi_1 - xi)

            for idx , element in enumerate(item[1:]):

                f_x0 = r[idx+1]
                f_xi = item[idx+1]

                print(f_x0, f_xi)

                aux *= (f_x0 - f_xi)

            hypervolume += aux


            # f_x0 = r[1]
            # f_xi = item[1]
            # xi = item[0]
            # try:
            #     xi_1 = ordered[idx + 1][0]
            # except IndexError:
            #     xi_1 = r[0]
            # hypervolume += (xi_1 - xi) * (f_x0 - f_xi)

        return hypervolume

    @staticmethod
    def get_hypervolume_normalized_pygmo(experiment, objective_num, r):

        experiment = np.array(experiment)

        traits = experiment[:, :12]
        objetives = experiment[:, 12:12 + objective_num].astype(float)

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(traits,
                                                                                                              objetives)
        hv = hypervolume(points=objective_frontier)

        # print(objective_frontier)

        return hv.compute(ref_point=r)


    @staticmethod
    def get_hypervolume_normalized_pygmo2(experiment, objective_num, r):



        experiment = np.array(experiment)

        traits = experiment[:, :12]
        objetives = experiment[:, 12:12 + objective_num].astype(float)

        objetives = eidetic.normalize_coll(objetives, 0, adpcm[1], adpcm[0])
        objetives = eidetic.normalize_coll(objetives, 1, alm[1], alm[0])
        objetives = eidetic.normalize_coll(objetives, 2, memory[1], memory[0])

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(traits,
                                                                                                              objetives)
        hv = hypervolume(points=objective_frontier)

        # print(objective_frontier)

        return hv.compute(ref_point=r)


    @staticmethod
    def get_frontier(trait_space: np.array, objective_space: np.array):

        trait_frontier = np.array(trait_space[0:1])
        objective_frontier = np.array(objective_space[0:1])

        for trait_candidate, objective_candidate in zip(trait_space[1:, ], objective_space[1:, ]):

            partial_objective_domination = (objective_candidate < objective_frontier)
            dominated_indexes = partial_objective_domination.all(axis=1)

            try:
                dominated_traits = np.vstack((dominated_traits, trait_frontier[dominated_indexes]))
                dominated_objectives = np.vstack((dominated_objectives, objective_frontier[dominated_indexes]))
            except UnboundLocalError:
                dominated_traits = trait_frontier[dominated_indexes]
                dominated_objectives = objective_frontier[dominated_indexes]

            trait_frontier = trait_frontier[~dominated_indexes]
            objective_frontier = objective_frontier[~dominated_indexes]

            will_go = partial_objective_domination.any(axis=1).all()

            if will_go:
                trait_frontier = np.vstack((trait_frontier, trait_candidate))
                objective_frontier = np.vstack((objective_frontier, objective_candidate))
            else:
                dominated_traits = np.vstack((dominated_traits, trait_candidate))
                dominated_objectives = np.vstack((dominated_objectives, objective_candidate))
        try:
            return (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives)
        except UnboundLocalError:
            return (trait_frontier, objective_frontier), (np.array([]), np.array([]))

        # for i in ordered:
        #     print(i)

    @staticmethod
    def plot_hypervolume_statistic(experiment, num_metrics):

        sums = []
        for generation in experiment:
            sums.append(eidetic.get_hypervolume(generation, num_metrics))


        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

    @staticmethod
    def plot_hypervolume_statistic_normalized(experiment, num_metrics):

        metrics = [12]

        for i in range(1, num_metrics):
            metrics.append(i+12)

        norm_data = {}
        for metric in metrics:
            norm_data[metric] = eidetic.get_min_max(experiment, metric)

        print(norm_data)

        sums = []
        for generation in experiment:
            sums.append(eidetic.get_hypervolume_normalized(generation, num_metrics, norm_data))

        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

    @staticmethod
    def plot_hypervolume_statistic_normalized_pygmo(experiment, num_metrics):

        metrics = [12]

        for i in range(1, num_metrics):
            metrics.append(i + 12)

        norm_data = {}
        for metric in metrics:
            norm_data[metric] = eidetic.get_min_max(experiment, metric)

        r = []
        for value in norm_data.values():
            r.append(value[1])

        print(r)

        sums = []
        for generation in experiment:
            sums.append(eidetic.get_hypervolume_normalized_pygmo(generation, num_metrics, r))

        # print(sums)

        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')

    @staticmethod
    def plot_hypervolume_statistic_normalized_pygmo2(experiment, num_metrics):

        # metrics = [12]
        #
        # for i in range(1, num_metrics):
        #     metrics.append(i + 12)
        #
        # norm_data = {}
        # for metric in metrics:
        #     norm_data[metric] = eidetic.get_min_max(experiment, metric)
        #
        # r = []
        # for value in norm_data.values():
        #     r.append(value[1])
        #
        # print(r)
        r = (1,1,1)


        sums = []

        for generation in experiment:




            sums.append(eidetic.get_hypervolume_normalized_pygmo2(generation, num_metrics, r))

        # print(sums)

        trace = go.Scatter(
            x=list(range(len(experiment))),
            y=sums
        )

        data = [trace]
        py.plot(data, filename='basic-scatter')






    @staticmethod
    def final_plot_2d(raw, labels, x_label, y_label):

        data = []
        for item, name in zip(raw,labels):
            # Create a trace
            trace = go.Scatter(
                x=item[:,0],
                y=item[:,1],
                mode='markers',
                name = name,
                marker = dict(
                    size=10,
                    opacity=0.5,
                    # color='rgba(255, 182, 193, .9)',
                    line=dict(
                        width=0.5,
                    )
                )
            )
            data.append(trace)

        layout = go.Layout(
            # title='Stats of USA States',
            hovermode='closest',
            xaxis=dict(
                title=x_label,
                # ticklen=5,
                # zeroline=False,
                # gridwidth=2,
            ),
            yaxis=dict(
                title=y_label,
                # ticklen=5,
                # gridwidth=2,
            ),
            showlegend=True
        )

        fig = go.Figure(data=data, layout=layout)
        # Plot and embed in ipython notebook!
        py.plot(fig, filename='basic-scatter')

        # or plot with: plot_url = py.plot(data, filename='basic-line')

    @staticmethod
    def final_plot_2d_line(raw, labels, x_label, y_label):

        data = []
        for item, name in zip(raw,labels):
            # Create a trace
            trace = go.Scatter(
                x=item[:,0],
                y=item[:,1],
                mode='lines',
                name = name,
                marker = dict(
                    size=10,
                    opacity=0.5,
                    # color='rgba(255, 182, 193, .9)',
                    line=dict(
                        width=0.5,
                    )
                )
            )
            data.append(trace)

        layout = go.Layout(
            # title='Stats of USA States',
            hovermode='closest',
            xaxis=dict(
                title=x_label,
                # ticklen=5,
                # zeroline=False,
                # gridwidth=2,
            ),
            yaxis=dict(
                title=y_label,
                # ticklen=5,
                # gridwidth=2,
            ),
            showlegend=True
        )

        fig = go.Figure(data=data, layout=layout)
        # Plot and embed in ipython notebook!
        py.plot(fig, filename='basic-scatter')

        # or plot with: plot_url = py.plot(data, filename='basic-line')

    @staticmethod
    def normalize_coll(data, col_num, min, max):

        denominator = max - min
        data[:, col_num] -= min
        data[:, col_num] /= denominator

        return data

    @staticmethod
    def bootstrap_hypervome(population, num, histogram = True):

        r = (1,1)

        objetivos = population[:, 12:14].astype(np.float)
        objetivos = eidetic.normalize_coll(objetivos, 0, adpcm[1], adpcm[0])
        objetivos = eidetic.normalize_coll(objetivos, 1, alm[1], alm[0])
        size = objetivos.shape[0]

        bootstrap_data = []

        for rodada in range(num):
            indexes = np.random.randint(size, size = size)
            bootstrap_objetivos = objetivos[indexes]
            hv = hypervolume(points=bootstrap_objetivos)
            bootstrap_data.append(hv.compute(ref_point=r))


        data = [go.Histogram(x=bootstrap_data)]
        std_d = statistics.stdev(bootstrap_data)
        mean = sum(bootstrap_data)/len(bootstrap_data)
        maxi = max(bootstrap_data)
        mini = min(bootstrap_data)

        print(maxi, mini, mean, std_d)

        if histogram:
            layout = go.Layout(shapes= [{'line': {'color': '#FF4500', 'dash': 'solid', 'width': 2},
                                          'type': 'line',
                                          'x0': mean,
                                          'x1': mean,
                                          'xref': 'x',
                                          'y0': -0.1,
                                          'y1': 1,
                                          'yref': 'paper'},
                                        {'line': {'color': '#FFA500', 'dash': 'solid', 'width': 2},
                                         'type': 'line',
                                         'x0': mean+std_d,
                                         'x1': mean+std_d,
                                         'xref': 'x',
                                         'y0': -0.1,
                                         'y1': 1,
                                         'yref': 'paper'},
                                        {'line': {'color': '#FFA500', 'dash': 'solid', 'width': 2},
                                         'type': 'line',
                                         'x0': mean-std_d,
                                         'x1': mean-std_d,
                                         'xref': 'x',
                                         'y0': -0.1,
                                         'y1': 1,
                                         'yref': 'paper'},
                                        ],
                               hovermode='closest',
                               xaxis=dict(
                                   title="Hipervolume",
                                   # ticklen=5,
                                   # zeroline=False,
                                   # gridwidth=2,
                               ),
                               yaxis=dict(
                                   title="Ocorrencia",
                                   # ticklen=5,
                                   # gridwidth=2,
                               ),
                               showlegend=False
                               )


            fig = go.Figure(data=data, layout=layout)

            py.plot(fig, filename='basic histogram')

        return bootstrap_data


    @staticmethod
    def bootstrap_hypervome_3d(population, num, aux, histogram = True):

        r = (1.0001,1.0001,1.0001)

        objetivos = population[:, 12:15].astype(np.float)


        if aux == 26:
            objetivos = eidetic.normalize_coll(objetivos, 0, adpcm[1], adpcm[0])
        if aux == 27:
            objetivos = eidetic.normalize_coll(objetivos, 0, sobel[1], sobel[0])
        if aux == 29:
            objetivos = eidetic.normalize_coll(objetivos, 0, dotprod[1], dotprod[0])
        if aux == 30:
            objetivos = eidetic.normalize_coll(objetivos, 0, vecsum[1], vecsum[0])
        if aux == 31:
            objetivos = eidetic.normalize_coll(objetivos, 0, quicksort[1], quicksort[0])

        objetivos = eidetic.normalize_coll(objetivos, 1, alm[1], alm[0])
        objetivos = eidetic.normalize_coll(objetivos, 2, memory[1], memory[0])
        size = objetivos.shape[0]

        bootstrap_data = []

        for rodada in range(num):
            indexes = np.random.randint(size, size = size)
            bootstrap_objetivos = objetivos[indexes]
            hv = hypervolume(points=bootstrap_objetivos)
            bootstrap_data.append(hv.compute(ref_point=r))


        data = [go.Histogram(x=bootstrap_data)]
        std_d = statistics.stdev(bootstrap_data)
        mean = sum(bootstrap_data)/len(bootstrap_data)
        maxi = max(bootstrap_data)
        mini = min(bootstrap_data)

        print(maxi, mini, mean, std_d)

        if histogram:
            layout = go.Layout(shapes= [{'line': {'color': '#FF4500', 'dash': 'solid', 'width': 2},
                                          'type': 'line',
                                          'x0': mean,
                                          'x1': mean,
                                          'xref': 'x',
                                          'y0': -0.1,
                                          'y1': 1,
                                          'yref': 'paper'},
                                        {'line': {'color': '#FFA500', 'dash': 'solid', 'width': 2},
                                         'type': 'line',
                                         'x0': mean+std_d,
                                         'x1': mean+std_d,
                                         'xref': 'x',
                                         'y0': -0.1,
                                         'y1': 1,
                                         'yref': 'paper'},
                                        {'line': {'color': '#FFA500', 'dash': 'solid', 'width': 2},
                                         'type': 'line',
                                         'x0': mean-std_d,
                                         'x1': mean-std_d,
                                         'xref': 'x',
                                         'y0': -0.1,
                                         'y1': 1,
                                         'yref': 'paper'},
                                        ],
                               hovermode='closest',
                               xaxis=dict(
                                   title="Hipervolume",
                                   # ticklen=5,
                                   # zeroline=False,
                                   # gridwidth=2,
                               ),
                               yaxis=dict(
                                   title="Ocorrencia",
                                   # ticklen=5,
                                   # gridwidth=2,
                               ),
                               showlegend=False
                               )


            fig = go.Figure(data=data, layout=layout)

            py.plot(fig, filename='basic histogram')

        return bootstrap_data, mean, std_d

        # print(objetivos[indexes])

        # print(indexes)

        # indexes = [True] * size
        #
        # for idx in indexes_to_remove:
        #     indexes[idx] = False
        #
        # print(indexes)


        # traits = traits[indexes]


        # hv = hypervolume(points=objective_frontier)

        # print(objective_frontier)

        # return hv.compute(ref_point=r)

        # (trait_frontier, objective_frontier), \
        # (dominated_traits, dominated_objectives) = \
        #     eidetic.get_frontier(
        #     population[:, :12],
        #         population[:, 12:14].astype(np.float))

if __name__ == "__main__":
    # pass

    import libs.librarian.librarian as l
    import libs.paretoFrontier.paretoFrontier as pf
    lib = l.librarian_nsga()
    lib2 = l.librarian_milenium()

    # 3, 6
    experiments_to_run = [14]



    #experiment 1: GERAR EVOLUÇÃO DO HYPERVOLUME NA AMOSTRAGEM ALEATORIA
    if 1 in experiments_to_run:
        mil = lib2.get_benchmark_data()
        evolution = []
        for i in range(0,1000,50):
            gen = mil[i: i+50]
            evolution.append(gen)
        eidetic.plot_hypervolume_statistic_normalized_pygmo(evolution, 2)

    # experiment 2: mil cores ADPCM fronteira de pareto
    if 2 in experiments_to_run:
        mil = np.array(lib2.get_benchmark_data())
        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(mil[:, :12], mil[:, 12:14].astype(np.float))

        objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])

        dominated_objectives = eidetic.normalize_coll(dominated_objectives, 0, adpcm[1], adpcm[0])
        dominated_objectives = eidetic.normalize_coll(dominated_objectives, 1, alm[1], alm[0])

        eidetic.final_plot_2d([dominated_objectives, objective_frontier],
                              labels=["Dominados", "Fronteira de Pareto"],
                              x_label="Cilcos de Máquina adpcm",
                              y_label="Uso de elementos lógicos")

    # bootstrap no mil 2 objetivos
    if 3 in experiments_to_run:

        mil = np.array(lib2.get_benchmark_data())
        mil_boot = eidetic.bootstrap_hypervome(mil, 100000, histogram=True)

    #plotar evolução hipervolumes do NSGA 2objetivos
    if 4 in experiments_to_run:

        mean = 0.9271273213894703
        std_d = 0.004158576127227285

        valid = [10, 16, 17, 18, 19]

        data = []

        for aux, val in enumerate(valid):

            exp = lib.get_experiment_data(val)
            exp = np.array(exp)
            to_plot = []

            for generation in exp:
                objetivos = generation[:, 12:14].astype(np.float)
                objetivos = eidetic.normalize_coll(objetivos, 0, adpcm[1], adpcm[0])
                objetivos = eidetic.normalize_coll(objetivos, 1, alm[1], alm[0])
                hv = hypervolume(points=objetivos)
                to_plot.append(hv.compute(ref_point=(1,1)))

            trace = go.Scatter(
                y=to_plot,
                x=list(range(20)),
                name= "Execução " +str(aux+1),
                line = dict(
                    # color=('rgb(205, 12, 24)'),
                    width=1)
            )

            data.append(trace)

        layout = go.Layout(shapes=[{'line': {'color': '#00FFFF', 'dash': 'dashdot', 'width': 2},
                                    'type': 'line',
                                    'x0': -0.1,
                                    'x1': 19,
                                    'xref': 'x',
                                    'y0': mean,
                                    'y1': mean,
                                    'yref': 'y'},
                                   {'line': {'color': '#0000FF', 'dash': 'dashdot', 'width': 2},
                                    'type': 'line',
                                    'x0': -0.1,
                                    'x1': 19,
                                    'xref': 'x',
                                    'y0': mean + std_d,
                                    'y1': mean + std_d,
                                    'yref': 'y'},
                                   {'line': {'color': '#0000FF', 'dash': 'dashdot', 'width': 2},
                                    'type': 'line',
                                    'x0': -0.1,
                                    'x1': 19,
                                    'xref': 'x',
                                    'y0': mean - std_d,
                                    'y1': mean - std_d,
                                    'yref': 'y'},
                                   ],
                           hovermode='closest',
                           xaxis=dict(
                               title="Geração",
                               # ticklen=5,
                               # zeroline=False,
                               # gridwidth=2,
                           ),
                           yaxis=dict(
                               title="Hipervolume",
                               # ticklen=5,
                               # gridwidth=2,
                           ),
                           showlegend=True
                           )

        fig = go.Figure(data=data, layout=layout)

        py.plot(fig, filename='basic-scatter')

    # histogramas do bootstrap hipervolume para ultimas geraçoes do NSGA 2 obj
    if 5 in experiments_to_run:

        valid = [10,16,17,18,19]
        data = []
        mean = 0.9271273213894703
        std_d = 0.004158576127227285

        for auxaux, val in enumerate(valid):

            exp = lib.get_experiment_data(val)[-1]
            exp = np.array(exp)

            data.append(go.Histogram(x=eidetic.bootstrap_hypervome(exp, 100000, histogram=False),
                                     name= "Execução "+ str(auxaux+1)))

        layout = go.Layout(shapes= [{'line': {'color': '#FF4500', 'dash': 'dashdot', 'width': 2},
                                          'type': 'line',
                                          'x0': mean,
                                          'x1': mean,
                                          'xref': 'x',
                                          'y0': -0.1,
                                          'y1': 1,
                                          'yref': 'paper'},
                                        {'line': {'color': '#FFA500', 'dash': 'dashdot', 'width': 2},
                                         'type': 'line',
                                         'x0': mean+std_d,
                                         'x1': mean+std_d,
                                         'xref': 'x',
                                         'y0': -0.1,
                                         'y1': 1,
                                         'yref': 'paper'},
                                        {'line': {'color': '#FFA500', 'dash': 'dashdot', 'width': 2},
                                         'type': 'line',
                                         'x0': mean-std_d,
                                         'x1': mean-std_d,
                                         'xref': 'x',
                                         'y0': -0.1,
                                         'y1': 1,
                                         'yref': 'paper'},
                                        ],
                          hovermode='closest',
                          xaxis=dict(
                              title="Hipervolume",
                              # ticklen=5,
                              # zeroline=False,
                              # gridwidth=2,
                          ),
                          yaxis=dict(
                              title="Ocorrencia",
                              # ticklen=5,
                              # gridwidth=2,
                          ),
                          showlegend=True
                          )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='basic histogram')

    #boxplot bootstrap mil vs 5 NSGA 2 obj
    if 6 in experiments_to_run:

        valid = [10,16,17,18,19]
        data = [go.Box(y=mil_boot,
                               boxpoints=False,
                               name="Mil cores",
                               # jitter=0.3,
                               # pointpos=-1.8
                               )]

        for aux, val in enumerate(valid):

            exp = lib.get_experiment_data(val)[-1]
            exp = np.array(exp)

            data.append(go.Box(y=eidetic.bootstrap_hypervome(exp, 1000, histogram=False),
                               boxpoints=False,
                               name= "NSGA " + str(aux+1)
                               # jitter=0.3,
                               # pointpos=-1.8
                               ))

        layout = go.Layout(
            yaxis=dict(
                title="Hipervolume",
                # ticklen=5,
                # gridwidth=2,
            )
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='simple-3d-scatter')

        py.plot(fig)

    # fronteira de pareto NSGA 2 obj vs mil
    if 7 in experiments_to_run:

        mil = np.array(lib2.get_benchmark_data())
        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(
            mil[:, :12], mil[:, 12:14].astype(np.float))

        objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])

        data = [objective_frontier]

        print(data)
        # valid = [10, 16, 17, 18, 19]
        valid = [10, 16, 17]

        for val in valid:

            exp = lib.get_experiment_data(val)[-1]
            exp = np.array(exp)

            (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(
                exp[:, :12], exp[:, 12:14].astype(np.float))

            objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
            objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])

            data.append(objective_frontier)

        eidetic.final_plot_2d(data,
                              # labels=["Mil cores", "NSGA 1","NSGA 2","NSGA 3","NSGA 4","NSGA 5"],
                              labels=["Mil cores", "NSGA 1","NSGA 2"],
                              x_label="Cilcos de Máquina adpcm",
                              y_label="Uso de elementos lógicos"
                              )


    ############################## 3 obj ######################################

    #fronteira de pareto mil cores adpcm 3 obj
    if 8 in experiments_to_run:

        mil = np.array(lib2.get_benchmark_data())

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(
            mil[:, :12], mil[:, 12:15].astype(np.float))

        objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 2, memory[1], memory[0])

        dominated_objectives = eidetic.normalize_coll(dominated_objectives, 0, adpcm[1], adpcm[0])
        dominated_objectives = eidetic.normalize_coll(dominated_objectives, 1, alm[1], alm[0])
        dominated_objectives = eidetic.normalize_coll(dominated_objectives, 2, memory[1], memory[0])

        eidetic.plot_3D_no_id(data = [dominated_objectives,objective_frontier],
                              xlabel= "Ciclos de Máquina ADPCM",
                              ylabel= "Unidades Lógicas",
                              zlabel= "Unidades de Memória")

    #fronteira pareto mil cores + NSGA
    if 9 in experiments_to_run:
        mil = np.array(lib2.get_benchmark_data())

        data = []

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(
            mil[:, :12], mil[:, 12:15].astype(np.float))

        objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 2, memory[1], memory[0])

        data.append(objective_frontier)

        exp = lib.get_experiment_data(26)[-1]
        exp = np.array(exp)

        (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(
            exp[:, :12], exp[:, 12:15].astype(np.float))

        objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])
        objective_frontier = eidetic.normalize_coll(objective_frontier, 2, memory[1], memory[0])

        # data.append(objective_frontier)

        data.append(objective_frontier)


        eidetic.plot_3D_no_id(data=data,
                              xlabel="Ciclos de Máquina ADPCM",
                              ylabel="Unidades Lógicas",
                              zlabel="Unidades de Memória")

    # evolução NSGA 3 obj
    if 10 in experiments_to_run:

        data = []
        valid = [26, 27, 29, 30, 31]

        for aux, val in enumerate(valid):

            exp = lib.get_experiment_data(val)
            exp = np.array(exp)
            to_plot = []
            # print(len(exp))

            for generation in exp:
                # print(generation)

                objetivos = generation[:, 12:15].astype(np.float)
                if aux == 0:
                    objetivos = eidetic.normalize_coll(objetivos, 0, adpcm[1], adpcm[0])
                    nomeco = "adpcm"
                if aux == 1:
                    objetivos = eidetic.normalize_coll(objetivos, 0, sobel[1], sobel[0])
                    nomeco = "sobel"
                if aux == 2:
                    objetivos = eidetic.normalize_coll(objetivos, 0, dotprod[1], dotprod[0])
                    nomeco = "dotprod"
                if aux == 3:
                    objetivos = eidetic.normalize_coll(objetivos, 0, vecsum[1], vecsum[0])
                    nomeco = "vecsum"
                if aux == 4:
                    objetivos = eidetic.normalize_coll(objetivos, 0, quicksort[1], quicksort[0])
                    nomeco = "quicksort"

                objetivos = eidetic.normalize_coll(objetivos, 1, alm[1], alm[0])
                objetivos = eidetic.normalize_coll(objetivos, 2, memory[1], memory[0])

                hv = hypervolume(points=objetivos)
                to_plot.append(hv.compute(ref_point=(1, 1, 1)))

            trace = go.Scatter(
                y=to_plot,
                x=list(range(30)),
                name= nomeco,
                line=dict(
                    # color=('rgb(205, 12, 24)'),
                    width=1)
            )

            data.append(trace)

        layout = go.Layout(
                           hovermode='closest',
                           xaxis=dict(
                               title="Geração",
                               # ticklen=5,
                               # zeroline=False,
                               # gridwidth=2,
                           ),
                           yaxis=dict(
                               title="Hipervolume",
                               # ticklen=5,
                               # gridwidth=2,
                           ),
                           showlegend=True
                           )

        fig = go.Figure(data=data, layout=layout)

        py.plot(fig, filename='basic-scatter')

    # histograma mil vs nsga
    if 11 in experiments_to_run:

        valid = [26, 27, 29, 30, 31]
        # valid = [26, 27]

        for val in valid:

            data = []
            exp = lib.get_experiment_data(val)[-1]

            if val == 26:
                mil = np.array(lib2.get_benchmark_data())
            if val == 27:
                mil = np.array(lib2.get_benchmark_data(benchmark="sobel"))
            if val == 29:
                mil = np.array(lib2.get_benchmark_data(benchmark="dotprod"))
            if val == 30:
                mil = np.array(lib2.get_benchmark_data(benchmark="vecsum"))
            if val == 31:
                mil = np.array(lib2.get_benchmark_data(benchmark="quicksort"))


            mil_boot, mil_mean, mil_std = eidetic.bootstrap_hypervome_3d(mil, 100000, val, histogram=False)
            exp = np.array(exp)
            nsga_boot, nsga_mean, nsga_std = eidetic.bootstrap_hypervome_3d(exp, 100000, val, histogram=False)


            data.append(go.Histogram(x=mil_boot,
                                     name="Mil Cores",
                                     opacity=0.75)
                        ),
            data.append(go.Histogram(x=nsga_boot,
                                     name="NSGA",
                                     opacity=0.75)
                        )

            layout = go.Layout(
                hovermode='closest',
                xaxis=dict(
                    title="Hipervolume",
                ),
                yaxis=dict(
                    title="Ocorrencia",
                ),
                showlegend=True,
                barmode='overlay',
                shapes=[{'line': {'color': '#0000FF', 'dash': 'dashdot', 'width': 2},
                         'type': 'line',
                         'x0': mil_mean,
                         'x1': mil_mean,
                         'xref': 'x',
                         'y0': -0.1,
                         'y1': 1,
                         'yref': 'paper'},
                        {'line': {'color': '#00BFFF', 'dash': 'dashdot', 'width': 2},
                         'type': 'line',
                         'x0': mil_mean + mil_std,
                         'x1': mil_mean + mil_std,
                         'xref': 'x',
                         'y0': -0.1,
                         'y1': 1,
                         'yref': 'paper'},
                        {'line': {'color': '#00BFFF', 'dash': 'dashdot', 'width': 2},
                         'type': 'line',
                         'x0': mil_mean - mil_std,
                         'x1': mil_mean - mil_std,
                         'xref': 'x',
                         'y0': -0.1,
                         'y1': 1,
                         'yref': 'paper'},
                        {'line': {'color': '#DC143C', 'dash': 'dashdot', 'width': 2},
                         'type': 'line',
                         'x0': nsga_mean,
                         'x1': nsga_mean,
                         'xref': 'x',
                         'y0': -0.1,
                         'y1': 1,
                         'yref': 'paper'},
                        {'line': {'color': '#8B0000', 'dash': 'dashdot', 'width': 2},
                         'type': 'line',
                         'x0': nsga_mean + nsga_std,
                         'x1': nsga_mean + nsga_std,
                         'xref': 'x',
                         'y0': -0.1,
                         'y1': 1,
                         'yref': 'paper'},
                        {'line': {'color': '#8B0000', 'dash': 'dashdot', 'width': 2},
                         'type': 'line',
                         'x0': nsga_mean - nsga_std,
                         'x1': nsga_mean - nsga_std,
                         'xref': 'x',
                         'y0': -0.1,
                         'y1': 1,
                         'yref': 'paper'},
                        ],
            )
            fig = go.Figure(data=data, layout=layout)
            py.plot(fig, filename='basic histogram')

    #box plot
    if 12 in experiments_to_run:

        valid = [26, 27, 29, 30, 31]
        # valid = [26, 27]
        boot_num = 100000

        y_m = []
        x_m = []

        y_n = []
        x_n = []

        for val in valid:

            data = []
            exp = lib.get_experiment_data(val)[-1]

            if val == 26:
                mil = np.array(lib2.get_benchmark_data())
                x_m += ['adpcm'] * boot_num
                x_n += ['adpcm'] * boot_num
            if val == 27:
                mil = np.array(lib2.get_benchmark_data(benchmark="sobel"))
                x_m += ['sobel'] * boot_num
                x_n += ['sobel'] * boot_num
            if val == 29:
                mil = np.array(lib2.get_benchmark_data(benchmark="dotprod"))
                x_m += ['dotprod'] * boot_num
                x_n += ['dotprod'] * boot_num
            if val == 30:
                mil = np.array(lib2.get_benchmark_data(benchmark="vecsum"))
                x_m += ['vecsum'] * boot_num
                x_n += ['vecsum'] * boot_num
            if val == 31:
                mil = np.array(lib2.get_benchmark_data(benchmark="quicksort"))
                x_m += ['quicksort'] * boot_num
                x_n += ['quicksort'] * boot_num

            mil_boot, mil_mean, mil_std = eidetic.bootstrap_hypervome_3d(mil, boot_num, val, histogram=False)
            exp = np.array(exp)
            nsga_boot, nsga_mean, nsga_std = eidetic.bootstrap_hypervome_3d(exp, boot_num, val, histogram=False)

            y_m += mil_boot
            y_n += nsga_boot




        trace0 = go.Box(
            boxpoints=False,
            y= y_m,
            x= x_m,
            name='Mil Cores',
            marker=dict(
                color='#3D9970'
            )
        )

        trace1 = go.Box(
            boxpoints=False,
            y= y_n,
            x= x_n,
            name='NSGA',
            marker=dict(
                color='#FF4136'
            )
        )

        data = [trace0, trace1]

        layout = dict(
            # 'xaxis': {
            #     'title': 'normalized moisture',
            #     'zeroline': False,
            # },
            boxmode= 'group',
            yaxis=dict(
                title="Hipervolume",
                # ticklen=5,
                # gridwidth=2,
            ),
            xaxis = dict(
                title="Kernel",
                # ticklen=5,
                # gridwidth=2,
            )
        )


        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='basic histogram')

    #melhora abs 2obj
    if 13 in experiments_to_run:

        valid = [10, 16, 17, 18, 19]
        # valid = [19]

        for aux, val in enumerate(valid):

            exp = lib.get_experiment_data(val)
            exp = np.array(exp)


            primeira_gen = exp[0]
            ultima_gen = exp[-1]

            (_, primeira_frontier), (_, _) = eidetic.get_frontier(
                primeira_gen[:, :12], primeira_gen[:, 12:14].astype(np.float))

            (_, ultima_frontier), (_, _) = eidetic.get_frontier(
                ultima_gen[:, :12], ultima_gen[:, 12:14].astype(np.float))

            # print(primeira_gen_objetivos)
            # print(ultima_gen_objetivos)

            tranposed = primeira_frontier.T[0]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = primeira_frontier[indexes]

            primeira_ponta = aux_primeira_gen_objetivos[0]
            # primeiro_meio = aux_primeira_gen_objetivos[int(aux_primeira_gen_objetivos.shape[0]/2)]

            tranposed = primeira_frontier.T[1]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = primeira_frontier[indexes]

            segunda_ponta = aux_primeira_gen_objetivos[0]

            # print(primeira_ponta, segunda_ponta, primeiro_meio)


            tranposed = ultima_frontier.T[0]
            indexes = tranposed.argsort()
            aux_ultima_gen_objetivos = ultima_frontier[indexes]

            primeira_ponta_2 = aux_ultima_gen_objetivos[0]
            # segundo_meio = aux_ultima_gen_objetivos[int(aux_ultima_gen_objetivos.shape[0] / 2)]

            tranposed = ultima_frontier.T[1]
            indexes = tranposed.argsort()
            aux_ultima_gen_objetivos = ultima_frontier[indexes]

            segunda_ponta_2 = aux_ultima_gen_objetivos[0]

            # print(primeira_ponta_2, segunda_ponta_2, segundo_meio)

            print(val)
            print('\nprimeira ponta')
            print(primeira_ponta)
            print(primeira_ponta_2)

            print('\nsegunda ponta')

            print(segunda_ponta)
            print(segunda_ponta_2)

            print('\n------------\n')
            print(primeira_ponta_2/primeira_ponta)
            print(segunda_ponta_2/segunda_ponta)
            # print(segundo_meio/primeiro_meio)

            print('\n\n')


            # for generation in exp:

                # objetivos = generation[:, 12:14].astype(np.float)
                # objetivos = eidetic.normalize_coll(objetivos, 0, adpcm[1], adpcm[0])
                # objetivos = eidetic.normalize_coll(objetivos, 1, alm[1], alm[0])

                # hv = hypervolume(points=objetivos)

                # to_plot.append(hv.compute(ref_point=(1,1)))

    #melhora abs 3obj
    if 14 in experiments_to_run:

        # valid = [26]
        valid = [26, 27, 29, 30, 31]

        for aux, val in enumerate(valid):

            exp = lib.get_experiment_data(val)
            exp = np.array(exp)

            # print(exp)

            primeira_gen = exp[0]
            ultima_gen = exp[-1]

            (_, primeira_frontier), (_, _) = eidetic.get_frontier(
                primeira_gen[:, :12], primeira_gen[:, 12:15].astype(np.float))

            (_, ultima_frontier), (_, _) = eidetic.get_frontier(
                ultima_gen[:, :12], ultima_gen[:, 12:15].astype(np.float))


            tranposed = primeira_frontier.T[0]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = primeira_frontier[indexes]
            primeira_ponta = aux_primeira_gen_objetivos[0]

            tranposed = primeira_frontier.T[1]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = primeira_frontier[indexes]
            segunda_ponta = aux_primeira_gen_objetivos[0]
            #
            tranposed = primeira_frontier.T[2]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = primeira_frontier[indexes]
            terceira_ponta = aux_primeira_gen_objetivos[0]

            tranposed = ultima_frontier.T[0]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = ultima_frontier[indexes]
            primeira_ponta_2 = aux_primeira_gen_objetivos[0]

            tranposed = ultima_frontier.T[1]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = ultima_frontier[indexes]
            segunda_ponta_2 = aux_primeira_gen_objetivos[0]

            tranposed = ultima_frontier.T[2]
            indexes = tranposed.argsort()
            aux_primeira_gen_objetivos = ultima_frontier[indexes]
            terceira_ponta_2 = aux_primeira_gen_objetivos[0]
            #
            print(val)
            print(primeira_ponta_2/primeira_ponta)
            print(segunda_ponta_2/segunda_ponta)
            print(terceira_ponta_2/terceira_ponta)

            print('\n\n')

    #plota primeira e ultima 2obj
    if 15 in experiments_to_run:


        valid = [10, 16, 17, 18, 19]
        # valid = [19]

        for aux, val in enumerate(valid):
            time.sleep(1)
            exp = lib.get_experiment_data(val)
            exp = np.array(exp)

            # print(exp)

            primeira_gen = exp[0]
            ultima_gen = exp[-1]

            # primeira_gen_objetivos = primeira_gen[:, 12:14].astype(np.float)
            # ultima_gen_objetivos = ultima_gen[:, 12:14].astype(np.float)

            (_, primeira_frontier), (_, _) = eidetic.get_frontier(
                primeira_gen[:, :12], primeira_gen[:, 12:14].astype(np.float))

            (_, ultima_frontier), (_, _) = eidetic.get_frontier(
                ultima_gen[:, :12], ultima_gen[:, 12:14].astype(np.float))

            # primeira_frontier = eidetic.normalize_coll(primeira_frontier, 0, adpcm[1], adpcm[0])
            # primeira_frontier = eidetic.normalize_coll(primeira_frontier, 1, alm[1], alm[0])

            # ultima_frontier = eidetic.normalize_coll(ultima_frontier, 0, adpcm[1], adpcm[0])
            # ultima_frontier = eidetic.normalize_coll(ultima_frontier, 1, alm[1], alm[0])

            eidetic.final_plot_2d([primeira_frontier, ultima_frontier],
                                  labels=["primeira", "ultima"],
                                  x_label="Cilcos de Máquina adpcm",
                                  y_label="Uso de elementos lógicos")







    # mil = np.array(lib2.get_benchmark_data(benchmark='quicksort'))
    #
    # (trait_frontier, aaa), (dominated_traits, dominated_objectives) = eidetic.get_frontier(mil[:, :12], mil[:, 12:15])
    # #     data.append(objective_frontier)
    #
    #
    # # eidetic.plot_3D_no_id([objective_frontier])
    #
    #
    # #
    # #
    # #
    # exp = lib.get_experiment_data(26)

    # exp = np.array(exp)
    #
    # data = []
    # #
    # for gen in exp:
    #
    #     aux = np.array(gen)
    #     # aux = aux[:,12:15]
    #
    #     (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(aux[:,:12],aux[:,12:15].astype(np.float))
    #
    #     objective_frontier = eidetic.normalize_coll(objective_frontier, 0, adpcm[1], adpcm[0])
    #     objective_frontier = eidetic.normalize_coll(objective_frontier, 1, alm[1], alm[0])
    #     objective_frontier = eidetic.normalize_coll(objective_frontier, 2, memory[1], memory[0])
    #
    #     data.append(objective_frontier)

        # print(objective_frontier.shape)
        # print(aux)

    # data.append(aaa)

    # eidetic.plot_3D_no_id(data)

    # # eidetic.plot(data, file='a.png')
    #
    # print(eidetic.plot_hypervolume_statistic_normalized_pygmo2(exp, 3))
    #
    # # eidetic.plot_hypervolume_statistic(exp, 2)
    # # eidetic.plot_hypervolume_statistic_normalized(exp, 2)
    # # eidetic.plot_area_experiment_statistic(exp, [12,13])
    #
    # # best2 = lib2.get_benchmark_data(metrics = ['alm'])
    #
    # # traits, objectives = lib2.get()
    # #
    # # (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(traits, objectives)
    # #
    # # tranposed = objective_frontier.T[0]
    # # indexes = tranposed.argsort()
    # # ordered = objective_frontier[indexes]
    # #
    # # print(ordered)
    #
    #
    # # print(traits, objectives)
    #
    #
    # # best2, _ = pf.fast_non_dominated_sort(best2)
    #
    # # best2 = best2[:,1:]
    # #
    # # print(best2)
    # #
    # # best = np.array(exp[19])
    # # #
    # # best = best[:,12:14].astype(np.float)
    # # #
    # # eidetic.plot([best, best2])
    #
    # # eidetic.get_area(exp[0], [12,13])
    #
    # # eidetic.get_min_max(exp, 12)
    #
    #
    # # eidetic.plot_area_experiment_statistic(exp, [12, 13])
    #
    # # print(eidetic.plot_max_experiment_statistic(exp, 13))
    #
    #
    #
    # # #
    # # import libs.librarian.librarian
    # # import libs.paretoFrontier.paretoFrontier as pf
    # # lib_ = libs.librarian.librarian.librarian_milenium()
    # #
    # # data = lib_.get_benchmark_data(benchmark="adpcm", metrics=["alm", "memory", "ram"])
    # # data = lib_.get_data(20)
    # #
    # # frontiers, a = pf.get_frontiers(data, 10)
    # #
    # # eidetic.plot_3D(frontiers)
    # #
    # #
    # #
    # # test = frontiers[0][:, 1:]
    # # test2 = frontiers[1][:, 1:]
    # # # print(test)
    # #
    # # result = []
    # # for i, item in enumerate(test):
    # #     previous_slice = test[:i, :]
    # #     next_slice = test[i + 1:, :]
    # #     candidate_less_space = np.vstack((previous_slice, next_slice))
    # #     result.append((item < candidate_less_space).all(axis=1).all())
    # # print(any(result))
    # # #
    # # # test2 = frontiers[1][:, 1:]
    # # # # print(test)
    # # #
    # # # result = []
    # # # for i, item in enumerate(test2):
    # # #     previous_slice = test2[:i, :]
    # # #     next_slice = test2[i + 1:, :]
    # # #     candidate_less_space = np.vstack((previous_slice, next_slice))
    # # #     # print(item)
    # # #     result.append((item < candidate_less_space).all(axis=1).all())
    # # # print(any(result))
    # #
    # # # print(test)
    # #
    # # # print(test)
    # # for i, item in enumerate(test2):
    # #     # print(item)
    # #     print((item > test).all(axis=1).any())
    # #
    # #
    # # # eidetic.plot_3D([data[0:100], data[101:200]])
    # # # eidetic.plot_3D(frontiers)
    # #
    # #
    # #
    # # fittest, dominated = pf.get_pareto_fittest(data, 100)
    # # eidetic.plot_3D([fittest, dominated], xlabel="quicksort", title="adpcm", ylabel="alm", zlabel="memory", barlabel="ram")
    # #
    # # # print(fittest, dominated)
    # #
    # # # frontiers, _ = pf.get_frontiers(data, 15)
    # # # print(frontiers)
    # #
    # #
    # # # eidetic.plot(data= [fittest, dominated],
    # # #              types= ["fittest", "dominated"],
    # # #              file= "output.png",
    # # #              labels=False,
    # # #              tittle="UHUL")
    # #
    # # # eidetic.plot(data=frontiers,
    # # #              file="output2.png")
    # #
    # # # eidetic.plot_3Din2D(data=frontiers,
    # # #                     file="output2.png")
    # #
    # #
    # #
    # #
