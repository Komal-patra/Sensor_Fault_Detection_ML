from .config import mongo_client
import pandas as pd
import logging
import json
from .exception import SensorException
import sys
import yaml
import os
import dill
import numpy as np

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


def read_yaml_file(file_path):
    try:
        with open(file_path,'rb') as file_reader:
            return yaml.safe_load(file_reader)
    except Exception as e:
        raise SensorException(e,sys)
    

def write_yaml_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok= True)
        with open(file_path,'w') as file_writer:
            yaml.dump(data, file_writer)
    except Exception as e:
        raise SensorException(e,sys)


def convert_columns_float(df:pd.DataFrame, exclude_columns:list=[])->pd.DataFrame:
    
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column] = df[column].astype('float')
        return df
    
    except Exception as e:
        SensorException(e,sys)


def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise SensorException(e,sys) 
    

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SensorException(e, sys) from e

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e, sys) from e