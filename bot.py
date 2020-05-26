# Halvor Persson (born 11 March 1966) is a Norwegian former ski jumper.

# Nathan D. Koenigsmark
# discord bot for many things

# dependencies:
# $ pip install -U discord.py

import os
import discord

# yes i know this is bad practice but my .env file wouldn't load an I'm no superman
# just promise you won't read the next line okay?... okay.
TOKEN = 'NzE0NzI3NjI3MTEzMzY1NTA0.' + 'XszTuQ.UbPBWYzelALUzm0LmfOK97op_wY'

client = discord.Client()

# print a console message to confirm connection
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Send a DM to welcome newbies to the sever
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hallo {member.name}, welcome to the windowless room!')
    await member.dm_channel.send(f'Be sure to check into the "roles" channel to give yourself a role.')


client.run(TOKEN)
