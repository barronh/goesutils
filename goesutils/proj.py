def getproj(geods, updatexy=True):
    """
    Arguments
    ---------
    geods : xarray.Dataset
        Dataset with geospatial variables x, y, and goes_imager_projection
    updatexy : bool
        If True, update x and y from radians to meters to be consistent with
        projection. If False, return sat_h so updates could be made.

    Returns
    -------
    proj or proj, sat_h
        If updatexy is False, proj and satellite perspective height (sat_h)
        will be returned. Otherwise, only proj
    """
    import pyproj

    sat_h = geods['goes_imager_projection'].attrs['perspective_point_height']
    crs = pyproj.CRS.from_cf(geods['goes_imager_projection'].attrs)
    if updatexy:
        proj = pyproj.Proj(crs, to_meters=sat_h, preserve_units=True)
        geods.coords['x'] = geods.x * sat_h
        geods.coords['y'] = geods.y * sat_h
        return proj
    else:
        proj = pyproj.Proj(crs, preserve_units=True)
        return proj
