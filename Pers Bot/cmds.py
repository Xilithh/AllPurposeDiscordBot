import discord
import typing
import wavelink
from discord.ext import commands

channelID = []
GDCVC = []
x = 1
@commands.command(name="profile")
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    name = member.display_name
    pfp = member.display_avatar
    join = member.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S")
    acc_age = member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S")

    guild_icon_url = ctx.guild.icon.url if ctx.guild.icon else None

    profile = discord.Embed(title="User Profile", description=f'{name}', color=discord.Color.blue())
    profile.set_author(name=f'{ctx.guild.name}', icon_url=guild_icon_url)
    profile.set_thumbnail(url=pfp)
    profile.add_field(name='Username', value=f'{member.mention}', inline=False)
    profile.add_field(name='Date Joined', value=join)
    profile.add_field(name='Account Created at', value=acc_age, inline=False)
    profile.add_field(name='Role(s)', value=' '.join([role.mention for role in member.roles if role.name != '@everyone']), inline=False)
    profile.set_footer(text=f'{ctx.author} generated this request')

    await ctx.send(embed=profile)


    
def setup_commands(bot):
    @bot.command(name="play")
    async def play(ctx, *, search: str):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect(cls=wavelink.Player)
                
            else:
                await ctx.send("You need to be in a voice channel to play music.")
                return

        vc: wavelink.Player = ctx.voice_client
        
        DCVC = ctx.voice_client
        GDCVC.append(DCVC)
        
        text_channel_id = ctx.channel.id
        channelID.append(text_channel_id)
        
        songs: list[wavelink.Track] = await wavelink.Playable.search(search, source=wavelink.TrackSource.SoundCloud)
        if not songs:
            await ctx.send("No tracks found on SoundCloud.")
            return

        vc.queue.put(songs[0])
        queue_position = len(vc.queue)

        if not vc.playing:
            next_track = vc.queue.get()
            await vc.play(next_track)
            
            play = discord.Embed(title='Now Playing:', description=f'{songs[0].title}', color=discord.Color.purple())
      
            play.set_thumbnail(url=songs[0].artwork)
            play.add_field(name='Author', value=f'{songs[0].author}', inline=False)
    
            minutes, seconds = divmod(songs[0].length // 1000, 60)
            play.add_field(name='Length', value=f'{minutes} minutes {seconds} seconds', inline=False)
            play.set_footer(text=f'{ctx.author} requested this song')
    
    
            await ctx.send(embed=play)
        else:
            
            Qplay = discord.Embed(title='Queued', description=f'{songs[0].title}', color=discord.Color.purple())
            Qplay.set_footer(text=f'Position #{queue_position}')
            
            
            await ctx.send(embed=Qplay)


    @bot.command(name="skip")
    async def skip(ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc and vc.playing:
            await vc.stop()

    @bot.command(name="stop")
    async def stop(ctx):
        vc: wavelink.Player = ctx.voice_client
        if vc:
            await vc.stop()
            vc.queue.clear()
            await vc.disconnect()
            await ctx.send("Stopped the music and cleared the queue.")

def setup(bot):
    bot.add_command(profile)
