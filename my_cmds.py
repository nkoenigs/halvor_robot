# class containing all of the Main commands for Halvor Persson

import os
import discord
from discord.ext import commands

class Main_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # the Halvor Persson Meme
    @commands.command(name = 'hallo', help = 'gives life changing information about our lord and savior', category = 'main')
    async def hallo_wurold(self, ctx):
        await ctx.send('Hallo I, Halvor Persson, (born 11 March 1966) am a Norwegian former ski jumper!')
