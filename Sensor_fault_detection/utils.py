from .config import mongo_client
import pandas as pd
import logging
import json

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
        raise e

