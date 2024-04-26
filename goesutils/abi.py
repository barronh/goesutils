import pandas as pd
# Define dictionary keys
keys = ['fulldisc', 'conus', 'meso_1', 'meso_2']

# Define dictionary values for each ABI L2 product 
abiprod = {
  'Aerosol Detection': ['ADPF', 'ADPC', 'ADPM', 'ADPM'],
  'Aerosol Optical Depth': ['AODF', 'AODC', pd.NA, pd.NA],
  'Clear Sky Mask': ['ACMF', 'ACMC', 'ACMM', 'ACMM'],
  'Cloud and Moisture Imagery': ['CMIPF', 'CMIPC', 'CMIPM', 'CMIPM'],
  'Cloud and Moisture Imagery Multiband': [
      'MCMIPF', 'MCMIPC', 'MCMIPM', 'MCMIPM'
  ],
  'Cloud Optical Depth': ['CODF', 'CODC', pd.NA, pd.NA],
  'Cloud Particle Size': ['CPSF', 'CPSC', 'CPSM', 'CPSM'],
  'Cloud Top Height': ['ACHAF', 'ACHAC', 'ACHAM', 'ACHAM'],
  'Cloud Top Phase': ['ACTPF', 'ACTPC', 'ACTPM', 'ACTPM'],
  'Cloud Top Pressure': ['CTPF', 'CTPC', pd.NA, pd.NA],
  'Cloud Top Temperature': ['ACHTF', 'None', 'ACHTM', 'ACHTM'],
  'Derived Motion Winds': ['DMWF', 'DMWC', 'DMWM', 'DMWM'],
  'Derived Stability Indices': ['DSIF', 'DSIC', 'DSIM', 'DSIM'],
  'Downward Shortwave Radiation': ['DSRF', 'DSRC', 'DSRM', 'DSRM'],
  'Fire Hotspot Characterization': ['FDCF', 'FDCC', 'FDCM', 'FDCM'],
  'Land Surface Temperature': ['LSTF', 'LSTC', 'LSTM', 'LSTM'],
  'Legacy Vertical Moisture Profile': ['LVMPF', 'LVMPC', 'LVMPM', 'LVMPM'],
  'Legacy Vertical Temperature Profile': ['LVTPF', 'LVTPC', 'LVTPM', 'LVTPM'],
  'Rainfall Rate/QPE': ['RRQPEF', pd.NA, pd.NA, pd.NA],
  'Reflected Shortwave Radiation': ['RSRF', 'RSRC', pd.NA, pd.NA],
  'Sea Surface Temperature': ['SSTF', pd.NA, pd.NA, pd.NA],
  'Total Precipitable Water': ['TPWF', 'TPWC', 'TPWM', 'TPWM'],
  'Volcanic Ash': ['VAAF', pd.NA, pd.NA, pd.NA],
}

abiproddf = 'ABI-L2-' + pd.DataFrame(abiprod, index=keys).T
abiproddf.index.name = 'Description'
