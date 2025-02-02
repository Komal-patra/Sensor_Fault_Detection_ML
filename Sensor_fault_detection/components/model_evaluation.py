from Sensor_fault_detection.entity.config_entity import ModelEvaluationConfig
from Sensor_fault_detection.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact, ModelTrainerArtifact,ModelEvaluationArtifact
from Sensor_fault_detection.logger import logging
from Sensor_fault_detection.exception import SensorException
import os,sys 
from sklearn.metrics import f1_score
from Sensor_fault_detection.utils import read_yaml_file,load_object
from Sensor_fault_detection.ml.model_resolver import ModelResolver
import pandas as pd


class ModelEvaluation:
    
    def __init__(self,
        model_eval_config:ModelEvaluationConfig,
        data_validation_artifact: DataValidationArtifact,
        data_transformation_artifact:DataTransformationArtifact,
        model_trainer_artifact:ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20}  Model Evaluation {'<<'*20}")
            self.model_eval_config=model_eval_config
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_artifact=model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise SensorException(e, sys)   

    def initiate_model_evaluation(self)->ModelEvaluationArtifact:
        try:
            
            logging.info("if saved model folder has model the we will compare "
            "which model is best trained or the model from saved model folder")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact

            #Finding location of transformer, model and target encoder
            logging.info("Finding location of transformer model and target encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            
            logging.info("Previous trained objects of transformer, model and target encoder")
            #Previous trained  objects
            transformer = load_object(file_path=transformer_path)
            model = load_object(file_path=model_path)
            target_encoder = load_object(file_path=target_encoder_path)

            
            logging.info("Currently trained model objects")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            current_model  = load_object(file_path=self.model_trainer_artifact.model_path)
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)
            
            test_df = pd.read_csv(self.data_validation_artifact.test_file_path)
            schema_info = read_yaml_file(file_path=self.model_eval_config.schema_file_path)
            target_column = schema_info['target_column']

            target_df=test_df[target_column]
            y_true =target_encoder.transform(target_df)

            input_feature_name = list(transformer.feature_names_in_)
            input_arr =transformer.transform(test_df[input_feature_name])
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")

             # accuracy using current trained model
            input_feature_name = list(current_transformer.feature_names_in_)
            input_arr =current_transformer.transform(test_df[input_feature_name])
            y_pred = current_model.predict(input_arr)
            y_true =current_target_encoder.transform(target_df)
            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            print(f"Prediction using trained model: {current_target_encoder.inverse_transform(y_pred[:5])}")

            diff = current_model_score-previous_model_score
            if diff<self.model_eval_config.change_threshold:
                logging.info("Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=diff)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact
        except Exception as e:
            raise SensorException(e, sys)   


