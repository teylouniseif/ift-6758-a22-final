import streamlit as st
import pandas as pd
import numpy as np
import ift6758.client.game_client as game_client
import ift6758.client.serving_client as serving_client

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
        df = game_client.get_game_events(game_id)
        teamnames = game_client.get_team_names()
        st.header("Game :"+game_id+":"+teamnames[0]+"vs"+teamnames[1])
       

with st.container():
    st.header("Data Used for predict")
    pass