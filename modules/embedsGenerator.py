import discord
from datetime import datetime

def join(username):
    embed = discord.Embed(
        description= f":bust_in_silhouette: **{username}** \n:inbox_tray: `{current_time()}`",
        color= discord.Color.green()
    )
    return embed

def exit(username, perma):

    str_time = perma_formatter(perma)

    embed = discord.Embed(
        description= f":bust_in_silhouette: **{username}** \n:outbox_tray: `{current_time()}` :hourglass_flowing_sand: `{str_time}`",
        color= discord.Color.red()
    )
    return embed

def user_relatorio(username, perma):
    str_time = perma_formatter(perma)

    embed = discord.Embed(
        description= f"**FOLHA PONTO**\nOlá, :bust_in_silhouette: {username}\nVocê possui `{str_time}h` em calls",
        color= discord.Color.yellow()
    )
    return embed


def current_time():
    return datetime.now().strftime('%H:%M:%S')

def perma_formatter(perma) -> str:
    horas = (perma // 3600)
    minutos = (perma % 3600) // 60
    segundos = (perma % 60)

    str_time = ""
    if horas>0:
        str_time += f"{int(horas)}:"
    
    str_time += f"{int(minutos)}:{int(segundos)}"
    return str_time