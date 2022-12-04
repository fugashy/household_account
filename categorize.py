# -*- coding: utf-8 -*-
from sys import argv
import math
import pandas as pd
import yaml
from pprint import pprint
import matplotlib.pyplot as plt

import plot

_CSV_COLUMN_NAMES=[
        'state',
        'date_pay',
        'store',
        'date_use',
        'count',
        'num',
        'cost',
        'unit',
        'unit_name',
        'rate']


if __name__ == "__main__":
    # set configulations up
    config_path = argv[1]
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    input_filepaths = config["input_filepaths"]
    category_db = config["categories"]

    # construct map for summarize
    cost_by_filename = dict()
    for input_filepath in input_filepaths:
        filename = input_filepath.split('/')[-1].split('.')[0]
        cost_by_filename[filename] = dict()
        for category in category_db:
            cost_by_filename[filename][category["name"]] = dict()
        cost_by_filename[filename]["other"] = dict()

    # merge cost that have the same store
    for input_filepath in input_filepaths:
        csv = pd.read_csv(
            input_filepath,
            encoding="shift_jis",
            names=_CSV_COLUMN_NAMES)
        filename = input_filepath.split('/')[-1].split('.')[0]
        print(f"---------- {filename} ----------")
        for row in csv.itertuples():
            try:
                cost = float(str(row.cost).replace(',', ''))
            except:
                continue
            if math.isnan(cost):
                continue

            # suppress AP/QP
            store = row.store.replace("ＡＰ／ＱＰ／", "")

            found = False
            for category in category_db:
                for value in category["values"]:
                    if value in store:
                        if store not in cost_by_filename[filename][category["name"]]:
                            cost_by_filename[filename][category["name"]][store] = 0.0
                        cost_by_filename[filename][category["name"]][store] += cost
                        found = True
                        break
                if found:
                    break

            if not found:
                print(f"{store} {cost} yen is categorized as other")
                if store not in cost_by_filename[filename]["other"]:
                    cost_by_filename[filename]["other"][store] = 0.0
                cost_by_filename[filename]["other"][store] += cost

    # make campas
    filenum = len(cost_by_filename.keys())
    category_num = len(cost_by_filename[list(cost_by_filename.keys())[0]].keys())

    fig = plt.figure(figsize=[10, 2.5 + (2.5 * filenum)])
    gs = fig.add_gridspec(1 + filenum, category_num)

    # plot sum
    ax1 = fig.add_subplot(gs[0, :])
    plot.plot_cost_by_category(ax1, cost_by_filename)

    # plot categories
    for i, filename in enumerate(sorted(cost_by_filename.keys())):
        store_value_by_category = cost_by_filename[filename]
        for j, category in enumerate(sorted(store_value_by_category.keys())):
            cost_map = store_value_by_category[category]
            ax = fig.add_subplot(gs[1 + i, j])
            plot.plot_cost_by_store(ax, category, cost_map)

    plt.subplots_adjust(wspace=0.2, hspace=0.5)

    fig.savefig("summary.png", dpi=300)
    print(f"output summary as summary.png")
