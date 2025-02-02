# Sensor_Fault_Detection_ML
The end- to- end machine learning project to detect the sensor fault Detection

## Problem Statement
The Air Pressure System (APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing the vehicle down. The benefits of using an APS instead of a hydraulic system are the easy availability and long-term sustainability of natural air.

This is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class
indicates that the failure was caused by something else.

### Solution Proposed 
In this project, the system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.
## Tech Stack Used
1. Python 
2. FastAPI 
3. Machine learning algorithms
4. Docker
5. MongoDB

## Infrastructure Required.

1. AWS S3
2. AWS EC2
3. AWS ECR
4. Git Actions
5. Terraform

## How to run?
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need AWS account to access the service like S3, ECR and EC2 instances.

## Data Collections
![image](https://user-images.githubusercontent.com/57321948/193536736-5ccff349-d1fb-486e-b920-02ad7974d089.png)


## Project Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536768-ae704adc-32d9-4c6c-b234-79c152f756c5.png)


## Deployment Archietecture
![image](https://user-images.githubusercontent.com/57321948/193536973-4530fe7d-5509-4609-bfd2-cd702fc82423.png)


### Step 1: Clone the repository
```bash
git clone https://github.com/Komal-patra/Sensor_Fault_Detection_ML.git
```

### Step 2- Create a conda environment after opening the repository

```bash
conda create -n sensor python=3.8
```

```bash
conda activate sensor
```

### Step 3 - Install the requirements
```bash
pip install -r requirements.txt
```

### step 4: Docker image Creation

```bash
    docker images
```

```bash
    docker build -t sensor:latest .
```

```bash
    docker run -p 8080:8080 -v \airflow\dags:/app/airflow/dags -e 'MONGO_DB_URL=mongodb+srv://mongodb:mongodb@clusterkomalmongodb.trikl.mongodb.net/?retryWrites=true&w=majority&appName=ClusterKomalMongoDB' sensor:latest
```

```bash
    docker-compose up
```



### Airflow 

![image](https://github.com/Komal-patra/Sensor_Fault_Detection_ML/blob/1f9fb475c5a7719fb26ad5610ac73255022c0532/images/Airflow_batch_prediction.png)

![image](https://github.com/Komal-patra/Sensor_Fault_Detection_ML/blob/1f9fb475c5a7719fb26ad5610ac73255022c0532/images/Airflow_training_pipeline.png)
