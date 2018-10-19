
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
                        colorbar = dict(thickness=50, x=0.75, len=0.5, title=barlabel),
                        size=5,
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

        # r = [ordered[-1, 0]]
        #
        # for i in range(1, ordered.shape[1]):
        #     r.append(ordered[0, i])

        r = []

        for value in norm_data.values():
            r.append(value[1])

        hypervolume = 0
        # print(ordered)

        for idx, item in enumerate(ordered):

            f_x0 = r[1]
            f_xi = item[1]
            xi = item[0]
            try:
                xi_1 = ordered[idx + 1][0]
            except IndexError:
                xi_1 = r[0]
            hypervolume += (xi_1 - xi) * (f_x0 - f_xi)

        return hypervolume

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

        # print(metrics)

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


if __name__ == "__main__":
    # pass

    import libs.librarian.librarian as l
    # import libs.paretoFrontier.paretoFrontier as pf
    lib = l.librarian_nsga()
    # lib2 = l.librarian_milenium()
    exp = lib.get_experiment_data(20)

    # exp = np.array(exp)

    # data = []
    #
    # for gen in exp:
    #
    #     aux = np.array(gen)
    #     # aux = aux[:,12:15]
    #
    #     (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(aux[:,:12],
    #                                                                                                           aux[:,
    #                                                                                                           12:15])
    #     data.append(objective_frontier)
    #     # print(aux)
    #
    # eidetic.plot_3D_no_id(data)

    # print(eidetic.get_hypervolume(exp[0], 2))

    # eidetic.plot_hypervolume_statistic(exp, 2)
    # eidetic.plot_hypervolume_statistic_normalized(exp, 2)
    # eidetic.plot_area_experiment_statistic(exp, [12,13])

    # best2 = lib2.get_benchmark_data(metrics = ['alm'])

    # traits, objectives = lib2.get()
    #
    # (trait_frontier, objective_frontier), (dominated_traits, dominated_objectives) = eidetic.get_frontier(traits, objectives)
    #
    # tranposed = objective_frontier.T[0]
    # indexes = tranposed.argsort()
    # ordered = objective_frontier[indexes]
    #
    # print(ordered)


    # print(traits, objectives)


    # best2, _ = pf.fast_non_dominated_sort(best2)

    # best2 = best2[:,1:]
    #
    # print(best2)
    #
    # best = np.array(exp[19])
    # #
    # best = best[:,12:14].astype(np.float)
    # #
    # eidetic.plot([best, best2])

    # eidetic.get_area(exp[0], [12,13])

    # eidetic.get_min_max(exp, 12)


    # eidetic.plot_area_experiment_statistic(exp, [12, 13])

    # print(eidetic.plot_max_experiment_statistic(exp, 13))



    # #
    # import libs.librarian.librarian
    # import libs.paretoFrontier.paretoFrontier as pf
    # lib_ = libs.librarian.librarian.librarian_milenium()
    #
    # data = lib_.get_benchmark_data(benchmark="adpcm", metrics=["alm", "memory", "ram"])
    # data = lib_.get_data(20)
    #
    # frontiers, a = pf.get_frontiers(data, 10)
    #
    # eidetic.plot_3D(frontiers)
    #
    #
    #
    # test = frontiers[0][:, 1:]
    # test2 = frontiers[1][:, 1:]
    # # print(test)
    #
    # result = []
    # for i, item in enumerate(test):
    #     previous_slice = test[:i, :]
    #     next_slice = test[i + 1:, :]
    #     candidate_less_space = np.vstack((previous_slice, next_slice))
    #     result.append((item < candidate_less_space).all(axis=1).all())
    # print(any(result))
    # #
    # # test2 = frontiers[1][:, 1:]
    # # # print(test)
    # #
    # # result = []
    # # for i, item in enumerate(test2):
    # #     previous_slice = test2[:i, :]
    # #     next_slice = test2[i + 1:, :]
    # #     candidate_less_space = np.vstack((previous_slice, next_slice))
    # #     # print(item)
    # #     result.append((item < candidate_less_space).all(axis=1).all())
    # # print(any(result))
    #
    # # print(test)
    #
    # # print(test)
    # for i, item in enumerate(test2):
    #     # print(item)
    #     print((item > test).all(axis=1).any())
    #
    #
    # # eidetic.plot_3D([data[0:100], data[101:200]])
    # # eidetic.plot_3D(frontiers)
    #
    #
    #
    # fittest, dominated = pf.get_pareto_fittest(data, 100)
    # eidetic.plot_3D([fittest, dominated], xlabel="quicksort", title="adpcm", ylabel="alm", zlabel="memory", barlabel="ram")
    #
    # # print(fittest, dominated)
    #
    # # frontiers, _ = pf.get_frontiers(data, 15)
    # # print(frontiers)
    #
    #
    # # eidetic.plot(data= [fittest, dominated],
    # #              types= ["fittest", "dominated"],
    # #              file= "output.png",
    # #              labels=False,
    # #              tittle="UHUL")
    #
    # # eidetic.plot(data=frontiers,
    # #              file="output2.png")
    #
    # # eidetic.plot_3Din2D(data=frontiers,
    # #                     file="output2.png")
    #
    #
    #
    #
