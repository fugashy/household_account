# -*- coding: utf-8 -*-
from sys import argv
import math
import pandas as pd
import yaml
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib


if __name__ == "__main__":
    config_path = argv[1]
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    input_filepaths = config["input_filepaths"]
    category_db = config["categories"]

    cost_by_filename = dict()
    for input_filepath in input_filepaths:
        filename = input_filepath.split('/')[-1].split('.')[0]
        cost_by_filename[filename] = dict()
        for category in category_db:
            cost_by_filename[filename][category["name"]] = 0.0
        cost_by_filename[filename]["other"] = 0.0

    for input_filepath in input_filepaths:
        csv = pd.read_csv(
            input_filepath,
            encoding="shift_jis",
            names=['state', 'date_pay', 'store', 'date_use', 'count', 'num', 'cost', 'unit', 'unit_name', 'rate'])
        filename = input_filepath.split('/')[-1].split('.')[0]
        for row in csv.itertuples():
            try:
                cost = float(str(row.cost).replace(',', ''))
            except:
                continue
            if math.isnan(cost):
                continue

            found = False
            for category in category_db:
                for value in category["values"]:
                    if value in row.store:
                        cost_by_filename[filename][category["name"]] += cost
                        found = True
                        break
                if found:
                    break

            if not found:
                print(f"{row.store} is categorized as other")
                cost_by_filename[filename]["other"] += cost


    pprint(cost_by_filename)

    fig, ax = plt.subplots(1)

    for i, filename in enumerate(cost_by_filename.keys()):
        e = cost_by_filename[filename]
        sum_cost = 0.0
        costs_to_plot = list()
        for category in e.keys():
            sum_cost += e[category]
            costs_to_plot.append(sum_cost)

        tuples = zip(reversed(costs_to_plot), matplotlib.colors.cnames.keys(), reversed(e.keys()))
        for cost, color, label in tuples:
            if i == 0:
                ax.bar(int(filename[2:]), cost, color=color, label=label)
            else:
                ax.bar(int(filename[2:]), cost, color=color)

    ax.legend(bbox_to_anchor=(1, 1), loc="upper left")
    plt.show()
