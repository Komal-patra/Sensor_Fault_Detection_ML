from Sensor_fault_detection.entity.config_entity import DataValidationConfig
from Sensor_fault_detection.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Sensor_fault_detection.logger import logging
from Sensor_fault_detection.exception import SensorException
import os, sys
from typing import Optional
import numpy as np 
import pandas as pd 
from Sensor_fault_detection.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp


class DataValidation:

    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
        except Exception as e:
            raise SensorException(e, sys)
        
    
    def drop_missing_values_columns(self, df:pd.DataFrame, report_key_name:str)->Optional[pd.DataFrame]:

        try:
            threshold = self.data_validation_config.missing_threshold
            null_report = (df.isna().sum()*100)/df.shape[0]
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report> threshold].index
            logging.info(f"Columns to drop: {list(drop_column_names)}")
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(list(drop_column_names), axis=1,inplace=True)

            if len(df.columns)==0:
                return None
            return df

        except Exception as e:
            raise SensorException(e,sys)
        
    def is_required_columns_exists(self, df:pd.DataFrame, report_key_name:str)-> bool:

        try:
            schema_info = read_yaml_file(file_path=self.data_validation_config.schema_file_path)
            required_columns = schema_info['required_columns']
            logging.info(f"Required columns: {required_columns}")

            missing_required_column = []
            for column in required_columns:
                if column not in df.columns:
                    missing_required_column.append(column)
            
            if len(missing_required_column)==0:
                return True
            logging.info(f"Missing required columns are  {missing_required_column}")
            self.validation_error[report_key_name]= missing_required_column
            return False
    
        except Exception as e:
            raise SensorException(e,sys)
        
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key_name)-> None:

        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                        'pvalues':float(same_distribution.pvalue),
                        'same_distribution': True

                    }
                else:
                    drift_report[base_column]={
                        'pvalues':float(same_distribution.pvalue),
                        'same_distribution': False

                    }
                self.validation_error[report_key_name]=drift_report
    
        except Exception as e:
            raise SensorException(e,sys)

    def drop_columns(self, df:pd.DataFrame)-> pd.DataFrame:
        
        try:
            schema_info = read_yaml_file(file_path=self.data_validation_config.schema_file_path)
            drop_columns = schema_info['drop_columns']
            logging.info(f"Dropping column based on schema provided: {drop_columns}")
            df.drop(drop_columns, axis=1, inplace=True)
            return df

        except Exception as e:
            raise SensorException(e,sys)


    def initiate_data_validation(self)-> DataValidationArtifact:
        
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            train_df = self.drop_columns(df=train_df)
            test_df = self.drop_columns(df= test_df)

            train_df = self.drop_missing_values_columns(df=train_df, report_key_name="train_missing_values_columns")
            test_df = self.drop_missing_values_columns(df=test_df, report_key_name="test_missing_values_columns")

            if train_df is None:
                logging.info(f"No column left in train df hence stopping this pipeline")
                raise Exception("No column left in train df hence stopping this pipeline")
            
            
            if test_df is None:
                logging.info(f"No column left in test df hence stopping this pipeline")
                raise Exception("No column left in test df hence stopping this pipeline")

            is_exists = self.is_required_columns_exists(df=train_df, report_key_name="train_required_column")
            if not is_exists:
                raise Exception("Required columns are not available in train df")

            is_exists = self.is_required_columns_exists(df=test_df, report_key_name="train_required_column")
            if not is_exists:
                raise Exception("Required columns are not available in test df")

            if len(train_df.columns)!=len(test_df.columns):
                raise Exception(f"Train and test df does not have equal columns")
            
            self.data_drift(base_df=train_df, current_df=test_df, report_key_name="train_test_drift")

            write_yaml_file(file_path=self.data_validation_config.report_file_name, data=self.validation_error)
            
            os.makedirs(self.data_validation_config.valid_dir,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, header=True,index=False)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, header=True,index=False)

            data_validation_artifact = DataValidationArtifact(report_file_path=self.data_validation_config.report_file_name, 
                        train_file_path=self.data_validation_config.valid_train_file_path, 
                        test_file_path=self.data_validation_config.valid_test_file_path, 
                        status=True)
            return data_validation_artifact

        except Exception as e:
            raise SensorException(e,sys)