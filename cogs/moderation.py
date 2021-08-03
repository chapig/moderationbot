import discord, arrow, asyncpg, json
from discord.ext import commands, tasks
from bot_configuration import mute_user, update

with open("settings.json") as settings_file:
    settings = json.load(settings_file)
    settings_file.close()
    
owner_id = settings["owner"]

def owner_or_permissions(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)

class Moderation(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.unmutecheck.add_exception_type(asyncpg.PostgresConnectionError)
        self.unmutecheck.start()
    
    @commands.command(aliases=["mutetemp, tempmute"])
    @commands.guild_only()
    @owner_or_permissions(administrator=True)
    async def temp_mute(self, ctx, member: discord.Member, time_in_sec: int, reason:str = None):
        """
        Temporary mute command, time must be set in seconds.
        """
        
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if role is not None:
        
            user = mute_user.get(guild_id=ctx.guild.id, user_id=member.id)
            arrowtime = arrow.now().shift(seconds=time_in_sec).format('HH:mm:ss')
            humanized_time = arrow.now().shift(seconds=time_in_sec).humanize()
            if not user.ismuted:
                user.mute(istemporary=True, during=arrowtime)
                await member.add_roles(role, reason=reason if reason is not None else 'Temporary mute was applied to this user.')
                await ctx.send(f"> Member **{member.mention}** was **succesfully** muted and will be unmuted **{humanized_time}**. \n> **Reason for mute:** {reason if reason is not None else 'Temporary mute was applied to this user.'}")
            else:
                await ctx.send(f"> **{member.display_name}** has **already** been muted and will be unmuted in **{user.muted_until}**, current time for the bot is **{arrow.now().format('HH:mm:ss')}**.")
                
        else:
            await ctx.send(":exclamation: Before using this command, make sure to create a role named `Muted`.")
        
    @tasks.loop(seconds=5.0)
    async def unmutecheck(self):
        results = update.fetchall()
        for each in results:
              
            guild = self.client.get_guild(each[1]) # each[1] stands for guild id
            member = guild.get_member(each[0]) # each[1] stands for member id
            
            try:
                #We could also add personalized role.
                role = discord.utils.get(guild.roles, name="Muted")
                await member.remove_roles(role, reason="Unmuted by Bot, this was caused by temporary mute.")
                mute_user.remove(guild_id=each[1], user_id=each[0]) #We remove the row from the database.
            except Exception:
                pass
      
def setup(client):
    client.add_cog(Moderation(client))
