def getproj(geods):
    import pyproj

    sat_h = geods['goes_imager_projection'].attrs['perspective_point_height']
    crs = pyproj.CRS.from_cf(geods['goes_imager_projection'].attrs)
    proj = pyproj.Proj(crs, to_meters=sat_h, preserve_units=True)
    return proj
