from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import inspect
from players import get_last5_data

def insert_player(player_name):
    # connect to the database using your credentials
    username = 'root'
    password = 'szczupak2137'
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@localhost:3306/players', echo=False)
    metadata = MetaData()
    
    # define player_ids table structure
    player_ids = Table('player_ids', metadata, 
                        Column('player_id', Integer, primary_key=True, autoincrement=True),
                        Column('player', String(50), nullable=False)
                      )
    
    # use the inspect() method to check if player_ids table already exists, create if not
    inspector = inspect(engine)

    if not inspector.has_table('player_ids'): 
        metadata.create_all(engine)
        print('Table created.')
    else:
        print('Table already exists.')

    # insert values to the player_ids table
    with engine.connect() as conn:
        # check if a player instance already exists in the player_ids table
        query = text("SELECT player FROM player_ids")
        execution = conn.execute(query)
        result = execution.fetchall()

        players_list = []

        for player in result:
            players_list.append(player[0])
        
        # if not, add the player
        if player_name not in players_list:
            try:
                insert = player_ids.insert().values(player=player_name)
                result = conn.execute(insert)
                print('Player ID and player inserted.')
                conn.commit()
                player_id = result.inserted_primary_key[0] 
            except SQLAlchemyError as e:
                print(f"Error: {e}")
                return
        else:
            print(f"{player_name} already has his ID.")
            return

        # create corresponding player table
        if player_id:
            try:
                df = get_last5_data(player_name)
                if not df.empty:
                    # insert the player_id column as it's not the part of the dataframe
                    df.insert(0, 'player_id', player_id)
                    
                    # get the appropriate table name by using a simple join on the function parameter, which is player_name
                    table_name = ''.join([player_name.split()[0][0:], "_", player_name.split()[1][0:]]).lower()

                    # turn the dataframe to a custom sql table
                    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
                    print(f"{table_name} inserted.")
                    # modify the player_id column, as it's of bigint type initially, which prevents us from setting it as foreign key because the data types don't match
                    query = text(f'ALTER TABLE {table_name} MODIFY COLUMN player_id INT')
                    conn.execute(query)
                    print(f"{table_name} modified - player_id column set to INT.")
                    conn.commit()

                    # set the player_id column as a foreign key by referencing the same column from player_ids table
                    query = text(f'ALTER TABLE {table_name} ADD CONSTRAINT fk_playerid FOREIGN KEY (player_id) REFERENCES player_ids(player_id)')
                    print("Foreign key constraint added.")
                    conn.commit()
                    conn.close()
                else:
                    print("No data to insert for the player.")
            except Exception as e:
                print(f"An error occurred while inserting game data: {e}")
        else:
            print("Player ID not found")
