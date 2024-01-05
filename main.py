# IMPORTS
import os
os.system("pip install -U pycord")
import discord
import asyncio
import time, datetime, requests
from discord.ext import tasks
import discord.ui
import json
from dotenv import load_dotenv
from keep_alive import keep_alive

intents = discord.Intents.all()
intents.members = True  # Enable members intent

bot = discord.Bot(intents=intents)

# Decorator function for rate limiting
def rate_limit(func):
    async def wrapper(ctx, *args, **kwargs):
        try:
            await func(ctx, *args, **kwargs)
        except discord.HTTPException as e:
            if e.status == 429:  # Handle rate limit (429) errors
                await ctx.respond("Oops! I'm sending too many messages. Please try again later.")
            else:
                await ctx.respond("An error occurred while executing the command.")
        await asyncio.sleep(1)  # Introduce a 1-second delay between command invocations
    return wrapper


# Apply rate limiting to all commands
for command in bot.commands:
    bot.commands[command].callback = rate_limit(bot.commands[command].callback)


special_guy_id = 1042427450249973790  # Replace with the special user's ID
opted_out_users = set()

@bot.event
async def on_ready():
    print(f"WORKING AS {bot.user}")
    activity = discord.Game(name=f"Forknite")
    status = discord.Status.online


async def set_dnd():
  await bot.wait_until_ready()
  await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Forknite"))

my_secret = os.environ['TOKEN']

@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    if owner:
        await owner.send(
            f"Hello {owner.mention}!\n\n"
            "This is customizable.`. "
            "This is customizable."
        )

@bot.event
async def on_guild_remove(guild):
    owner = guild.owner
    if owner:
        try:
            invite_link = "YOUR_INVITE_LINK_HERE"
            formatted_invite_link = f"[Invite Link]({invite_link})"
            support_link = "SUPPORT_LINK_HERE"
            formatted_support_link = f"[Bot Support]({support_link})"

            message = (
                f"Hey {owner.mention}, I've left your server '{guild.name}'. "
                f"If you want to re-invite me, use this {formatted_invite_link}. "
                f"For any assistance or questions, feel free to join our support server: {formatted_support_link}."
            )
            await owner.send(message)
        except discord.Forbidden:
            print(f"Could not send a message to {owner.display_name}. Missing permissions?")
        except Exception as e:
            print(f"Failed to send a message to {owner.display_name}: {e}")

# Existing help command
@bot.slash_command(description="Get information about available commands.")
async def help(ctx):
    commands_list = [
        ("/ping", "Returns the bot's ping"),
        ("/roll [number_of_dice]", "Rolls a dice"),
        ("/kick [member] [reason]", "Kicks a member from the server"),
        ("/clear [amount]", "Clears messages (Owner/Staff only)"),
        ("/createchannel [channel_name]", "Creates a channel (Server Owner only)"),
        ("/ban [member] [duration] [time_unit]", "Bans a user for a specified duration"),
        ("/deletechannel [channel]", "Deletes a specified channel (Owner/Staff only)"),
        ("/support", "Get bot support link"),
        ("/bot_invite", "Get bot invite link"),
        ("/avatar [user]", "Display the avatar of a user"),
        ("/userinfo [user]", "Show user information"),
        ("/mute [member] [duration] [time_unit]", "Mute a member (Admin only)"),
        ("/unmute [member]", "Unmute a member (Admin only)"),
        ("/add [num1] [num2]", "Add two numbers"),
        ("/subtract [num1] [num2]", "Subtract two numbers"),
        ("/multiply [num1] [num2]", "Multiply two numbers"),
        ("/divide [num1] [num2]", "Divide two numbers"),
    ]

    em = discord.Embed(
        title="Commands Information",
        description="Here's a list of available commands and their descriptions:",
        color=discord.Color.blue()
    )

    for command, description in commands_list:
        em.add_field(name=command, value=description, inline=False)

    em.set_author(name=ctx.author)
    em.timestamp = datetime.datetime.utcnow()
    await ctx.respond(embed=em)


# Ping Command
@bot.slash_command(description="Returns the bot's ping")
async def ping(ctx):
  before = time.monotonic()
  await ctx.respond("Fetching Ping..", delete_after=0)
  ping = (time.monotonic() - before) * 1000
  em = discord.Embed(title="PONG!🏓", description=f"My Ping is `{int(ping)} ms`")
  em.set_author(name=ctx.author)
  em.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=em)

@bot.slash_command(description="Roll dice")
async def roll(ctx, number_of_dice: int = 1):
    import random

    if number_of_dice > 0:
        rolls = [random.randint(1, 6) for _ in range(number_of_dice)]
        total = sum(rolls)

        if number_of_dice == 1:
            await ctx.respond(f"You rolled a dice and got: `{rolls[0]}`")
        else:
            await ctx.respond(f"You rolled {number_of_dice} dice and got: `{', '.join(str(roll) for roll in rolls)}`\nTotal: `{total}`")
    else:
        await ctx.respond("`❌` Please enter a valid number of dice to roll.")


# Kick Command
@bot.slash_command(description="Kicks the mentioned member from the server.")
async def kick(ctx, member: discord.Member, *, reason=None):
  authorperms = ctx.author.guild_permissions
  if authorperms.kick_members:
    if member is not ctx.author:
      if reason is None:
        await ctx.guild.kick(member, reason="Reason Not Provided.")
        embed = discord.Embed(
             title="Kicked",
             description=f"{member.mention} was kicked by {ctx.author}."
             f"\n**Reason** ```"
             f"\nReason Not Provided.```")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/946015466114146384/946015554278424586/kick.png")
        await ctx.respond(embed=embed)
        em = discord.Embed(
             title="Kicked",
             description=
             f"You have been kicked from **{ctx.guild.name}** by {ctx.author}"
             f"\n**Reason** ```\nReason Not Provided.```")
        em.set_thumbnail(url="https://media.discordapp.net/attachments/946015466114146384/946015554278424586/kick.png")
        await member.send(embed=em)
      else:
        await ctx.guild.kick(member, reason=reason)
        embed = discord.Embed(
             title="Kicked",
             description=f"{member.mention} was kicked by {ctx.author}."
             f"\n**Reason** ```"
             f"\n{reason}```")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/946015466114146384/946015554278424586/kick.png")
        await ctx.respond(embed=embed)
        em = discord.Embed(
             title="Kicked",
             description=
             f"You have been kicked from **{ctx.guild.name}** by {ctx.author}"
             f"\n**Reason** ```\n{reason}```")
        em.set_thumbnail(url="https://media.discordapp.net/attachments/946015466114146384/946015554278424586/kick.png")
        await member.send(embed=em)
    else:
      await ctx.respond("` ❌ `| {ctx.author.mention} You Can't Kick Yourself **DUMB**.")
  else:
    await ctx.respond(f"` ❌ `| {ctx.author.mention} You don't have the perms to kick members.")

@bot.slash_command(description="Clear messages (Owner/Staff only)")
async def clear(ctx, amount: int = 5):
    allowed_roles = ["Owner", "Staff"]
    member_roles = [role.name for role in ctx.author.roles]

    if any(role in allowed_roles for role in member_roles):
        if ctx.author.guild_permissions.manage_messages:
            await ctx.defer()  # Acknowledge the command

            # Perform message purging asynchronously
            async with ctx.typing():
                await asyncio.sleep(1)  # Simulating a delay (you can remove this line)
                await ctx.channel.purge(limit=amount + 1)
                await ctx.send(f"Cleared {amount} messages.", delete_after=3)
        else:
            await ctx.send("I don't have the required permissions to delete messages.")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.slash_command(description="Create a channel")
async def createchannel(ctx, channel_name: str):
    if ctx.author.id != ctx.guild.owner_id:
        await ctx.respond("Only the server owner can use this command.")
        return

    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        await ctx.respond(f"Channel `{channel_name}` already exists.")
    else:
        await guild.create_text_channel(channel_name)
        await ctx.respond(f"Channel `{channel_name}` created.")


@bot.slash_command(description="Ban a user for a specified duration")
async def ban(ctx, member: discord.Member, duration: int, time_unit: str):
    allowed_roles = ["Owner", "Staff"]  # List of roles allowed to use the command
    member_roles = [role.name for role in ctx.author.roles]

    if any(role in allowed_roles for role in member_roles):
        if duration <= 0:
            await ctx.respond("Duration should be a positive number.")
            return

        if time_unit.lower() in ['second', 'seconds']:
            duration *= 1
        elif time_unit.lower() in ['minute', 'minutes']:
            duration *= 60
        elif time_unit.lower() in ['hour', 'hours']:
            duration *= 3600
        elif time_unit.lower() in ['day', 'days']:
            duration *= 86400
        else:
            await ctx.respond("Invalid time unit. Use seconds, minutes, hours, or days.")
            return

        await ctx.guild.ban(member)
        await ctx.respond(f"{member.mention} has been banned for {duration} {time_unit}.")

        # Unban after the specified duration
        await asyncio.sleep(duration)
        await ctx.guild.unban(member)
        await ctx.respond(f"{member.mention} has been unbanned after {duration} {time_unit}.")
    else:
        await ctx.respond("You don't have permission to use this command.")


    if servers_info:
        embed = discord.Embed(title="Servers Information", description=servers_info, color=discord.Color.blue())
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("I am not in any servers!")

@bot.slash_command(description="Delete a specified channel")
async def deletechannel(ctx, channel: discord.TextChannel):
    allowed_roles = ["Owner", "Staff"]  # List of roles allowed to use the command
    member_roles = [role.name for role in ctx.author.roles]

    if any(role in allowed_roles for role in member_roles):
        await channel.delete()
        await ctx.respond(f"Channel '{channel.name}' has been deleted.")
    else:
        await ctx.respond("You don't have permission to use this command.")


@bot.slash_command(description="Get bot support link")
async def support(ctx):
    support_link = "SUPPORT_LINK_HERE"
    await ctx.respond(f"Here's the bot support: {support_link}")





@bot.slash_command(description="Get bot invite link")
async def bot_invite(ctx):
    invite_link = "INVITE LINK HERE"

    try:
        await ctx.author.send(f"Here's the bot invite: [BOT LINK]({invite_link})")
        await ctx.respond("Sent you the bot invite link via DM!")
    except discord.HTTPException as e:
        if e.status == 429:  # Handle rate limit (429) errors
            await ctx.respond("Oops! I'm sending too many messages. Please try again later.")
        else:
            await ctx.respond("An error occurred while sending the invite link.")

@bot.slash_command(description="Display the avatar of a user")
async def avatar(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    requester_avatar_url = ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    embed = discord.Embed(title=f"Avatar of {user.name}")
    embed.set_image(url=avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=requester_avatar_url)

    await ctx.respond(embed=embed)



@bot.slash_command(description="Show user information")
async def userinfo(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    embed = discord.Embed(title="User Information", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
    embed.add_field(name="User ID", value=user.id, inline=False)
    embed.add_field(name="Account Created", value=user.created_at.strftime("%A, %B %d, %Y"), inline=False)
    if isinstance(user, discord.Member):
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%A, %B %d, %Y"), inline=False)
        embed.add_field(name="Top Role", value=user.top_role.name, inline=False)

    await ctx.respond(embed=embed)

@bot.slash_command(description="Mute a member")
async def mute(ctx, member: discord.Member, duration: int, time_unit: str):
    if ctx.author.guild_permissions.administrator:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            # If the 'Muted' role doesn't exist, create it
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role)

        await ctx.respond(f"{member.display_name} has been muted for {duration} {time_unit}.")
    else:
        await ctx.respond("You don't have permission to use this command.")

@bot.slash_command(description="Unmute a member")
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.respond(f"{member.display_name} has been unmuted.")
        else:
            await ctx.respond(f"{member.display_name} is not muted.")
    else:
        await ctx.respond("You don't have permission to use this command.")

@bot.slash_command(description="Add two numbers")
async def add(ctx, num1: float, num2: float):
    result = num1 + num2
    await ctx.respond(f"Result: {result}")

@bot.slash_command(description="Subtract two numbers")
async def subtract(ctx, num1: float, num2: float):
    result = num1 - num2
    await ctx.respond(f"Result: {result}")

@bot.slash_command(description="Multiply two numbers")
async def multiply(ctx, num1: float, num2: float):
    result = num1 * num2
    await ctx.respond(f"Result: {result}")

@bot.slash_command(description="Divide two numbers")
async def divide(ctx, num1: float, num2: float):
    if num2 == 0:
        await ctx.respond("Cannot divide by zero!")
    else:
        result = num1 / num2
        await ctx.respond(f"Result: {result}")

bot.loop.create_task(set_dnd())
keep_alive()
bot.run(my_secret) # Runs the bot
