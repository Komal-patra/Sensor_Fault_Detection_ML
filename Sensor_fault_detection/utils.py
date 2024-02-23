from .config import mongo_client
import pandas as pd
import logging
import json
from .exception import SensorException
import sys

def dump_csv_file_to_mongodb_collection(file_path:str, database_name:str, collection_name:str)->None:
    try:
        # reading the csv file 
        df = pd.read_csv(file_path)
        #logging the shape of data
        logging.info(f'Rows and columns {df.shape}')
        # dropping the index column
        df.reset_index(drop=True, inplace=True)
        #converting the pandas df into json
        json_records = list(json.loads(df.T.to_json()).values())
        # creating the database, collection and json records
        mongo_client[database_name][collection_name].insert_many(json_records)

    except Exception as e:
        raise SensorException(e,sys)

def export_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    try:
        # fetching the document from mongodb into pandas dataframe
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        # as we dont need the default id column from the document
        if '_id' in df.columns.to_list():
            df = df.drop('_id', axis=1)
        return df
    except Exception as e:
        raise SensorException(e,sys)
