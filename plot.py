# -*- coding: utf-8 -*-
import matplotlib
import japanize_matplotlib


def plot_cost_by_category(ax, cost_map):
    category_num = None
    for i, filename in enumerate(cost_map.keys()):
        e = cost_map[filename]
        sum_cost = 0.0
        costs_to_plot = list()
        for category in e.keys():
            if category_num is None:
                category_num = len(e.keys())
            for store in e[category].keys():
                sum_cost += e[category][store]
            costs_to_plot.append(sum_cost)

        tuples = zip(reversed(costs_to_plot), matplotlib.colors.cnames.keys(), reversed(e.keys()))
        for cost, color, label in tuples:
            if i == 0:
                ax.bar(int(filename[2:]), cost, color=color, label=label)
            else:
                ax.bar(int(filename[2:]), cost, color=color)
        ax.text(int(filename[2:]), costs_to_plot[-1] / 2, int(costs_to_plot[-1]), va="center", ha="center")

    ax.legend(bbox_to_anchor=(0, 1), loc="lower left", ncol=category_num)
    xvalues = [int(filename[2:]) for filename in cost_map.keys()]
    ax.set_xticks(range(min(xvalues), max(xvalues)+1, 1))


def plot_cost_by_store(ax, title, cost_map):
    values = [cost_map[key] for key in reversed(cost_map.keys())]
    labels = [key for key in reversed(cost_map.keys())]
    ax.pie(values, labels=labels, startangle=90, counterclock=False, textprops={"fontsize": 4})
    ax.set_title(f"{title}:{int(sum(values))}", fontsize=7)
