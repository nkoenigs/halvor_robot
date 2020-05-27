import asyncio
import copy
import discord
import wikipedia
from discord.ext import commands

#helper outside class?
# helper for scoreboard
def grab_score(player):
    return player.score

# class containing the update capabilties for Halvor Persson
class WikipediaGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.player_list = []
        
    # a inner class for a player in the game
    class Players:
        def __init__(self, member):
            self.member = member
            self.name = member.nick
            self.article = None
            self.score = 0

    # returns a list of all of the players names
    def list_names(self):
        name_list = []
        for player in self.player_list:
            name_list.append(player.name)
        return name_list

    # starts a new game
    @commands.command(name = 'new_wiki_game', help = 'restarts the wiki game with a fresh set of players and clues')
    async def new_wiki_game(self, ctx):
        self.player_list = []
        await ctx.send('A new game has been created, the old game is no more.')
    
    # prints out the current player scores
    # TODO test this shit
    @commands.command(name= 'wiki_scores', help = 'check to see who is winning the wikigame atm!')
    async def wiki_scores(self, ctx):
        my_list = copy.deepcopy(self.player_list)
        my_list.sort(key=grab_score)
        for player in my_list:
            await ctx.send(f'{player.name} has a score of {player.score}')
    
    # join the game as a new player
    @commands.command(name = 'join_wiki_game', help = 'join an active wiki game as a new player')
    async def join_wiki_game(self, ctx):
        name_list = self.list_names()
        if(ctx.author.nick in name_list):
            await ctx.send(f'Error, a player with the name {ctx.author.nick} is allready in this game')
        else:
            new_player = self.Players(ctx.author)
            self.player_list.append(new_player)
            await ctx.send(f'{ctx.author.nick} has joined the wikipedia game!')
            if(ctx.author.dm_channel == None):
                await ctx.author.create_dm()
            await ctx.author.dm_channel.send(f'Hallo {ctx.author.nick}, welcome to the wikipeadia game!, please send me your article (use cmd >my_article)')

    # give the bot my article for the game
    @commands.command(name = 'my_article', help = 'give halvor an article for the wikipedia game')
    async def give_article(self, ctx):
        name_list = self.list_names()
        if(not ctx.author.nick in name_list):
            await ctx.send(f'{ctx.author.nick} is not in this wiki game. Try the >join_wiki_game command')
        else