import pandas as pd
import pandas_datareader.data as web

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib inline

import seaborn as sns
sns.set_style('white', {"xtick.major.size": 2, "ytick.major.size": 2})
flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71","#f4cae4"]
sns.set_palette(sns.color_palette(flatui,7))

import missingno as msno
p=print

f1 = 'USREC' # recession data from FRED

start = pd.to_datetime('1999-01-01')
end = pd.datetime.today()

mkt = '^GSPC'
MKT = (web.DataReader([mkt,'^VIX'], 'yahoo', start, end)['Adj Close']
      .resample('MS') # month start b/c FED data is month start
       .mean()
       .rename(columns={mkt:'SPX','^VIX':'VIX'})
       .assign(SPX_returns=lambda x: np.log(x['SPX']/x['SPX'].shift(1)))
       .assign(VIX_returns=lambda x: np.log(x['VIX']/x['VIX'].shift(1)))
       )

data = (web.DataReader([f1], 'fred', start, end)
        .join(MKT, how='outer')
        .dropna())

p(data.head())
p(data.info())
msno.matrix(data)

# recessions are marked as 1 in the data
recs = data.query('USREC==1')


# now we can grab the indices for the start
# and end of each recession
recs2k_bgn = recs_2k.index[0]
recs2k_end = recs_2k.index[-1]

recs2k8_bgn = recs_2k8.index[0]
recs2k8_end = recs_2k8.index[-1]

plot_cols = ['SPX', 'SPX_returns']

# 2 axes for 2 subplots
fig, axes = plt.subplots(2,1, figsize=(14,9), sharex=True)
data[plot_cols].plot(subplots=True, ax=axes)
for ax in axes:
    ax.axvspan(recs2k_bgn, recs2k_end, color=sns.xkcd_rgb['grey'], alpha=0.5)
    ax.axvspan(recs2k8_bgn, recs2k8_end,  color=sns.xkcd_rgb['grey'], alpha=0.5)

plt.savefig('T:\\Universität Bern\\Lehrveranstaltungen MA\\Empirical Corporate Finance\\2020\\02_Slides\\Session 5 & 6\\SPX.png')
