import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.animation import FuncAnimation
import time
import sqlite3
import seaborn as sns
connection = sqlite3.connect('data_db.db')
c = connection.cursor()

plt.xkcd()

fig = plt.figure(constrained_layout = True, figsize = (10,10))
spec = fig.add_gridspec( nrows = 2, ncols = 4, figure = fig)

f_ax1 = fig.add_subplot(spec[0, 0])
f_ax2 = fig.add_subplot(spec[0, 1])
f_ax3 = fig.add_subplot(spec[1, 0])
f_ax4 = fig.add_subplot(spec[1, 1])
f_ax5 = fig.add_subplot(spec[0:,2:])
list2 = []

i = 0
def animate(i):
	query = ('SELECT * FROM dice_values')
	data = pd.read_sql_query(query, connection)
	means = data["mean"]
	id = data["id"]

	f_ax1.cla()
	f_ax1.set_title('Histogram of means', size = 14, pad = 10)
	f_ax1.hist(means, density = True, bins = 10)

	f_ax2.cla()
	f_ax2.set_title('Probability Plot', size = 14, pad = 10)
	stats.probplot(means, dist = "norm", plot = f_ax2)

	f_ax3.cla()
	f_ax3.set_title('P values of Shapiro test', size = 14, pad = 10)
	if i >= 3:
		anno_opts = dict(xy = (0.5, 0.5), xycoords = 'axes fraction', va = 'center', ha = 'center',size = 15)
		f_ax3.annotate('{k}'.format(k = str(np.round(stats.shapiro(means)[1],2))), **anno_opts)
	f_ax3.axis('off')

	f_ax4.cla()
	f_ax4.set_title('Line chart of P values', size = 14, pad = 10)
	if i >= 3:
		query = ('SELECT * FROM p_values')
		p_value_df = pd.read_sql_query(query, connection)
		x = p_value_df["id"]
		y = p_value_df["p_value"]
		f_ax4.plot(x,y)

	f_ax5.cla()
	f_ax5.set_title('Distribution of output', size = 14, pad = 10)
	for i in range(1,data.shape[1]-1):
		list2.append(data.iloc[-1,i])
	sns.countplot(list2, ax = f_ax5)	
	










ani = FuncAnimation(fig, animate, interval = 500)

plt.show()	