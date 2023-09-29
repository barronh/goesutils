"""
Plot Truecolor Approximation
============================

Download one ABI-L2-MCMIPC file from GOES-16 and plot a true color image.
"""

import matplotlib.pyplot as plt
import goesutils
from goesutils.style import cmi2geocolor
from goesutils.proj import getproj
import pandas as pd
import xarray as xr
import pycno

nav = goesutils.NOAAs3('noaa-goes16')
dates = pd.date_range('2023-09-21 20', '2023-09-21 20', freq='H')
remotekeys = nav.findfiles(short_name='ABI-L2-MCMIPC', dates=dates)
localpaths = nav.getfiles(remotekeys[:1])

ds = xr.open_dataset(localpaths[0])
rgb = cmi2geocolor(ds)

proj = getproj(ds)
cno = pycno.cno(proj=proj)

hdx = (ds.x[-1] - ds.x[0]) / (ds.x.size - 1) / 2
hdy = (ds.y[-1] - ds.y[0]) / (ds.y.size - 1) / 2
extent = [ds.x[0] - hdx, ds.x[-1] + hdx, ds.y[-1] + hdy, ds.y[0] - hdy]

fig, ax = plt.subplots()
p = ax.imshow(rgb[::-1], extent=extent)
ax.set(xticks=[], yticks=[])
cno.drawstates(ax=ax, color='white')

# Show the figure
plt.show()
# Or save the figure
# fig.savefig('color.png')
