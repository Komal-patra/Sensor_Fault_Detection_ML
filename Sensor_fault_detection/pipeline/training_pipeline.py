from Sensor_fault_detection.entity.config_entity import (TrainingPipelineConfig, 
                                                         DataIngestionConfig, 
                                                         DataValidationConfig, 
                                                         DataTransformationConfig,
                                                         ModelTrainerConfig,
                                                         ModelEvaluationConfig)

from Sensor_fault_detection.entity.artifact_entity import (DataIngestionArtifact, 
                                                           DataValidationArtifact, 
                                                           DataTransformationArtifact,
                                                           ModelTrainerArtifact,
                                                           ModelEvaluationArtifact)

from Sensor_fault_detection.exception import SensorException

from Sensor_fault_detection.logger import logging

import os, sys

from Sensor_fault_detection.components.data_ingestion import DataIngestion
from Sensor_fault_detection.components.data_validation import DataValidation
from Sensor_fault_detection.components.data_transformation import DataTransformation
from Sensor_fault_detection.components.model_trainer import ModelTrainer
from Sensor_fault_detection.components.model_evaluation import ModelEvaluation


class TrainingPipeline:


    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.training_pipeline_config=training_pipeline_config

        except Exception as e:
            raise SensorException(e, sys)


    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config =DataIngestionConfig(
                training_pipeline_config=self.training_pipeline_config)
            
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        
        except Exception as e:
            raise SensorException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact)-> DataValidationArtifact:
        
        try:
            data_validation_config = DataValidationConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            data_validation = DataValidation(data_validation_config=data_validation_config,
                                             data_ingestion_artifact=data_ingestion_artifact)
            
            return data_validation.initiate_data_validation()
        
        except Exception as e:
            SensorException(e,sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact)-> DataTransformationArtifact:
        
        try:
            data_transformation_config = DataTransformationConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            data_transformation = DataTransformation(data_transformation_config= data_transformation_config,
                                             data_validation_artifact=data_validation_artifact)
            
            return data_transformation.initiate_data_transformation()
        
        except Exception as e:
            SensorException(e,sys)

    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact)-> ModelTrainerArtifact:
        
        try:
            model_trainer_config = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )
            model_trainer = ModelTrainer(model_trainer_config= model_trainer_config,
                                             data_transformation_artifact=data_transformation_artifact)
            
            return model_trainer.initiate_model_trainer()
        
        except Exception as e:
            SensorException(e,sys)

    def start_model_evaluation(self,   data_validation_artifact: DataValidationArtifact,
        data_transformation_artifact:DataTransformationArtifact,
        model_trainer_artifact:ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_eval_config = ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
            model_eval = ModelEvaluation(model_eval_config=model_eval_config,
             data_validation_artifact=data_validation_artifact,
             data_transformation_artifact=data_transformation_artifact,
             model_trainer_artifact=model_trainer_artifact)
            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise SensorException(e, sys)

        
    def start(self,):
        
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact
            )
            data_tranformation_artifact = self.start_data_transformation(
                data_validation_artifact=data_validation_artifact
            )
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_tranformation_artifact
            )
            model_eval_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
                            data_transformation_artifact=data_tranformation_artifact,
                            model_trainer_artifact=model_trainer_artifact)
            
        except Exception as e:
            raise SensorException(e, sys)