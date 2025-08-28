import discord
from datetime import datetime

def join(username):
    embed = discord.Embed(
        description= f":inbox_tray: **{username}** \n:clock4: `{current_time()}`",
        color= discord.Color.green()
    )
    return embed

def exit(username):
    embed = discord.Embed(
        description= f":outbox_tray: **{username}** \n:clock4: `{current_time()}`",
        color= discord.Color.red()
    )
    return embed

def current_time():
    return datetime.now().strftime('%H:%M:%S')