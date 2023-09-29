__init__ = ['cmi2geocolor']


def cmi2geocolor(ds):
    """
    Convert CMI_01 (B), CMI_02 (R), and CMI_03 (G') to color. Steps
    as follows:

    1. Clip all values to 0 to 1
    2. Raise all values to the power of (1 / 2.2)
    3. Replace G' with G = 0.45 * R + 0.1 * G' + 0.45 * B
    4. Clip all values to 0 to 1

    Arguments
    ---------
    ds : xarray.Dataset
      Expected to be a ABI-L2-MCMIPC file opened with xarray. Must have
      variables B=CMI_C01, R=CMI_C02, and G'=CMI_C03

    Returns
    -------
    rgb : numpy.array
        Array shaped (y, x, RGB) with values appropriate for pyplot.imshow
    """
    import numpy as np

    rgb = np.array([ds.CMI_C02, ds.CMI_C03, ds.CMI_C01])
    rgb = np.power(np.clip(np.rollaxis(rgb, 0, 3), 0, 1), 1 / 2.2)
    # pseudo green
    rgb[..., 1] = np.clip(
        0.45 * rgb[..., 0] + 0.1 * rgb[..., 1] + 0.45 * rgb[..., 2],
        0, 1
    )

    return rgb
