import discord 
import logging
import random
import requests
import asyncio

from enum import Enum
from utils import catch_exception
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Generator
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
    class SingleWiki:
        title: str
        expert: Optional["discord.User"]
        researcher: Optional["discord.User"] = None
        claimed_expert: Optional["discord.User"] = None

    @dataclass
    class SingleGame:
        """
        Dataclass for the details of any single game
        """
        wikis_per_player: int
        options_per_player: int
        sec_to_read: int
        state: Gamestate = Gamestate.ADD_PLAYERS
        thread: discord.threads.Thread=None
        join_msg: discord.message.MessageReference=None
        players: List["discord.User"]=field(default_factory=list)
        wikis: List["WikipediaGame.SingleWiki"]=field(default_factory=list)
        index: int=0

    
    @commands.command(name='new_game', help='starts a new wiki game. Optional: call as >new_game '
                      '$1 $2 $3 to set the number of selected wikis per player, the total number '
                      'of wikis to show each player, and the seconds to read up')
    async def setup_game(self, ctx, wikis_per_player: int=1, options_per_player: int=3, 
                         seconds_to_read: int=120):
        """
        Creates a new wiki game in a thread.
        Opens the game with a message that users can react to to join as players.
        Fails and alerts the prompter if the message is allready in a thread.

        Args:
            ctx (commands.Context): The context of the command invocation
            wikis_per_player (int): number of selected wikis per player
            options_per_player (int): number of optional wikis to show each player
            seconds_to_read (int): number of seconds to read the wikis
        """
        LOG.info(f"Setup game command {_strfy_ctx(ctx)}")

        # Check if the message is already in a thread
        if isinstance(ctx.channel, discord.Thread):
            await ctx.send("This command is already part of a thread, I cannot create a new game "
                           "as a nested thread.")
            return
        
        # check for valid args
        if wikis_per_player < 1 or wikis_per_player > options_per_player:
            await ctx.send("Invalid number of wikis and options given in command")
            return
        
        # Setup Game
        game = WikipediaGame.SingleGame(wikis_per_player, options_per_player, seconds_to_read)
        self.games.append(game)
        game.thread = await ctx.message.create_thread(name="Wikipedia Game")
        game.join_msg = await game.thread.send("React to this message to join the wiki game!")
        await game.join_msg.add_reaction("👍")

    @commands.command(name='deal', help='starts the game. Only call this in a wiki game '
                      'thread after all players have reacted to the new game')
    async def start_game(self, ctx):
        """
        Starts the game with the current players. 
        Deal out articles to everyone in dms. 
        Shuffles the hat and assigns guessers.

        Args:
            ctx (commands.Context): The context of the command invocation
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
            await ctx.send("This game has already started")
            return
        game.state = Gamestate.READ_WIKI

        # # get the list of players
        game.players = await self._get_reactors(ctx.channel, game.join_msg)

        # get wiki articles
        try:
            all_wikis = self._get_random_wikipedia_pages(game.options_per_player*len(game.players))
        except requests.exceptions.RequestException as e:
            LOG.error("Issue reaching wiki API from " + str(e))
            await ctx.send("Error reaching wiki API")
            return
        
        # send players their wikis
        await ctx.send("Sending out wikis!")
        wiki_iterator = iter(all_wikis.items())
        player_offers = {}
        for player in game.players:
            await player.send(
                f"Welcome to the wiki game! Here are your options for subjects to become the expert"
                f" on. React to the ones you are okay playing with. {game.wikis_per_player} will "
                f"be selected at the end of {game.sec_to_read} seconds.")
            player_offers[player] = []
            for i in range(0, game.options_per_player):
                title, url = next(wiki_iterator)
                msg = await player.send(url)
                await msg.add_reaction("✅")
                player_offers[player].append((title, msg))

            LOG.info(player_offers)

        # wait for read time
        LOG.info(f"waiting for {game.sec_to_read} seconds")
        await asyncio.sleep(game.sec_to_read)

        # select all articles for hat
        for player in game.players:
            accepted = []
            rejected = []
            selected = []
            await player.send("Times up!")

            # check reactions on each offered wiki
            for (offer_title, offer_msg) in player_offers[player]:
                reactors = await self._get_reactors(player.dm_channel, offer_msg)
                if len(list(set(reactors))):
                    accepted.append(offer_title)
                else:
                    rejected.append(offer_title)

            # select wikis for game
            while len(selected) < game.wikis_per_player:
                if accepted:
                    selected.append(WikipediaGame.SingleWiki(
                        accepted.pop(random.randrange(len(accepted))), player))
                else:
                    selected.append(WikipediaGame.SingleWiki(
                        rejected.pop(random.randrange(len(rejected))), player))
                game.wikis.extend(selected)
            LOG.info(f"Player {player.name} selected {selected}")

        # shuffle wikis
        guesser_list = game.players * game.wikis_per_player  
        for _ in range(1000):  # Try 1000 times to ensure no guesser is paired with their player
            random.shuffle(guesser_list)
            random.shuffle(game.wikis)
            guess_iter = iter(guesser_list)
            valid_pairs = True
            for wiki in game.wikis:
                wiki.researcher = next(guess_iter)
                if wiki.researcher == wiki.expert:
                    valid_pairs = False
                    break
            if valid_pairs:
                break
        else:
            await ctx.send("Something went wrong, couldn't pair guessers correctly.")
            return
        await ctx.send("Game is ready! Draw a subject.")
        game.state = Gamestate.BETWEEN_ROUNDS
            
    @commands.command(name='draw', help='play a round of the game')
    async def play_round(self, ctx):
        """
        deal out one article from the hat and declare who is judge for the round
        """
        game = self._get_game(ctx)
        if game is None:
            await ctx.send("A single valid game could not be found for this thread. Consider "
                           "deleting it and starting a new game.")
            return
        if game.state != Gamestate.BETWEEN_ROUNDS:
            await ctx.send("Now is not the time to draw for this game")
            return
        game.state = Gamestate.LIVE_ROUND
        await ctx.send(f"For this round the reasercher will be {game.wikis[game.index].researcher} and"
                       f" topic will be {game.wikis[game.index].title}. Good luck identifying the "
                       "expert in the room!")

    @commands.command(name='expert_is', help='for entering the the reaserchers selction for the expert')
    async def end_round(self, ctx, expert: Optional['discord.User']=None):
        # get game
        game = self._get_game(ctx)
        if game is None:
            await ctx.send("A single valid game could not be found for this thread. Consider "
                           "deleting it and starting a new game.")
            return

        # insure valid input
        if ctx.author != game.wikis[game.index].researcher:
            await ctx.send("This user is not the reasercher")
            return
        if expert is None:
            await ctx.send("Given expert is not a discord user")
            return
        if expert == game.wikis[game.index].researcher or expert not in game.players:
            await ctx.send("Given expert is not a valid guess")
            return
        
        #update with selected expoert
        game.wikis[game.index].claimed_expert = expert
        game.index += 1
        if game.index < len(game.wikis):
            game.state = Gamestate.BETWEEN_ROUNDS
            await ctx.send("Selection recorded! Draw when ready.")
            return
        
        # game over! score and report
        game.state = Gamestate.ENDGAME
        result_str = "GAME OVER. The true experts where:\ntitle  -- expert -- result\n"
        scores = {player: 0 for player in game.players}
        for wiki in game.wikis:
            result = wiki.expert == wiki.claimed_expert
            result_str += f"{wiki.title} -- {wiki.expert} -- {_emojyfy(result)}\n"
            if result:
                scores[wiki.researcher] += 1
            scores[wiki.claimed_expert] += 1
        result_str += "SCORES:\n"
        for player, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
            result_str += f"{player}: {score}\n"
        result_str += "Thanks for playing!"
        await ctx.send(result_str)

    async def _get_reactors(self, channel, msg) -> List["discord.User"]:
        """
        Get the list of unique users to react to a message excluding this bot

        Args:
            channel (discord.Channel): channel to find the message in
            msg (discord.Message): message to get reactions from

        Returns:
            list of users who reacted to the message
        """
        updated_msg = await channel.fetch_message(msg.id)
        reactions = []
        for reaction in updated_msg.reactions:
            reactions.extend([user async for user in reaction.users() if user != self.bot.user])
        return list(set(reactions))

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

    def _get_random_wikipedia_pages(self, number_of_pages) -> dict[str, str]:
        """
        Fetches random English Wikipedia page titles and URLs.

        Args:
            number_of_pages (int): Number of random pages to fetch (max 500 for bots, 10 for users).

        Returns:
            title and url for each page.
        """
        endpoint = "https://en.wikipedia.org/w/api.php"
        collected = {}
        batch_size = min(10, number_of_pages)  # Max 10 for anonymous users per request

        while len(collected) < number_of_pages:
            params = {
                "action": "query",
                "format": "json",
                "list": "random",
                "rnnamespace": 0,
                "rnlimit": min(batch_size, number_of_pages - len(collected))
            }

            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()

            for page in data["query"]["random"]:
                title = page["title"]
                collected[title] = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

        return collected

def _strfy_ctx(ctx) -> str:
    """
    Helper method get a end tag for more useful logs from context 

    Args:
        ctx (commands.Context): The context of the command invocation
    """
    return f" from user {ctx.author.name} with ID {ctx.message.id}"

def _emojyfy(bool) -> str:
    """
    Helper to turn a bool into a good or bad emoji

    Args:
        bool (bool): given bool

    Returns ✅ or ❌
    """
    return "✅" if bool else "❌"

async def setup(bot):
    """
    Adds cog to bot. Required for "load_extension" call in main
    """
    await bot.add_cog(WikipediaGame(bot))
