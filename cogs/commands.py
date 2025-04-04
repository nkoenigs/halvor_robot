import logging

from discord.ext import commands

LOG = logging.getLogger('discord')
LOG.info("logger online cmd")

class CommandsCog(commands.Cog):   
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hallo', help='gives life changing information about our lord and savior')
    async def hallo_wurold(self, ctx):
        """
        Hello world command. Responds with all that is to be known about halvar persson

        Args:
            ctx (commands.Context): The context of the command invocation, providing message and channel info.
        """
        LOG.info("Hello world called")
        await ctx.send(f'Hallo {ctx.author.mention}! I, Halvor Persson, (born 11 March 1966) am a Norwegian former ski jumper.')

async def setup(bot):
    """
    Adds cog to bot. Required for "load_extension" call in main
    """
    await bot.add_cog(CommandsCog(bot))
