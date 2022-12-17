import os
from xgboost import XGBClassifier,Booster
from comet_ml import API

def download_model(workspace, model , version , model_log):
    if os.path.exists(model) and os.listdir(model):
        #load model , le mot cle 'global' declare une seul fois!
        filename = os.listdir(model)[0]
        # global model_log
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
            model_log = XGBClassifier()
            booster = Booster()
            booster.load_model(model+"/"+filename)
            model_log._Booster = booster
            # write to the log about the model change
            msg = 'Le modèle est changé à: '+model

    
    return msg,model_log

