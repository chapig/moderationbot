import mysql.connector
from mysql.connector import connection
import json 

with open("settings.json") as settings_file:
    settings = json.load(settings_file)
    settings_file.close()
    
if settings["database"]["default"] == True:
  
  database_name = "moderation_discord" #DEFAULT
  table_name = "discordmoderation" #DEFAULT
  user_id_column_name = "userid" #DEFAULT
  guild_id_column_name = "guildid" #DEFAULT
  istemporary_mute_column_name = "istempmute" #DEFAULT
  ismuted_column_name = "ismuted" #DEFAULT
  muted_until_column_name =  "muteduntil" #DEFAULT
  
elif settings["database"]["default"] == False:
  
  database_name = settings["database"]["custom"]["name"]  
  table_name = settings["database"]["custom"]["table"]  
  database_host = settings["database"]["custom"]["host"]
  database_user = settings["database"]["custom"]["user"]
  database_password = settings["database"]["custom"]["password"] 

class Conn:
  
  def __init__(self):
    
    self.cnx = mysql.connector.connect(  host=settings["database"]["host"],
                                          user=settings["database"]["user"],
                                          password=settings["database"]["password"],
                                          database=database_name)
    self.cursor = self.cnx.cursor()


class Everyone:
  
  def fetchall(self):
    
    connection = Conn()
    connection.cursor.execute(f"SELECT * FROM {table_name} WHERE CURTIME() >= {muted_until_column_name};")
    self.results = connection.cursor.fetchall()
    return self.results
        

class Result:
  
  def __init__(self, guild_id, user_id: int):
    
    connection = Conn()
    self.guild_id = guild_id
    self.user_id = user_id
    
    connection.cursor.execute(f"SELECT {ismuted_column_name} FROM {table_name} WHERE {user_id_column_name} = {self.user_id} AND {guild_id_column_name} = {self.guild_id};")
    self.ismuted = connection.cursor.fetchone()[0]
    
    connection.cursor.execute(f"SELECT {muted_until_column_name} FROM {table_name} WHERE {user_id_column_name}  = {self.user_id} AND {guild_id_column_name} = {self.guild_id};")
    self.muted_until = connection.cursor.fetchone()[0]
  
  def mute(self, istemporary:bool, during=None):
    
    connection = Conn()
    
    if istemporary and during is not None:
      
      connection.cursor.execute(f"UPDATE {table_name} SET {ismuted_column_name} = 1, {istemporary_mute_column_name} = 1, {muted_until_column_name} = '{during}' WHERE {guild_id_column_name} = {self.guild_id} AND {user_id_column_name}  = {self.user_id};")
      connection.cnx.commit()
    
    else: 
      
      connection.cursor.execute(f"UPDATE {table_name} SET {ismuted_column_name} = 1 WHERE {user_id_column_name} = {self.user_id} AND {guild_id_column_name} = {self.guild_id};")
      connection.cnx.commit()
    

class User:
  
  def get(self, guild_id: int, user_id: int):
    
    self.guild_id = guild_id
    self.user_id = user_id
    connection = Conn()
    
    connection.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}
                              ({user_id_column_name} BIGINT, {guild_id_column_name} BIGINT, {ismuted_column_name} TINYINT(1) DEFAULT 0, 
                              {istemporary_mute_column_name} TINYINT(1) DEFAULT 0, {muted_until_column_name} TIME);""")
    
    connection.cursor.execute(  f"""ALTER TABLE {table_name} ADD UNIQUE INDEX({user_id_column_name}, {guild_id_column_name})
                                """
                            )
    
    connection.cursor.execute(f"""INSERT IGNORE INTO {table_name}
                              ({user_id_column_name}, {guild_id_column_name}) VALUES ({self.user_id}, {self.guild_id});""")
    connection.cnx.commit()
    return Result(guild_id, user_id)
  
  def remove(self, guild_id: int, user_id: int):
    
    self.guild_id = guild_id
    self.user_id = user_id
    connection = Conn()
    connection.cursor.execute(f"DELETE FROM {table_name} WHERE {guild_id_column_name} = {guild_id} AND {user_id_column_name}= {user_id};")
    connection.cnx.commit()
