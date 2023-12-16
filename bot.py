import discord
from discord.ext import commands
from keep_alive import keep_alive
keep_alive()

# Define the intents to specify what events the bot will receive
intents = discord.Intents.default()
intents.messages = True  # Enable receiving message events
intents.guilds = True  # Enable accessing information about guilds
intents.message_content = True  # Enable accessing message content

# Create an instance of Bot with defined intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event to confirm the bot's login
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Command to display the bot's latency
@bot.command()
async def ping(ctx):
    latency = bot.latency * 1000  # Convert to milliseconds
    embed = discord.Embed(title="Pong! 🏓", color=discord.Color.blue())
    embed.add_field(name="Latency", value=f'{latency:.2f}ms', inline=False)
    await ctx.send(embed=embed)

# Command to simulate rolling a dice
@bot.command()
async def roll(ctx):
    embed = discord.Embed(title="Rolling Dice 🎲", description="You rolled a 6!", color=discord.Color.green())
    await ctx.send(embed=embed)

bot.run('YOUR_BOT_TOKEN')  # Replace with your bot token
