def test_navaodfind():
    from .. import NOAAs3
    import pandas as pd

    nav = NOAAs3('noaa-goes16')
    dates = pd.date_range('2023-09-21 12', '2023-09-21 18', freq='H')
    remotekeys = nav.findfiles('ABI-L2-AODC', dates)
    assert (len(remotekeys) == 84)
    expath = (
        'ABI-L2-AODC/2023/264/12/OR_ABI-L2-AODC-M6_G16_'
        + 's20232641201172_e20232641203545_c20232641205547.nc'
    )
    assert (expath in remotekeys)


def test_navaodget():
    from .. import NOAAs3
    import pandas as pd
    import tempfile
    import os

    nav = NOAAs3('noaa-goes16')
    dates = pd.date_range('2023-09-21 12', '2023-09-21 12', freq='H')
    remotekeys = nav.findfiles('ABI-L2-AODC', dates)
    with tempfile.TemporaryDirectory() as td:
        locps = nav.getfiles(remotekeys=remotekeys[:1], workdir=td)
        assert os.path.exists(locps[0])


def test_form():
    from .. import NOAAs3

    nav = NOAAs3('noaa-goes16')
    try:
        nav.form
    except ImportError:
        import warnings
        warnings.warn('Needs newer python to test')
