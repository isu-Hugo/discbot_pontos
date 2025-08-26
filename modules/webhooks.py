import discord
import aiohttp
from datetime import datetime

async def send_message(data: discord.Embed):
    from modules.clientImplements import WEBHOOK_URL
    async with aiohttp.ClientSession() as sessao:
        webhook = discord.Webhook.from_url(WEBHOOK_URL, session=sessao)

        sent_message = await webhook.send(embed=data, wait=True, silent=True)

        return sent_message


async def join_message(username:str):

    hora = datetime.now().strftime('%H:%M:%S')
    embed = discord.Embed(
        title="",
        description=f":inbox_tray: **{username}** \n:clock4: `{hora}`",
        color=discord.Color.green()
    )

    return await send_message(data=embed)

async def leave_message(username:str):
    hora = datetime.now().strftime('%H:%M:%S')
    embed = discord.Embed(
        title="",
        description=f":outbox_tray: **{username}** \n:clock4: `{hora}`",
        color=discord.Color.red()
    )
    await send_message(embed)