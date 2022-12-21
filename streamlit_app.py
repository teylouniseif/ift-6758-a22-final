import streamlit as st
import pandas as pd
import numpy as np
import milestone1_2.question1 as question1
import milestone1_2.question4 as question4
import os
import json

"""question1.get_play_by_play_season_gameType(year, game_id[4:6],"data_saved/play_by_play")"""

st.title("Hockey Visualization App")

with st.sidebar:
    st.text_input("Workspace")
    st.text_input("Model")
    st.text_input("Version")

with st.container():
    game_id = st.text_input("Game ID", value="2016020001")

with st.container():
    if st.button("Ping game") and game_id:
        match_type = game_id[4:6]
        if match_type == "02":
            match_type = "regular"
        elif match_type == "03":
            match_type = "playoff"
        else:
            match_type = "None"
        
        year = game_id[:4]
        path = "\\data_saved\\play_by_play\\"+year+"\\"+match_type

        with open(os.path.abspath(os.getcwd()) + path +"\\"+game_id+".json", 'r') as f:
            data = json.loads(f.read())
        teamAway = data["gameData"]["teams"]["away"]["teamName"]
        teamHome = data["gameData"]["teams"]["home"]["teamName"]
        
        st.header("Game "+game_id+": "+teamAway+" vs "+teamHome)
       

with st.container():
    st.header("Data Used for predict")

    df_raw = question4.create_full_df(directory=os.path.abspath(os.getcwd()) + path)
    df = df_raw.loc[df_raw.Game_ID==int(game_id)]  
    st.dataframe(df)
    pass