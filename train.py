from Sensor_fault_detection.pipeline.training_pipeline import TrainingPipeline
from Sensor_fault_detection.entity.config_entity import TrainingPipelineConfig
from Sensor_fault_detection.logger import logging


if __name__=="__main__":
    try:
        training_pipeline_config=  TrainingPipelineConfig()
        training_pipeline = TrainingPipeline(training_pipeline_config=training_pipeline_config)
        training_pipeline.start()
    except Exception as e:
        logging.info(e)
        print(e)