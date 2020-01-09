import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import json
from matplotlib.animation import PillowWriter


def create_plot_file(frame_range, plot_asex=True, plot_sex=True, filename = 'trial_no_name'):
    with open('camera_roll.json', 'r') as fp:
        total_plot_data = json.load(fp)
        print('sucesfully loaded stuff')

    def get_data(sex=True):
        data = {}
        if sex == True:
            for i in list(total_plot_data.keys()):
                k = int(i)
                data[k] = (total_plot_data[i])[0]
        else:
            for i in list(total_plot_data.keys()):
                k = int(i)
                data[k] = (total_plot_data[i])[1]
        return data

    sex_data = get_data(sex=True)
    asex_data = get_data(sex=False)

    fig = plt.figure(figsize=(10, 10))

    total_min, total_max = 0, 0
    if plot_sex and plot_asex:
        total_min = np.min([np.min(sex_data[i]) for i in frame_range] + [np.min(asex_data[i]) for i in frame_range])
        total_max = np.max([np.max(sex_data[i]) for i in frame_range] + [np.max(asex_data[i]) for i in frame_range])

    if not plot_asex:
        total_min = np.min([np.min(sex_data[i]) for i in frame_range])
        total_max = np.max([np.max(sex_data[i]) for i in frame_range])
    if not plot_sex:
        total_min = np.min([np.min(asex_data[i]) for i in frame_range])
        total_max = np.max([np.max(asex_data[i]) for i in frame_range])

    def reset_plot():
        plt.clf()
        plt.xlabel('Loci 0', fontsize=20)
        plt.ylabel('Loci 1', fontsize=20)
        plt.xlim(total_min, total_max)
        plt.ylim(total_min, total_max)

    def animate(i):
        reset_plot()
        if plot_asex:
            asex_0, asex_1 = asex_data[i][0], asex_data[i][1]
            p = sns.kdeplot(asex_0, asex_1, cmap="Blues")
        if plot_sex:
            sex_0, sex_1 = sex_data[i][0], sex_data[i][1]
            p = sns.kdeplot(sex_0, sex_1, cmap="Reds")
        p.tick_params(labelsize=17)
        plt.setp(p.lines, linewidth=7)

    anim = matplotlib.animation.FuncAnimation(fig, animate, frames=frame_range, repeat=True)

    file_name = filename + '.gif'

    FFwriter = PillowWriter(fps=3)
    anim.save(file_name, writer=FFwriter)
