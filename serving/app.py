"""
If you are in the same directory as this file (app.py), you can run run the app using gunicorn:

    $ gunicorn --bind 0.0.0.0:<PORT> app:app

gunicorn can be installed via:

    $ pip install gunicorn

"""
import os
from pathlib import Path
import logging
from flask import Flask, jsonify, request, abort
import sklearn
import pandas as pd
import joblib
import os
import json
from util_server import*
# import ift6758


app = Flask(__name__)

model_log = None

@app.route('/')
def hello():
    return 'milestone3 server'

LOG_FILE = os.environ.get("FLASK_LOG", "flask.log")



@app.before_first_request
def before_first_request():
    """
    Hook to handle any initialization before the first request (e.g. load model,
    setup logging handler, etc.)
    """
    # TODO: setup basic logging configuration
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

    #pour eviter trop de infomartion sur le fichier log,effacez le fichier log après chaque déconnexion du serveur
    log_file = 'flask.log'
    if os.path.exists(log_file):
        with open(log_file, 'w') as f:
            f.truncate(0)


    #chager le modele par default
    global model_log
    msg, model_log =download_model('teylouniseifu', 'xgboost-model-milestone3' , '1.0.0' , model_log)
    app.logger.info('chager le modele par default: '+'xgboost-model-milestone3')


    pass


@app.route("/logs", methods=["GET"])
def logs():
    """Reads data from the log file and returns them as the response"""

    # TODO: read the log file specified and return the data
    with open('flask.log', 'r') as f:
        log = f.read()


    log_records = log.split('\n')
    json_log_app = []
    for record in log_records:
        if record:
            if ":app:" in record:
                json_log_app.append(record)

    return jsonify(json_log_app)  # response must be json serializable!


@app.route("/download_registry_model", methods=["POST"])
def download_registry_model():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/download_registry_model

    The comet API key should be retrieved from the ${COMET_API_KEY} environment variable.

    Recommend (but not required) json with the schema:

        {
            workspace: (required),
            model: (required),
            version: (required),
            ... (other fields if needed) ...
        }

    """
    # Get POST json data
    js = request.get_json(force = True)
    workspace = js['workspace']
    model = js['model']
    version = js['version']

    # TODO: check to see if the model you are querying for is already downloaded
    # TODO: if yes, load that model and write to the log about the model change.
    # eg: app.logger.info(<LOG STRING>)
    # TODO: if no, try downloading the model: if it succeeds, load that model and write to the log
    # about the model change. If it fails, write to the log about the failure and keep the
    # currently loaded model
    global model_log
    msg, model_log =download_model(workspace, model , version , model_log)
    if "Échec" in msg:
        app.logger.error(msg)
    else:
        app.logger.info(msg)

    return None


@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles POST requests made to http://IP_ADDRESS:PORT/predict

    Returns predictions
    """
    # Get POST json data
    js = request.get_json()
    json_str = json.dumps(js)

    df_test = pd.read_json(json_str) #.drop(columns=["Team_of_Shooter"])
    df_test["Rebond"]=df_test["Rebond"].astype("category")
    df_test["Last_event_type"]=df_test["Last_event_type"].astype("category")
    df_test["Shot_Type"]=df_test["Shot_Type"].astype("category")


    preds = model_log.predict_proba(df_test)
    preds = preds[:, 1]
    print(preds)



    response = preds.tolist()


    app.logger.info("Les résultats des prédiction du modèle"+ str(response))

    return jsonify(response)  # response must be json serializable!
