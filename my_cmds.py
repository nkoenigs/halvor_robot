import os
import discord
from discord.ext import commands

# class containing all of the Main commands for Halvor Persson
class Main_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # the Halvor Persson Meme
    @commands.command(name = 'hallo', help = 'gives life changing information about our lord and savior', category = 'main')
    async def hallo_wurold(self, ctx):
        await ctx.send('Hallo I, Halvor Persson, (born 11 March 1966) am a Norwegian former ski jumper!')

    # play the wet wet mud clip in call
    @commands.command(name = 'bae', help = 'play a relatable clip from i think you should leave')
    async def wet_wet_mud(self, ctx):
        try:
            tar = ctx.author.voice.channel
        except:
            await ctx.send(f'{ctx.author}, you need to be in a voice channel for me to play a clip')
        else:
            vc = await tar.connect()
            vc.play(discord.FFmpegPCMAudio('audio/wetwetmud.mp3'))
