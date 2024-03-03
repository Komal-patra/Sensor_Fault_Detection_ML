# Sensor_Fault_Detection_ML
The end- to- end machine learning project to detect the sensor fault

conda create -n sensor python=3.8

conda activate sensor

conda deactivate

pip install -r requirements.txt

pip install virtualenv


docker images

docker build -t sensor:latest .

docker run -p 8080:8080 -v \airflow\dags:/app/airflow/dags -e 'MONGO_DB_URL=mongodb+srv://mongodb:mongodb@clusterkomalmongodb.trikl.mongodb.net/?retryWrites=true&w=majority&appName=ClusterKomalMongoDB' sensor:latest

docker-compose up
