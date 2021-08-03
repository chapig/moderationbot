import discord, os
from discord.ext import commands

token = ""
cogs = ["cogs.moderation"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True

class Bot(commands.AutoShardedBot):
    
    def __init__(self):

        super().__init__(command_prefix="-", intents=intents, reconnect=True)
        self.loop.create_task(self.ready())

    async def on_connect(self):
        os.system("clear")
        print("Bot is starting up...")
        

    async def ready(self):

        await self.wait_until_ready()
        os.system("clear")

        try:
            for cog in cogs:
                self.load_extension(cog)
        except Exception as error:
            print(f"Extension could not be loaded due to the following error: \n{error}")
            
        print("Bot is now running.")

Bot().run(token)
