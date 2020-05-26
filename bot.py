# Halvor Persson (born 11 March 1966) is a Norwegian former ski jumper.

# Nathan D. Koenigsmark
# discord bot for many things

# dependencies:
# $ pip install -U discord.py

import os
import discord
from discord.ext import commands

from my_cmds import Main_Commands

bot = commands.Bot(command_prefix='>')
bot.add_cog(Main_Commands(bot))

# print a console message to confirm connection
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Send a DM to welcome newbies to the sever while also giveing them a role
# TODO :test giveing role to a new account
@bot.event
async def on_member_join(member):
    if(await member.dm_channel == None):
        await member.create_dm()
    await member.dm_channel.send(f'Hallo {member.name}, welcome to the windowless room!')
    role = member.guild.roles.get('386317626533609472')
    await member.add_roles(role)

if __name__ == "__main__":
    # yes i know this is bad practice but my .env file wouldn't load an I'm no superman
    # just promise you won't read the next line okay?... okay.
    bot.run('NzE0NzI3NjI3MTEzMzY1NTA0.' + 'XszTuQ.UbPBWYzelALUzm0LmfOK97op_wY')