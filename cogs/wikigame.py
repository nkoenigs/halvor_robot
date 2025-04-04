import discord 
import logging

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional
from discord.ext import commands

LOG = logging.getLogger('discord')
LOG.info("logger online wiki")

class Gamestate(Enum):
    """
    Enum for the current state of any given wiki game
    """
    ADD_PLAYERS = 1
    READ_WIKI = 2
    BETWEEN_ROUNDS = 3
    LIVE_ROUND = 4
    ENDGAME = 5

class WikipediaGame(commands.Cog):
    """
    Cog class containing the commands for the wiki game
    """
    def __init__(self, bot):
        self.bot = bot
        self.games = []

    @dataclass
    class SingleGame():
        """
        Dataclass for the details of any single game
        """
        state: Gamestate = Gamestate.ADD_PLAYERS
        thread: discord.threads.Thread=None
        join_msg: discord.message.MessageReference=None
        players: List["discord.User"]=field(default_factory=list)

    @commands.command(name='new_game', help='starts a new wiki game')
    async def setup_game(self, ctx):
        """
        Creates a new wiki game in a thread.
        Opens the game with a message that users can react to to join as players.
        Fails and alerts the prompter if the message is allready in a thread.

        Args:
            ctx (commands.Context): The context of the command invocation
        """
        LOG.info(f"Setup game command {_strfy_ctx(ctx)}")

        # Check if the message is already in a thread
        if isinstance(ctx.channel, discord.Thread):
            await ctx.send("This command is already part of a thread, I cannot create a new game "
                           "as a nested thread.")
            return
        
        # Setup Game
        game = WikipediaGame.SingleGame()
        self.games.append(game)
        game.thread = await ctx.message.create_thread(name="Wikipedia Game")
        game.join_msg = await game.thread.send("React to this message to join the wiki game!")
        await game.join_msg.add_reaction("👍")

    @commands.command(name='start_game', help='starts the game. Only call this in a wiki game '
                      'thread after all players have reacted to the new game')
    async def start_game(self, ctx):
        """
        Starts the game with the current players. deal out articles to everyone in dms. joins call to set a timer on reading articles.
        """
        LOG.info(f"Start game command {_strfy_ctx(ctx)}")

        # get the game
        game = self._get_game(ctx)
        if game is None:
            await ctx.send("A single valid game could not be found for this thread. Consider "
                           "deleting it and starting a new game.")
            return
        
        # check the game state
        if game.state != Gamestate.ADD_PLAYERS:
            await ctx.send("This game has allready started")
            return
        game.state = Gamestate.READ_WIKI

        # get the list of players
        for reaction in game.join_msg.reactions:
            game.players = await reaction.users().flatten()
        game.players = list(set(game.players))
        game.players.remove(self.bot.user)
        await ctx.send(game.players)

        

    def play_round():
        """
        deal out one article from the hat and declare who is judge for the round
        """
        pass

    def end_game_early():
        """
        ends the game early
        """
        pass

    def _get_game(self, ctx) -> Optional["SingleGame"]:
        """
        Gets the current game based on the thread this commands context is from.
        Replys to the user and returns None if context has no single matching thread.

        Args:
            ctx (commands.Context): The context of the command invocation

        Returns:
            Game for the current thread or None if it could not be found.
        """
        valid_games = [game for game in self.games if ctx.channel == game.thread]
        if len(valid_games) == 1:
            return valid_games[0]
        LOG.info(f"Found {len(valid_games)} valid games with command {_strfy_ctx(ctx)}")
        return None
            

    @commands.command(name="debug") # TODO remove
    async def debug(self, ctx):
        # Triggering pdb (Python Debugger)
        await ctx.send("Opening debugger...")
        import pdb
        pdb.set_trace()  # This will start the debugger in the console

def _strfy_ctx(ctx) -> str:
    """
    Helper method get a end tag for more useful logs from context 

    Args:
        ctx (commands.Context): The context of the command invocation
    """
    return f" from user {ctx.author.name} with ID {ctx.message.id}"

async def setup(bot):
    """
    Adds cog to bot. Required for "load_extension" call in main
    """
    await bot.add_cog(WikipediaGame(bot))
