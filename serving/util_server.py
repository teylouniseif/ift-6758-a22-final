import os
from xgboost import XGBClassifier,Booster
from comet_ml import API
from tensorflow import keras
from keras.models import load_model


def download_model(workspace, model , version , model_log, logger):
    if os.path.exists(model) and os.listdir(model):
        #load model , le mot cle 'global' declare une seul fois!
        filename = os.listdir(model)[0]
        # global model_log
        if 'neural' in filename:
            logger.info(model+"/"+filename)
            model_log = load_model(model+"/"+filename)
            logger.info(model+"/"+filename)
        else:
            model_log = XGBClassifier()
            booster = Booster()
            booster.load_model(model+"/"+filename)
            model_log._Booster = booster
        # write to the log about the model change
        # app.logger.info('Le modèle est changé à '+model)
        msg = 'Le modèle est changé à: '+model
    else:
        try:
            api = API(api_key='57KbI0mTaIGplsSaYoAFXYMFL')
            # Download a Registry Model:
            api.download_registry_model(workspace, model, version, output_path="./"+model, expand=True)
        except:
            # write to the log about the failure
            msg = 'Échec du chargement du modèle: '+ model
        else:
            #load model
            filename = os.listdir(model)[0]
            if 'neural' in filename:
                model_log = keras.models.load_model(model+"/"+filename)
            else:
                model_log = XGBClassifier()
                booster = Booster()
                booster.load_model(model+"/"+filename)
                model_log._Booster = booster

            # write to the log about the model change
            msg = 'Le modèle est changé à: '+model

    logger.info('model+"/"+filename')
    return msg,model_log
