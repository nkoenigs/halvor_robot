# Halvor Persson (born 11 March 1966) is a Norwegian former ski jumper.

# Nathan D. Koenigsmark
# discord bot for many things

# dependencies:
# $ pip install -U discord.py

import os
import discord


client = discord.Client()
new_member_role = "Simple Ricks"

# print a console message to confirm connection
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Send a DM to welcome newbies to the sever while also giveing them a role
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hallo {member.name}, welcome to the windowless room!')
    role = member.guild.roles.get('386317626533609472')
    await member.add_roles(role)
    

# yes i know this is bad practice but my .env file wouldn't load an I'm no superman
# just promise you won't read the next line okay?... okay.
client.run('NzE0NzI3NjI3MTEzMzY1NTA0.' + 'XszTuQ.UbPBWYzelALUzm0LmfOK97op_wY')