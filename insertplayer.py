from sqlalchemy import create_engine
from players import get_last5_data

def insert_player(player_name):
    df = get_last5_data(player_name) 
    player = ''.join([player_name.split()[0][0:], "_", player_name.split()[1][0:]]).lower()
    try:
        engine = create_engine('mysql+mysqlconnector://root:szczupak2137@localhost:3306/players', echo=False)
        df.to_sql(name=player, con=engine, if_exists='append', index=False)
        print("Success")
    except Exception as e:
        print(f"failed: {e}")
