__init__ = ['geocolor']


def cmi2geocolor(ds):
    """
    Arguments
    ---------
    ds : xarray.Dataset
      Expected to be a ABI-L2-MCMIPC file opened with xarray
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
