import mysql.connector as msql

username = 'root'  # <- enter your mysql username
passwrd = 'szczupak2137'  # <- enter the corresponding password
conn = msql.connect(host='localhost', user=username, password=passwrd)

cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
dbs = [db[0] for db in cursor.fetchall()]
if 'players' in dbs:
    print("Database already exists.")
else:
    cursor.execute("CREATE DATABASE players")
    print("Database created.")