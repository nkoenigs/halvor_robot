import asyncio
import copy
import discord
import random
from discord.ext import commands

# class containing the update capabilties for Halvor Persson
class WikipediaGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player_list = []
        self.correct_player = None
        self.current_guesser = None
        self.guesser_index = 0
        self.game_channel = None

    # a inner class for a player in the game
    class Players:
        def __init__(self, member):
            self.member = member
            self.article = None
            self.score = 0

    def find_player_obj(self, target):
        selected = None
        for player in self.player_list:
            if player.nick == target:
                selected = player
        return selected

    # starts a new game
    @commands.command(name = 'new_wiki', help = 'restarts the wiki game with a fresh set of players and clues')
    async def new_wiki(self, ctx):
        self.player_list = []
        self.guesser_index = 0
        self.game_channel = ctx.channel
        await ctx.send('A new game has been created, the old game is no more.')

    # join the game as a new player
    @commands.command(name = 'join_wiki', help = 'join an active wiki game as a new player')
    async def join_wiki(self, ctx):
        if not hash(ctx.channel) == hash(self.game_channel):
            await ctx.send(f'Please only join the game from the bot channel')
        elif not self.find_player_obj(ctx) == None:
            await ctx.send(f'Error, a player with the name {ctx.author.nick} is already in this game')
        else:
            new_player = self.Players(ctx.author)
            self.player_list.append(new_player)
            await ctx.send(f'{ctx.author.nick} has joined the wikipedia game!')
            if ctx.author.dm_channel == None:
                await ctx.author.create_dm()
            await ctx.author.dm_channel.send(f'Hallo {ctx.author.nick}, welcome to the wikipeadia game!, please send me your article (use cmd >my_article)')

    # leave the game
    @commands.command(name = 'leave_wiki', help = 'join an active wiki game as a new player')
    async def leave_wiki(self, ctx):
        target = self.find_player_obj(ctx)
        if target == None:
            await ctx.send(f'Error, a player with the name {ctx.author.nick} is not in this game')
        else:
            try:
                self.player_list.remove(target)
                await ctx.send(f'You have been removed from the game with a final score of {target.score}, Thanks for Playing!')
            except:
                await ctx.send('There was an error removing you from the game')

    # prints out the current player scores
    @commands.command(name= 'wiki_scores', help = 'check to see who is winning the wikigame atm!')
    async def wiki_scores(self, ctx):
        await ctx.send('SCOREBOARD:')
        for player in self.player_list:
            await ctx.send(f'{player.name} has a score of {player.score}')

    # give the bot my article for the game
    @commands.command(name = 'my_article', help = 'give halvor an article for the wikipedia game, type the title of your article after the commands (>my_article ___)')
    async def give_article(self, ctx, title):
        this_player = self.find_player_obj(ctx.author.nick)
        try:
            if this_player == None:
                await ctx.send(f'{ctx.author.nick} is not in this wiki game. Try the >join_wiki_game command')
            elif len(title) <= 1 :
                await ctx.send(f'That article title is very short, im not going to acept it')
            else:
                this_player.article = title
                await ctx.send(f'your article has been set')
        except:
            await ctx.send('There was an error with this submission, try again i guess.')

    # start a round of the game
    @commands.command(name = 'wiki_draw', help = 'start a round of the game by drawing an article.')
    async def draw_article(self, ctx):
        if not ctx.channel == self.game_channel:
            await ctx.send('This command should only be called in the main game channel')
            return
        if len(self.player_list) < 2:
            await ctx.send('Game needs atleast 2 players fam')
            return
        for player in self.player_list:
            if player.article == None:
                await ctx.send(f'{player.name} has not submited an article yet.')
                return
        self.current_guesser = self.player_list[self.guesser_index]
        self.guesser_index += 1
        if self.guesser_index >= len(self.player_list):
            self.guesser_index = 0
        while True:
            drawn = random.choice(self.player_list)
            if not drawn == self.current_guesser:
                break
        self.correct_player = drawn
        await ctx.send(f'{self.current_guesser.name} is guessing for the following article title: {self.correct_player.article}')

    # place a guess
    @commands.command(name = 'wiki_guess', help = 'place a guess as for who is the correct player')
    async def place_guess(self, ctx, guess):
        if not ctx.channel == self.game_channel:
            await ctx.send('This command should only be called in the main game channel')
        elif not ctx.author.nick == self.current_guesser.name:
            await ctx.send('This command should only be called by the current guesser')
        elif ctx.author.nick == guess:
            await ctx.send('You can\' guess yourself fam')
        else:
            guessed_player = self.find_player_obj(guess)
            if guessed_player == None:
                await ctx.send(f'{guess} is not a player in the game')
            guessed_player.score += 1
            if guessed_player == self.correct_player:
                self.current_guesser.score += 1
                await ctx.send('Correct Guess!')
            else:
                await ctx.send(f'Wrong! {self.correct_player} was the truth')

    


# #helper outside class?
# # helper for scoreboard
# def grab_score(player):
#     return player.score

# # class containing the update capabilties for Halvor Persson
# class WikipediaGame(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.last_member = 0
#         self.player_list = []
#         self.correct_player = None
#         self.game_channel = None
        
#     # a inner class for a player in the game
#     class Players:
#         def __init__(self, member):
#             self.member = member
#             self.name = member.nick
#             self.article = None
#             self.score = 0

#     # returns a list of all of the players names
#     def list_names(self):
#         name_list = []
#         for player in self.player_list:
#             name_list.append(player.name)
#         return name_list

#     # starts a new game
#     @commands.command(name = 'new_wiki_game', help = 'restarts the wiki game with a fresh set of players and clues')
#     async def new_wiki_game(self, ctx):
#         self.player_list = []
#         self.last_member = 0
#         self.game_channel = ctx.channel
#         await ctx.send('A new game has been created, the old game is no more.')
    
#     # prints out the current player scores
#     # TODO test this shit
#     @commands.command(name= 'wiki_scores', help = 'check to see who is winning the wikigame atm!')
#     async def wiki_scores(self, ctx):
#         my_list = copy.deepcopy(self.player_list)
#         my_list.sort(key=grab_score)
#         for player in my_list:
#             await ctx.send(f'{player.name} has a score of {player.score}')
    
#     # join the game as a new player
#     @commands.command(name = 'join_wiki_game', help = 'join an active wiki game as a new player')
#     async def join_wiki_game(self, ctx):
#         name_list = self.list_names()
#         if ctx.author.nick in name_list:
#             await ctx.send(f'Error, a player with the name {ctx.author.nick} is allready in this game')
#         else:
#             new_player = self.Players(ctx.author)
#             self.player_list.append(new_player)
#             await ctx.send(f'{ctx.author.nick} has joined the wikipedia game!')
#             if ctx.author.dm_channel == None:
#                 await ctx.author.create_dm()
#             await ctx.author.dm_channel.send(f'Hallo {ctx.author.nick}, welcome to the wikipeadia game!, please send me your article (use cmd >my_article)')

#     # give the bot my article for the game
#     @commands.command(name = 'my_article', help = 'give halvor an article for the wikipedia game, type the title of your article after the commands (>my_article ___)')
#     async def give_article(self, ctx, title):
#         this_player = None
#         for player in self.player_list:
#             if player.name == ctx.author.nick:
#                 this_player = player
#         try:
#             if this_player == None:
#                 await ctx.send(f'{ctx.author.nick} is not in this wiki game. Try the >join_wiki_game command')
#             elif len(title) <= 1 :
#                 await ctx.send(f'That article title is very short, im not going to acept it')
#             else:
#                 this_player.article = title
#                 await ctx.send(f'your article has been set')
#         except:
#             await ctx.send('There was an error with this submission, try again i guess.')

#     # give my answer (guesser only plz)
#     @commands.command(name = 'guess', help = 'for guesser use only! select who\'s article you think was true (>guess ____)')
#     async def guess(self, ctx, guess):
#         name_list = self.list_names()
#         if not guess in name_list:
#             await ctx.send(f'{guess} is not a player in the game, try again')
#         elif ctx.author.nick == guess:
#             await ctx.send('Hey asshole you can\' guess yourself')
#         elif not ctx.channel == self.game_channel:
#             await ctx.send('You can\'t report a score from a DM you dirty cheater')
#         else:
#             this_player = None
#             for player in self.player_list:
#                 if player.name == ctx.author.nick:
#                     this_player = player
#             this_player.score += 1
#             if guess == self.correct_player:
