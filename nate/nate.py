'''
Nathan Tarr's personal library of fuctions for daily workflow.
'''

def writeLog(content, log):
    '''
    (string, string) -> write to file
    
    Writes the text you provide to the log file you specify.
    
    Arguments:
    content -- string to write to file
    log -- the path of a log file
    '''
    print content
    with open(log, 'a') as logDoc:
        logDoc.write(content + '\n')
            

def AddArcMapSelections(raster, MUlist):
    '''
    (raster, list) -> selection

    For use in ArcMap python window.  Selects pixels for map unit codes specified
        in MUlist for viewing and review.

    Arguments:
    raster -- the raster layer you want to select from.
    MUlist -- a python list of codes to select from the "VALUE" field.
    '''
    import arcpy
    selectionType = "ADD_TO_SELECTION"
    sql = '"VALUE" = ' + str(MUlist[0])
    for m in MUlist[1:]:
        sql = sql + ' OR "VALUE" = ' + str(m)
    arcpy.SelectLayerByAttribute_management(raster, selectionType, sql)

def RemoveArcMapSelections(raster, MUlist):
    '''
    (raaster, list) -> selection

    For use in ArcMap python window.  Removes pixels for map unit codes specified
        in MUlist from selection for viewing and review.

    Arguments:
    raster -- the raster layer you want to select from.
    MUlist -- a python list of codes to select from the "VALUE" field.
    '''
    import arcpy
    selectionType = "REMOVE_FROM_SELECTION"
    sql = '"VALUE" = ' + str(MUlist[0])
    for m in MUlist[1:]:
        sql = sql + ' OR "VALUE" = ' + str(m)
    arcpy.SelectLayerByAttribute_management(raster, selectionType, sql)


def NewArcMapSelections(raster, MUlist):
    '''
    (raster, list) -> selection

    For use in ArcMap python window.  Creates a new selection of pixels for
        map unit codes specified in MUlist for viewing and review.  Previous
        selections are cleared first.

    Arguments:
    raster -- the raster layer you want to select from.
    MUlist -- a python list of codes to select from the "VALUE" field.
    '''
    import arcpy
    selectionType = "NEW_SELECTION"
    sql = '"VALUE" = ' + str(MUlist[0])
    for m in MUlist[1:]:
        sql = sql + ' OR "VALUE" = ' + str(m)
    arcpy.SelectLayerByAttribute_management(raster, selectionType, sql)


def MakeRemap(mapUnitCodes, reclassValue):
    '''
    (list, integer) -> list of lists

    Returns a RemapValue list for use with arcpy.sa.Reclassify()

    Arguments:
    mapUnitCodes -- A list of land cover map units that you with to reclassify.
    reclassValue -- The value that you want to reclassify the mapUnitCodes that you
        are passing to.

    Example:
    >>> MakeRemap([1201, 2543, 5678, 1234], 1)
    [[1201, 1], [2543, 1], [5678, 1], [1234, 1]]
    '''
    remap = []
    for x in mapUnitCodes:
        o = []
        o.append(x)
        o.append(reclassValue)
        remap.append(o)
    return remap

# Formula for longitude length
def nominal_precisions(longitude, latitude, produce):
    '''
    Calculates the nominal precisions based on an WGS84 coordinates.
    Method is based on information from wikipedia page on latitude and posts
    at https://gis.stackexchange.com/questions/8650/measuring-accuracy-of-latitude-and-longitude
    https://wiki.openstreetmap.org/wiki/Precision_of_coordinates

    PARAMETERS
    ----------
    latitude : decimal degrees (EPSG:4326) latitude as string.
    longitude : decimal degrees (EPSG:4326) longitude as string.
    produce : 'longitude', 'latitude', or 'both'

    RETURNS
    -------
    x : uncertainty in longitude (meters) as float.
    y : uncertianty in latitude (meters) as float.

    EXAMPLE
    -------
    x, y = nominal_precisions("-93.455", "26.3455", produce="both")
    '''
    lat = latitude.split(".")
    long = longitude.split(".")

    # Longitude
    digitsX = {2: 100, 3: 1000, 4: 10000, 5: 100000}
    x =(111321 * np.cos(float(latitude) * np.pi/180))/digitsX[len(long[1])] # decimal gets moved based on digits.

    # Latitude
    digitsY = {2: 1111.2, 3: 111.1, 4: 11.1, 5: 1.1} # Lookup for latitude precision
    y = digitsY[len(lat[1])]

    if produce == "both":
        return x, y
    if produce == "longitude":
        return x
    if produce == "latitude":
        return y