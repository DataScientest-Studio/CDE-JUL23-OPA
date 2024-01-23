import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('database')
)

mycursor = db.cursor()

# Creation des tables
mycursor.execute("CREATE TABLE symbol (id INTEGER NOT NULL, symbol VARCHAR(255),PRIMARY KEY (id))")
mycursor.execute("CREATE TABLE granularity (id INTEGER NOT NULL, granularity VARCHAR(255),PRIMARY KEY (id))")

# Insertion des valeurs
sql = "INSERT INTO symbol (id, symbol) VALUES (%s, %s)"
val = [
  (1, 'BTCEUR'),
 (2, 'ETHEUR')  
]

mycursor.executemany(sql,val)
db.commit()

sql = "INSERT INTO granularity (id, granularity) VALUES (%s, %s)"
val = [
  (1, '1_HOUR'),
  (2, '1_DAY')  
]

mycursor.executemany(sql,val)
db.commit()

# creation de la table history_Data
mycursor.execute("CREATE TABLE history_Data (id INTEGER NOT NULL AUTO_INCREMENT, close_time DATETIME,symbol_id INTEGER,granularity_id INTEGER,open FLOAT,high FLOAT,low FLOAT,close FLOAT,volume FLOAT, PRIMARY KEY (id),FOREIGN KEY(symbol_id) REFERENCES symbol (id),FOREIGN KEY(granularity_id) REFERENCES granularity (id))")

db.commit()


# faire quelque chose d'utile avec la connexion

db.close()
