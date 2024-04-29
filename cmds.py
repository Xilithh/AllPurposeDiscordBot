import discord
import typing
import wavelink
from discord.ext import commands

@commands.command("profile")
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    name = member.display_name
    pfp = member.display_avatar
    join = member.joined_at.strftime("%A, %B %d %Y @ %H:%M:%S")
    acc_age = member.created_at.strftime("%A, %B %d %Y @ %H:%M:%S")

    guild_icon_url = ctx.guild.icon.url if ctx.guild.icon else None  # Get the guild icon URL if available

    profile = discord.Embed(title="User Profile", description=f'{name}', color=discord.Color.blue())
    profile.set_author(name=f'{ctx.guild.name}', icon_url=guild_icon_url)
    profile.set_thumbnail(url=pfp)
    profile.add_field(name='Username', value=f'{member.mention}', inline=False)
    profile.add_field(name='Date Joined', value=join)
    profile.add_field(name='Account Created at', value=acc_age, inline=False)
    profile.add_field(name ='Role(s)', value=f"{' '.join([role.mention for role in member.roles if role.name != '@everyone'])}", inline=False)
    profile.set_footer(text=f'{ctx.author} generated this request')

    await ctx.send(embed=profile)

@commands.command("play")
async def play(ctx, search: str):
    vc = typing.cast(wavelink.Player, ctx.voice_client)
    if not vc:
        vc = await ctx.author.voice.channel.connect(cls=wavelink.Player, self_deaf=True)

    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.reply("You must be in the same voice channel as the bot.")

    song = (await wavelink.Playable.search(search, source=wavelink.TrackSource.SoundCloud))[0]

    if not song:
        return await ctx.reply("Could not find the requested track.")
    await vc.play(song)
    await ctx.reply(f"Now playing: '{song.title}' - '{song.author}'")






@commands.command("leave")
async def leave(ctx):
    vc = typing.cast(wavelink.Player, ctx.voice_client)
    if not vc:
        return await ctx.reply("Not currently in a voice channel.")
    
    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.reply("You must be in the same voice channel as the bot.")
    
    await vc.disconnect()
    return await ctx.reply("Left the voice channel.")

@commands.command("stop")
async def stop(ctx):
    vc = typing.cast(wavelink.Player, ctx.voice_client)
    if not vc:
        return await ctx.reply("Not currently in a voice channel.")
    
    if ctx.author.voice.channel.id != vc.channel.id:
        return await ctx.reply("You must be in the same voice channel as the bot.")
    
    await vc.stop()
    return await ctx.reply("Music player stopped.")

def setup(bot):
    bot.add_command(profile)
    bot.add_command(play)
    bot.add_command(leave)
    bot.add_command(stop)
