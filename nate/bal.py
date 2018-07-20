# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 15:13:38 2018 by nmtarr

Description: Functions with general use related to the USGS Biogeography
Analysis Laboratory
"""
def _connect_mongodb(host, port, username, password, db):
    import pymongo
    """ A util for making a connection to mongo """

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)
        
    return conn[db]


def read_collection_as_dataframe(db, collection, host, port, username, password, no_id=False, query={}):
    """ Read from Mongo and Store into DataFrame """
    import pandas
    # Connect to MongoDB
    db = _connect_mongodb(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pandas.DataFrame(list(cursor))
    
    # Delete the _id
    if no_id:
        del df['_id']
    
    return df


def get_collection_cursor(db, collection, host, port, username, password, query={}):
    """ Read from Mongo """

    # Connect to MongoDB
    db = _connect_mongodb(host=host, port=port, username=username, password=password, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)
    
    return cursor