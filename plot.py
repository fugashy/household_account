# -*- coding: utf-8 -*-
import matplotlib
import japanize_matplotlib
import datetime


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
            # とりあえず1日を付与
            date_obj = datetime.datetime(int(filename[:4]), int(filename[4:]), 1).date()
            if i == 0:
                ax.bar(date_obj, cost, width=3.0, color=color, edgecolor="black", label=label)
            else:
                ax.bar(date_obj, cost, width=3.0, color=color, edgecolor="black")
        ax.text(int(filename[2:]), costs_to_plot[-1] / 2, int(costs_to_plot[-1]), va="center", ha="center")

    ax.grid()
    ax.legend(bbox_to_anchor=(0, 1), loc="lower left", ncol=category_num)


def plot_cost_by_store(ax, title, cost_map):
    values = [cost_map[key] for key in reversed(cost_map.keys())]
    labels = [key for key in reversed(cost_map.keys())]
    ax.pie(values, labels=labels, startangle=90, counterclock=False, textprops={"fontsize": 4})
    ax.set_title(f"{title}:{int(sum(values))}", fontsize=7)
