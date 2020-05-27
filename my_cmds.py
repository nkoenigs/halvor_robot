import asyncio
import discord
import ffmpeg
from discord.ext import commands

# class containing all of the Main commands for Halvor Persson
class Main_Commands(commands.Cog):   
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #plays a given audio clip in the call of ctx's sender
    async def play_audio_clip(self, ctx, clip):
        try:
            tar = ctx.author.voice.channel
        except:
            await ctx.send(f'{ctx.author}, you need to be in a voice channel for me to play a clip')
        else:
            vc = await tar.connect()
            try:
                vc.play(discord.FFmpegPCMAudio(clip))
            except Exception as inst:
                await ctx.send('This is clip could not be found, try complaing to sleepy about his shity bot please.')
                await ctx.send(f'If he asks about the error its {type(inst)}, {inst}')
            else:
                while vc.is_playing():
                    await asyncio.sleep(.1)
                vc.stop()
            finally:
                await vc.disconnect()

    # the Halvor Persson Meme
    @commands.command(name = 'hallo', help = 'gives life changing information about our lord and savior')
    async def hallo_wurold(self, ctx):
        await ctx.send('Hallo I, Halvor Persson, (born 11 March 1966) am a Norwegian former ski jumper!')

    # play the wet wet mud clip in call
    @commands.command(name = 'bae', help = 'play a relatable clip from i think you should leave')
    async def wet_wet_mud(self, ctx):
        await self.play_audio_clip(ctx, 'audio/wetwetmud.mp3')

    # play samanthas ayaya
    @commands.command(name = 's_ayayaya', help = 'play a clip of ayayaya')
    async def samantha_ayaya(self, ctx):
        await self.play_audio_clip(ctx, 'audio/samantha_ayayaya.mp3')

    # play e&a poop into wine clip
    @commands.command(name = 'wine', help = 'play a great e&a clip')
    async def samantha_ayaya(self, ctx):
        await self.play_audio_clip(ctx, 'audio/poopintowine.wav')

    # play issacs im a little fat girl
    @commands.command(name = 'shame', help = 'play ignohrs classic line')
    async def ignhor_shame(self, ctx):
        played_clip = False
        for role in ctx.author.roles:            
            if(role.id == 714980503282778133):
                await self.play_audio_clip(ctx, 'audio/imalittlefatgirl.mp3')
                played_clip = True
        if(not played_clip):
            await ctx.send('Sorry fam but this command isn\'t going to work for you.')

    # updates halvor to the newest version
    @commands.command(name = 'update', help = 'restarts me with the newest github pull')
    async def self_update(self, ctx):
        await ctx.send('Yeah this dosen\'t work yet fam')



