from serving_client import ServingClient
from game_client import GameClient
"""import pandas as pd


x =  ServingClient(port=5001, features=['Secondes_jeu', 'Period_Number', 'X_Coordinate', 'Y_Coordinate',
       'Distance', 'Angle', 'Shot_Type', 'Last_event_type', 'X_last_event',
       'Y_last_event', 'Sec_from_lastEvent', 'Dis_from_lastEvent', 'Rebond',
       'Angle_change', 'Vitesse'])
#print(x.download_registry_model(
#workspace="teylouniseifu",
#model="boosted-tree-all-features-for-q5",
#version="1.0.0"
#))

js = {
"Secondes_jeu":{"185963":234.6,"286835":1698.6,"300289":432.6,"9512":2397.0,"188403":1311.6},
"Period_Number":{"185963":1,"286835":2,"300289":1,"9512":2,"188403":2},
"X_Coordinate":{"185963":55,"286835":-87,"300289":-76,"9512":77,"188403":-53},
"Y_Coordinate":{"185963":31,"286835":-22,"300289":29,"9512":-6,"188403":16},
"Distance":{"185963":46.7546789102,"286835":22.2036033112,"300289":168.514094366,"9512":14.3178210633,"188403":40.3112887415},
"Angle":{"185963":-41.5317707411,"286835":-82.2348339816,"300289":-9.9094996999,"9512":24.7751405688,"188403":23.3852210572},
"Shot_Type":{"185963":"Snap Shot","286835":"Wrist Shot","300289":"Wrist Shot","9512":"Snap Shot","188403":"Wrist Shot"},
"Last_event_type":{"185963":"Giveaway","286835":"Missed Shot","300289":"Faceoff","9512":"Blocked Shot","188403":"Faceoff"},
"X_last_event":{"185963":-43,"286835":-72,"300289":-69,"9512":63,"188403":20},
"Y_last_event":{"185963":37,"286835":-9,"300289":22,"9512":-11,"188403":22},
"Sec_from_lastEvent":{"185963":7.8,"286835":27.6,"300289":33.0,"9512":2.4,"188403":13.8},
"Dis_from_lastEvent":{"185963":98.1835016691,"286835":19.8494332413,"300289":9.8994949366,"9512":14.8660687473,"188403":73.2461603089},
"Rebond":{"185963":False,"286835":False,"300289":False,"9512":False,"188403":False},
"Angle_change":{"185963":0,"286835":0,"300289":0,"9512":0,"188403":0},
"Vitesse":{"185963":12.5876284191,"286835":0.7191823638,"300289":0.299984695,"9512":6.1941953114,"188403":5.307692776}
}
df=pd.DataFrame.from_dict(js)
print(x.predict(df))"""



#x =  GameClient(port=5001)
#print(x.get_game_events(2021020329))
#print(x.get_game_events(2021020329))
