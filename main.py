import discord
from discord import app_commands
from discord.ext import commands
import wavelink
from config import TOKEN
from cmds import setup
from cmds import setup_commands
from cmds import channelID
from cmds import GDCVC


bot = commands.Bot(command_prefix="$", intents = discord.Intents.all())


setup(bot)

async def connect_nodes():
    await bot.wait_until_ready()

    nodes = [
        wavelink.Node(
            identifier="Node1",
            uri="http://0.0.0.0:2333",
            password="youshallnotpass"
        )
    ]

    await wavelink.Pool.connect(nodes=nodes, client=bot)


@bot.event
async def on_ready():
    await connect_nodes()
    print("Bot is Online")
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)


@bot.event
async def on_wavelink_node_ready(payload: wavelink.NodeReadyEventPayload):
    print(f"Node with ID {payload.session_id} has connected")
    print(f"Resumed session: {payload.resumed}")


@bot.tree.command(name='hello', description='Slash command attempt')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey {interaction.user.mention}! Slash commands')

@bot.tree.command(name='say', description='(username) said (insert text)')
@app_commands.describe(thing_to_say = 'What should i say?')
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(f'{interaction.user.name} said: `{thing_to_say}`')



@bot.event
async def on_wavelink_track_end(payload):
    channel = bot.get_channel(channelID[0])
    player = payload.player  # Accessing the player from the payload
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)
        # Ensuring the text_channel_id is stored somewhere or managed differently # Ensure this ID is correctly assigned
        if channel:
            Cplay = discord.Embed(title='Now Playing:', description=f'{next_track.title}', color=discord.Color.purple())
      
            Cplay.set_thumbnail(url=next_track.artwork)
            Cplay.add_field(name='Author', value=f'{next_track.author}', inline=False)
    
            minutes, seconds = divmod(next_track.length // 1000, 60)
            Cplay.add_field(name='Length', value=f'{minutes} minutes {seconds} seconds', inline=False)
            
            await channel.send(embed=Cplay)
        else:
            print("Channel not found for sending messages.")
    else:
        await channel.send("Queue is empty, no more tracks to play. Diconnecting.")
        await GDCVC[0].disconnect()
setup_commands(bot)




bot.run(TOKEN)
