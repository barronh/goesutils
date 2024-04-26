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

# %%
# Prepare a base api object
# -------------------------

nav = goesutils.NOAAs3('noaa-goes16')
# Usually, you would process multiple hours, but here just one
dates = pd.date_range('2023-09-21 20', '2023-09-21 20', freq='h')
remotekeys = nav.findfiles(short_name='ABI-L2-MCMIPC', dates=dates)
# Download only the first file
localpaths = nav.getfiles(remotekeys[:1])

# %%
# Open file and covert to RGB
# ---------------------------

ds = xr.open_dataset(localpaths[0])
# Convert to RGB
rgb = cmi2geocolor(ds)

# %%
# Define geography objects
# ------------------------

proj = getproj(ds)
cno = pycno.cno(proj=proj)

# calculate the corners of the whole dataset
# use pixel width to extend centroids to corners
hdx = (ds.x[-1] - ds.x[0]) / (ds.x.size - 1) / 2
hdy = (ds.y[-1] - ds.y[0]) / (ds.y.size - 1) / 2
extent = [ds.x[0] - hdx, ds.x[-1] + hdx, ds.y[-1] + hdy, ds.y[0] - hdy]

# %%
# Make a plot with state overlay
# -------------------------

# Make a plot using standard matplotlib functions
fig, ax = plt.subplots()
p = ax.imshow(rgb[::-1], extent=extent)
ax.set(xticks=[], yticks=[])
# Defining the extent allows you to plot other geographic information on top
cno.drawstates(ax=ax, color='white')

# Show the figure
plt.show()
# Or save the figure
# fig.savefig('color.png')
