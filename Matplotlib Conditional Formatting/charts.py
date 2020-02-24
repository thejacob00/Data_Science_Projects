# Use the following data for this assignment:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])
df = df.T
xax = np.arange(4)
means = df.mean()
st_devs = df.std()

moe = st_devs/(len(df.index)**0.5)*1.96

y = 43000
mask_blue = means + moe < y
mask_red = means - moe > y
mask_white = (means + moe >= y) & (means - moe <= y)

plt.clf()
plt.bar(xax[mask_blue], means.values[mask_blue], color='blue', edgecolor='black', yerr=moe[mask_blue])
plt.bar(xax[mask_red], means.values[mask_red], color='red', edgecolor='black', yerr=moe[mask_red])
plt.bar(xax[mask_white], means.values[mask_white], color='white', edgecolor='black', yerr=moe[mask_white])
plt.xticks(xax, df.columns)
plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Color-Coded Bar Graph (y=43000)')
plt.savefig('solution.png')
plt.show()