import discord, os, json
from discord.ext import commands
cogs = ["cogs.moderation"]

intents = discord.Intents.default()
intents.members = True
intents.presences = True

def bot_token():
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
        settings_file.close()
    return settings["bot_token"]



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

try:
    Bot().run(bot_token())
except discord.errors.LoginFailure:
    print("An error has occured with your token, make sure to place it in your settings.json and also make sure it is a valid token.")
