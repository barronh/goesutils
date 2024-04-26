"""
Find and Retrieve Files w/ GUI
==============================

Find ABI-L2-MCMIPC files from GOES-16.
"""

import pandas as pd
import xarray as xr
import goesutils

# %%
# Navigator has a Interactive Form
# --------------------------------
#
# * form defaults to ABI-L2-AOD a week ago at 0Z
# * change anything you want
# * product definitions: https://docs.opendata.aws/noaa-goes16/cics-readme.html

nav = goesutils.NOAAs3('noaa-goes16')
nav.form

# %%
# Navigator form interaction utilities
# ------------------------------------
#
# * findfiles_from_form adn getfiles_from_form
# * for more information, see documentation.

remotepaths = nav.findfiles_from_form()
print(len(remotepaths), 'files eg,', remotepaths[0])
# 12 files eg, ABI-L2-AODC/2024/110/00/OR_ABI-L2-AODC-M6_G16_s20241100001171_e20241100003544_c20241100006242.nc

# Use get to download them instead
# localpaths = s3.getfiles_from_form()
# or use getfiles
localpaths = nav.getfiles(remotepaths[:1])

# %%
# Plot with helper utilities
# --------------------------
#
# * findfiles_from_form adn getfiles_from_form
# * for more information, see documentation.

from goesutils.proj import getproj
import pycno

aodds = xr.open_dataset(localpaths[0])
proj = getproj(aodds)
cno = pycno.cno(proj=proj)
qm = aodds['AOD'].where(aodds['DQF'] >= 1).plot(vmin=0)
cno.drawstates(ax=qm.axes)
qm.figure.savefig('aod.png')
