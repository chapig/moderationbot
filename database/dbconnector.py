import mysql.connector
from mysql.connector import connection

class Conn:
  
  def __init__(self):
    
    self.cnx = mysql.connector.connect(  host="localhost",
                                          user="root",
                                          password="root",
                                          database="moderation_discord")
    self.cursor = self.cnx.cursor()


class Everyone:
  
  def fetchall(self):
    
    connection = Conn()
    connection.cursor.execute("SELECT * FROM discordmoderation WHERE CURTIME() >= muteduntil;")
    self.results = connection.cursor.fetchall()
    return self.results
        

class Result:
  
  def __init__(self, guild_id, user_id: int):
    
    connection = Conn()
    self.guild_id = guild_id
    self.user_id = user_id
    
    connection.cursor.execute(f"SELECT ismuted FROM discordmoderation WHERE userid = {self.user_id} AND guildid = {self.guild_id};")
    self.ismuted = connection.cursor.fetchone()[0]
    
    connection.cursor.execute(f"SELECT muteduntil FROM discordmoderation WHERE userid = {self.user_id} AND guildid = {self.guild_id};")
    self.muted_until = connection.cursor.fetchone()[0]
  
  def mute(self, istemporary:bool, during=None):
    
    connection = Conn()
    
    if istemporary and during is not None:
      
      connection.cursor.execute(f"UPDATE discordmoderation SET ismuted = 1, istempmute = 1, muteduntil = '{during}' WHERE guildid = {self.guild_id} AND userid = {self.user_id};")
      connection.cnx.commit()
    
    else: 
      
      connection.cursor.execute(f"UPDATE discordmoderation SET ismuted = 1 WHERE userid = {self.user_id} AND guildid = {self.guild_id};")
      connection.cnx.commit()
    

class User:
  
  def get(self, guild_id: int, user_id: int):
    
    self.guild_id = guild_id
    self.user_id = user_id
    connection = Conn()
    
    connection.cursor.execute("""CREATE TABLE IF NOT EXISTS discordmoderation
                   (userid BIGINT, guildid BIGINT, ismuted TINYINT(1) DEFAULT 0, 
                   istempmute TINYINT(1) DEFAULT 0, muteduntil TIME);""")
    
    connection.cursor.execute(  """ALTER TABLE discordmoderation ADD UNIQUE INDEX(userid, guildid)
                                """
                            )
    
    connection.cursor.execute(f"""INSERT IGNORE INTO discordmoderation
                              (userid, guildid) VALUES ({self.user_id}, {self.guild_id});""")
    connection.cnx.commit()
    return Result(guild_id, user_id)
  
  def remove(self, guild_id: int, user_id: int):
    
    self.guild_id = guild_id
    self.user_id = user_id
    connection = Conn()
    connection.cursor.execute(f"DELETE FROM discordmoderation WHERE guildid = {guild_id} AND userid = {user_id};")
    connection.cnx.commit()
