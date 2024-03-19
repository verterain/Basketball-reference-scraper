The program retrieves the data from basketball-reference.com for a specified player, returning his performance in the last 5 games.
The data is stored in pandas dataframe, and then pushed to mysql database. All of the players have dedicated tables created dynamically from the script level.

To use the script, first run createdb.py script to create players database that will be our main place for data storage. The script assumes that your MySQL runs on localhost. Remember to edit username and passwrd variables with your data. Then, fill the same variables in insertplayer.py so the engine runs as it should. Now the script is ready to run through terminal of your choice. For powershell it's:

\path\> py main.py 'Player Name'

Plans for the future:
  - Create player_id table that will store all player names and id's as a primary key so we can join tables and compare performances of multiple players on desired conditions
  - Updating tables, so the script inserts latest performance if table of last 5 games for a specific player already exists; instead of overwriting previous 5 games with new 5 games, we append the table with additional rows (maybe based on the date column?)
