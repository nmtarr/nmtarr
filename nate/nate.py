'''
Nathan Tarr's personal library of fuctions for daily workflow.

'''
import arcpy

def AddArcMapSelections(raster, MUlist):
    '''
    (raster, list) -> selection

    For use in ArcMap python window.  Selects pixels for map unit codes specified
        in MUlist for viewing and review.

    Arguments:
    raster -- the raster layer you want to select from.
    MUlist -- a python list of codes to select from the "VALUE" field.
    '''
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
