# Disaster_Response_Pipeline





## Files
        disaster_response_pipeline
          |-- app
                |-- templates
                        |-- go.html
                        |-- master.html
                |-- run.py
          |-- data
                |-- ETL Pipeline Preparation.ipynb
                |-- disaster_message.csv
                |-- disaster_categories.csv
                |-- InsertDadabaseName.db
                |-- process_data.py
          |-- models
                |-- train_classifier.py

          |-- README
          |-- License


## Descriptions
1. App folder including the templates folder and "run.py" for the web application
2. Data folder containing "InsertDadabaseName.db", "disaster_categories.csv", "disaster_messages.csv" and "process_data.py" for data cleaning and transfering.
3. Models folder including "classifier.pkl" and "train_classifier.py" for the Machine Learning model.
4. README file
5. License file

## Instructions
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/InsertDadabaseName.db`
        
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/InsertDadabaseName.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
