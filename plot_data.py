import matplotlib.pyplot as plt
import matplotlib.animation
import seaborn as sns
import numpy as np
import json
import time

with open('camera_roll.json', 'r') as fp:
    total_plot_data = json.load(fp)
    print('sucesfully loaded stuff')

def get_data(sex = True):
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

sex_data = get_data(sex = True)
asex_data = get_data(sex = False)
x, y = sex_data[0][0],sex_data[0][1]
g = sns.JointGrid(x, y, size=8)
a = int(input('Axis start:'))
b = int(input('Axis end:'))
lim = (a,b)

def prep_axes(g, xlim, ylim):
    g.ax_joint.clear()
    g.ax_joint.set_xlim(xlim)
    g.ax_joint.set_ylim(ylim)
    g.ax_marg_x.clear()
    g.ax_marg_x.set_xlim(xlim)
    g.ax_marg_y.clear()
    g.ax_marg_y.set_ylim(ylim)
    plt.setp(g.ax_marg_x.get_xticklabels(), visible=False)
    plt.setp(g.ax_marg_y.get_yticklabels(), visible=False)
    plt.setp(g.ax_marg_x.yaxis.get_majorticklines(), visible=False)
    plt.setp(g.ax_marg_x.yaxis.get_minorticklines(), visible=False)
    plt.setp(g.ax_marg_y.xaxis.get_majorticklines(), visible=False)
    plt.setp(g.ax_marg_y.xaxis.get_minorticklines(), visible=False)
    plt.setp(g.ax_marg_x.get_yticklabels(), visible=False)
    plt.setp(g.ax_marg_y.get_xticklabels(), visible=False)

def prep_clear(g):
    g.ax_joint.clear()
    g.ax_marg_y.clear()
    g.ax_marg_x.clear()

def animate(i):
    prep_axes(g, lim, lim)
    g.x, g.y = sex_data[i][0],sex_data[i][1]
    g.plot_joint(sns.kdeplot, cmap="Reds")
    g.plot_marginals(sns.kdeplot, color="r", shade=True)
    g.x, g.y = asex_data[i][0],asex_data[i][1]
    g.plot_joint(sns.kdeplot, cmap="Blues")
    g.plot_marginals(sns.kdeplot, color="b", shade=True)

def animate_scatter(i):
    print('Shot num:', i)
    time.sleep(1)
    prep_clear(g)
    g.x, g.y = sex_data[i][0],sex_data[i][1]
    g.plot_joint(plt.scatter, cmap="Reds")
    g.plot_marginals(sns.kdeplot, color="r", shade=True)
    g.x, g.y = asex_data[i][0],asex_data[i][1]
    g.plot_joint(plt.scatter, cmap="Blues")
    g.plot_marginals(sns.kdeplot, color="b", shade=True)

a = int(input('Frame range start:'))
b = int(input('Frame range end:'))
steps = int(input('Step size:'))
frames=range(a,b, steps)
ani = matplotlib.animation.FuncAnimation(g.fig, animate, frames=frames, repeat=True)

plt.show()


