import streamlit as st
import pandas as pd
import numpy as np
import ift6758.client.game_client as game_client
import ift6758.client.serving_client as serving_client
from datetime import timedelta, time, date, datetime

st.title("Hockey Visualization App")

game_idx = dict()
servingClient = serving_client.ServingClient(features=['Secondes_jeu', 'Period_Number', 'X_Coordinate', 'Y_Coordinate',
'Distance', 'Angle', 'Shot_Type', 'Last_event_type', 'X_last_event',
'Y_last_event', 'Sec_from_lastEvent', 'Dis_from_lastEvent', 'Rebond',
'Angle_change', 'Vitesse'])
gameClient = game_client.GameClient(features=['Secondes_jeu', 'Period_Number', 'X_Coordinate', 'Y_Coordinate',
'Distance', 'Angle', 'Shot_Type', 'Last_event_type', 'X_last_event',
'Y_last_event', 'Sec_from_lastEvent', 'Dis_from_lastEvent', 'Rebond',
'Angle_change', 'Vitesse'])

with st.sidebar:
    workspace = st.text_input("Workspace", value="teylouniseifu")
    model = st.text_input("Model", value="model-xgb-2")
    version = st.text_input("Version", value="1.0.0")
    if st.button("Get model"):
        servingClient.download_registry_model(workspace,model,version)

with st.container():
    game_id = st.text_input("Game ID", value="2016020001")

with st.container():
    if st.button("Ping game") and game_id:
        df = gameClient.get_game_events(game_id)
        
        predictions = servingClient.predict(df)[1:-2].split(',')
        print(predictions)
        teamnames = gameClient.get_team_names()
        st.header("Game "+game_id+" : "+teamnames[0]+" vs "+teamnames[1])        
        
        # Get remaining period time
        df['Remaining_Time'] = df['Secondes_jeu'].apply(lambda x: 1200-int(x%1200))
        # Convert remaining time in time object
        df['Minutes'] = df['Remaining_Time'].apply(lambda x: int(x/60))
        df['Seconds'] = df['Remaining_Time'].apply(lambda x: int(x%60))
        df['Remaining_Time'] = [str(time(x['Minutes'], x['Seconds']))[:5] for _, x in df.iterrows()]
        df = df.drop(['Seconds', 'Minutes'], axis = 1)

        st.text("Period "+str(df['Period_Number'].iloc[-1])+" - "+str(df['Remaining_Time'].iloc[-1]+" left"))

        away, home = st.columns(2)
        
        away_score = 0
        home_score = 0

        for idx in range(len(predictions)):
            if df['Team_of_Shooter'].iloc[idx] == teamnames[0]:
                away_score += float(predictions[idx])
            elif df['Team_of_Shooter'].iloc[idx] == teamnames[1]:
                home_score += float(predictions[idx])

        away.metric(teamnames[0]+" xG (actual)", round(away_score,1), )
        home.metric(teamnames[1]+" xG (actual)", round(home_score,1), )

        st.header("Data Used for predict")
        st.dataframe(df)