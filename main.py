import discord
from discord import app_commands
from discord.ext import commands
import wavelink
import typing
from config import TOKEN
from cmds import setup

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


bot.run(TOKEN)
