import asyncio
import discord
import ffmpeg
from discord.ext import commands

# class containing all of the Main commands for Halvor Persson
class Main_Commands(commands.Cog):   
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # TODO add audio balanceing so we can amp up bae

    #plays a given audio clip in the call of ctx's sender
    async def play_audio_clip(self, ctx, clip):
        try:
            tar = ctx.author.voice.channel
        except:
            await ctx.send(f'{ctx.author}, you need to be in a voice channel for me to play a clip')
        else:
            vc = await tar.connect()
            print('trying to play clip: ' + str(clip))
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

    # updates halvor to the newest version
    @commands.command(name = 'update', help = 'restarts me with the newest github pull')
    async def self_update(self, ctx):
        await ctx.send('Yeah this dosen\'t work yet fam')



