"""
Find and Retrieve Files
=======================

Find ABI-L2-MCMIPC files from GOES-16.
"""

import pandas as pd
import goesutils

nav = goesutils.NOAAs3('noaa-goes16')

# Define a date range of interest
dates = pd.date_range('2023-09-21 20', '2023-09-21 23', freq='h')

datakey = 'ABI-L2-MCMIPC'
keys = nav.findfiles(short_name=datakey, dates=dates)
print(len(keys), keys[0], '...')
# 48 ABI-L2-MCMIPC/2023/264/20/OR_ABI-L2-MCMIPC-M6_G16_s20232642001172_e20232642003545_c20232642004068.nc ...

# Query and Download
# paths = nav.getfiles(short_name=datakey, dates=dates)
# Or download one or more from previous query
paths = nav.getfiles(keys[:2])
# reports as each is downloaded
# ABI-L2-MCMIPC/2023/264/20/OR_ABI-L2-MCMIPC-M6_G16_s20232642001172_e20232642003545_c20232642004068.nc
# ABI-L2-MCMIPC/2023/264/20/OR_ABI-L2-MCMIPC-M6_G16_s20232642006172_e20232642008557_c20232642009058.nc

print(len(paths), paths[0])
# 2 ./s3.noaa-goes16/ABI-L2-MCMIPC/2023/264/20/OR_ABI-L2-MCMIPC-M6_G16_s20232642001172_e20232642003545_c20232642004068.nc