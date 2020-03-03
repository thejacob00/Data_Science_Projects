import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Convert the text 'stopwatch time' (MM:SS.s) to raw seconds
def stopwatch_time_to_seconds(stopwatch_time):
    nums = stopwatch_time.split(':')
    return nums.apply(lambda x : float(x[0])*60 + float(x[1]))

# Convert a raw number of seconds to a race time
def seconds_to_time_label(secs):
    converted_secs = []
    for entry in secs:
        converted_secs.append(seconds_to_time(entry))
    return converted_secs

def seconds_to_time(secs):
    minutes = math.floor(secs / 60)
    seconds = secs - (60 * minutes)
    if seconds > 9:
        seconds_str = str(int(seconds))
    elif seconds > 0:
        seconds_str = '0' + str(int(seconds))
    else:
        seconds_str = '00'
    time_str = str(int(minutes)) + ':' + seconds_str
    return time_str

# Data Cleaning
cols_2016 = ['Place', 'Grade', 'Name', 'Junk', 'Time', 'School']
df_2016 = pd.read_table('2016.txt', header=None, names=cols_2016)
df_2016['Place'] = df_2016['Place'].astype(int)
df_2016 = df_2016.set_index('Place')
df_2016 = df_2016[['Grade', 'Name', 'Time', 'School']]
df_2016['Time'] = stopwatch_time_to_seconds(df_2016['Time'].str)

df_2017 = pd.read_table('2017.txt', header=None, names=cols_2016)
df_2017['Place'] = df_2017['Place'].astype(int)
df_2017 = df_2017.set_index('Place')
df_2017 = df_2017[['Grade', 'Name', 'Time', 'School']]
df_2017['Time'] = stopwatch_time_to_seconds(df_2017['Time'].str)

cols_2018 = ['Place', 'Grade', 'Name', 'Time']
df_2018 = pd.read_table('2018.txt', header=None, names=cols_2018)
df_2018 = df_2018[df_2018.index % 2 == 0]
df_2018['Place'] = df_2018['Place'].str.replace('.', '')
df_2018['Place'] = df_2018['Place'].astype(str).astype(int)
df_2018 = df_2018.set_index('Place')
df_2018['Time'] = stopwatch_time_to_seconds(df_2018['Time'].str)

df_2019 = pd.read_table('2019.txt', header=None, names=cols_2018)
df_2019 = df_2019[df_2019.index % 2 == 0]
df_2019['Place'] = df_2019['Place'].str.replace('.', '')
df_2019['Place'] = df_2019['Place'].astype(str).astype(int)
df_2019 = df_2019.set_index('Place')
df_2019['Time'] = stopwatch_time_to_seconds(df_2019['Time'].str)

# From the four file dataframes, create a merged dataframe with
# times from all four years, arranged by place.
df_cols = [df_2016['Time'], df_2017['Time'], df_2018['Time'], df_2019['Time']]
df = pd.merge(df_2016['Time'], df_2017['Time'], how='outer', left_index=True, right_index=True)
df = df.rename(columns={df.columns[0]: '2016', df.columns[1]: '2017'})
df = pd.merge(df, df_2018['Time'], how='outer', left_index=True, right_index=True)
df = pd.merge(df, df_2019['Time'], how='outer', left_index=True, right_index=True)
df = df.rename(columns={df.columns[2]: '2018', df.columns[3]: '2019'})

# Statistical Analysis
means = df.mean()
winners = df.min()
top25s = df.iloc[24]

# Plotting
plt.figure()
plt.plot(df.columns.values, winners, '-bo')
plt.plot(df.columns.values, top25s, '-go')
plt.plot(df.columns.values, means, '-ro')

ax = plt.gca()
ax.set_xlabel('Year')
ax.set_ylabel('Race Time')
ax.set_title('MHSAA Cross-Country State Championship Times')
ax.set_ylim(1200, 840)
y_axis_values = np.linspace(1200, 840, num=7, endpoint=True)
plt.yticks(y_axis_values, seconds_to_time_label(y_axis_values))
plt.legend(['Winning time', 'Top 25 time', 'Average time'], loc=4)

# Include the actual race-winning times for each year on the visual
for a, b in zip(df.columns.values, winners):
    plt.annotate(xy=[a, b], s=seconds_to_time(int(b)), ha='center', textcoords='offset points', xytext=(0, 10))

plt.savefig('visualization.png')
plt.show()