import logging
import discord
import io
import re

from datetime import datetime, timedelta
from discord.ext import commands

LOG = logging.getLogger('discord')
LOG.info("logger online cmd")
LOG_FILE = "bot.log"

class CommandsCog(commands.Cog):   
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hallo', help='gives life changing information about our lord and savior')
    async def hallo_wurold(self, ctx):
        """
        Hello world command. Responds with all that is to be known about halvar persson

        Args:
            ctx (commands.Context): The context of the command invocation.
        """
        LOG.info("Hello world called")
        await ctx.send(f'Hallo {ctx.author.mention}! I, Halvor Persson, (born 11 March 1966) am a Norwegian former ski jumper.')

    @commands.command(name='logs', help='returns logs from the last $1 minutes')
    async def logs(self, ctx, minutes: int = 10):
        """
        Returns bot logs from the last minutes

        Args:
            ctx (commands.Context): The context of the command invocation.
            minutes (int): Minutes back to get logs from
        """
        LOG.info("Get logs called")
        try:
            cutoff_time = datetime.now() - timedelta(minutes=minutes)
            log_lines = []

            timestamp_regex = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')

            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    match = timestamp_regex.match(line)
                    if match:
                        log_time = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                        if log_time >= cutoff_time:
                            log_lines.append(line)

            if not log_lines:
                await ctx.send(f"No logs found in the last {minutes} minutes.")
                return

            log_content = ''.join(log_lines)
            file = discord.File(io.StringIO(log_content), filename=f"logs_last_{minutes}_minutes.txt")
            await ctx.send(file=file)

        except Exception as e:
            await ctx.send(f"Error reading logs: {e}")

async def setup(bot):
    """
    Adds cog to bot. Required for "load_extension" call in main
    """
    await bot.add_cog(CommandsCog(bot))
