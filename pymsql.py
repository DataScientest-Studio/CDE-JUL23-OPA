import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="opa_user",
    password="opa_pwd",
    database="opa_db"
)

mycursor = db.cursor()

#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

#mycursor.execute("SHOW TABLES")

#for x in mycursor:
#  print(x)


mycursor.execute("CREATE TABLE symbol (id INTEGER NOT NULL, symbol VARCHAR(255),PRIMARY KEY (id))")
mycursor.execute("CREATE TABLE granularity (id INTEGER NOT NULL, granularity VARCHAR(255),PRIMARY KEY (id))")

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

mycursor.execute("CREATE TABLE history_Data (id INTEGER NOT NULL AUTO_INCREMENT, close_time DATETIME,symbol_id INTEGER,granularity_id INTEGER,open FLOAT,high FLOAT,low FLOAT,close FLOAT,volume FLOAT, PRIMARY KEY (id),FOREIGN KEY(symbol_id) REFERENCES symbol (id),FOREIGN KEY(granularity_id) REFERENCES granularity (id))")

db.commit()


# faire quelque chose d'utile avec la connexion

db.close()
