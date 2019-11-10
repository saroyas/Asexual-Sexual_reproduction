#%%
import matplotlib.pyplot as plt
import matplotlib.animation
import seaborn as sns
import numpy as np
import json
#%%
with open('data.json', 'r') as fp:
    total_plot_data = json.load(fp)
    print('sucesfully loaded stuff')

def get_data(sex = True):
    data = {}
    if sex == True:
        for i in list(total_plot_data.keys()):
            k = int(i)
            data[k] = (total_plot_data[i])['sex']
    else:
        for i in list(total_plot_data.keys()):
            k = int(i)
            data[k] = (total_plot_data[i])['asex']
    return data
#%%
sex_data = get_data(sex = True)
asex_data = get_data(sex = False)

#%%

sex_data[1]

#%%

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0,0,1,1], frameon=False)
ax.set_xlim(10, 50)
ax.set_ylim(10, 50)

sex_plot = sns.kdeplot(sex_data[0][0], sex_data[0][1], cmap="Reds")
asex_plot = sns.kdeplot(asex_data[0][0], asex_data[0][1], cmap="Blues")


#%%

def animate(i):
    sex_plot = sns.kdeplot(sex_data[0][0], sex_data[0][1], cmap="Reds")
    asex_plot = sns.kdeplot(asex_data[0][0], asex_data[0][1], cmap="Blues")
    sex_plot.set_data(sex_data[i][0], sex_data[i][1])
    asex_plot.set_data(asex_data[i][0], asex_data[i][1])


frames=range(0,500)
ani = matplotlib.animation.FuncAnimation(fig, animate, frames=frames, repeat=True)

plt.show()