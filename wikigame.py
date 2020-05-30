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
        def __init__(self, member, name):
            self.member = member
            self.name = name
            self.article = None
            self.score = 0

    def find_player_obj(self, target):
        selected = None
        for player in self.player_list:
            if player.member.name == target:
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
    @commands.command(name = 'join_wiki', help = 'join an active wiki game as a new player (>join_wiki \'your name\')')
    async def join_wiki(self, ctx, tag):
        if not hash(ctx.channel) == hash(self.game_channel):
            await ctx.send(f'Please only join the game from the bot channel')
        elif not self.find_player_obj(ctx) == None:
            await ctx.send(f'Error, a player with the name {ctx.author.name} is already in this game')
        elif tag == None or len(tag) <= 1:
            await ctx.send(f'bad tag given')
        else:
            new_player = self.Players(ctx.author, tag)
            self.player_list.append(new_player)
            await ctx.send(f'{tag} has joined the wikipedia game!')
            if ctx.author.dm_channel == None:
                await ctx.author.create_dm()
            await ctx.author.dm_channel.send(f'Hallo {tag}, welcome to the wikipeadia game!, please send me your article (use cmd >my_article)')

    # leave the game
    @commands.command(name = 'leave_wiki', help = 'join an active wiki game as a new player')
    async def leave_wiki(self, ctx):
        target = self.find_player_obj(ctx.author.name)
        if target == None:
            await ctx.send(f'Error, a player with the name {ctx.author.name} is not in this game')
        else:
            try:
                self.player_list.remove(target)
                await ctx.send(f'You have been removed from the game with a final score of {target.score}, Thanks for Playing!')
            except:
                await ctx.send('There was an error removing you from the game')

    # prints out the current player scores
    @commands.command(name= 'scoreboard', help = 'check to see who is winning the wikigame atm!')
    async def wiki_scores(self, ctx):
        await ctx.send('SCOREBOARD:')
        for player in self.player_list:
            await ctx.send(f'{player.name} has a score of {player.score}')

    # give the bot my article for the game
    @commands.command(name = 'my_article', help = 'give halvor an article for the wikipedia game, type the title of your article after the commands (>my_article ___)')
    async def give_article(self, ctx, *argv):
        title = ''
        for arg in argv:
            title = title + arg + ' '
        this_player = self.find_player_obj(ctx.author.name)
        try:
            if this_player == None:
                await ctx.send(f'{ctx.author.name} is not in this wiki game. Try the >join_wiki_game command')
            elif len(title) <= 1 :
                await ctx.send(f'That article title is very short, im not going to acept it')
            else:
                this_player.article = title
                await ctx.send(f'your article has been set')
        except:
            await ctx.send('There was an error with this submission, try again i guess.')

    # start a round of the game
    @commands.command(name = 'draw', help = 'start a round of the game by drawing an article.')
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
    @commands.command(name = 'guess', help = 'place a guess as for who is the correct player')
    async def place_guess(self, ctx, guess):
        if not ctx.channel == self.game_channel:
            await ctx.send('This command should only be called in the main game channel')
        elif not ctx.author.name == self.current_guesser.member.name:
            await ctx.send('This command should only be called by the current guesser')
        else:
            guessed_player = None
            for player in self.player_list:
                if player.name == guess:
                    guessed_player = player
            if guessed_player == None:
                await ctx.send(f'{guess} is not a player in the game')
            elif guessed_player.name == self.current_guesser.name:
                await ctx.send('You can\' guess yourself fam')
            else:
                guessed_player.score += 1
                if guessed_player == self.correct_player:
                    self.current_guesser.score += 1
                    await ctx.send('Correct Guess!')
                else:
                    await ctx.send(f'Wrong! {self.correct_player.name} was the truth')
