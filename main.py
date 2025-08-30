from modules import clientImplements
from modules.log import log
from modules import embedsGenerator
from modules.db import user_connected, user_desconected
import discord
import asyncio

client = clientImplements.load_Bot()
CONECTADO = True
DESCONECTADO = False
locks = {}
# === Eventos ===
@client.event
async def on_ready():
    print(f'Online como [{client.user}]')

# -----

@client.event
async def on_voice_state_update(member, before, after):
    if member.bot:
        print(f"bot desconsiderado: {member}")
        return
    lock = locks.setdefault(member.id, asyncio.Lock())

    async with lock:
        canal_pontos = await client.fetch_channel(clientImplements.CANAL_PONTOS_ID)


        if before.channel is None and after.channel is not None:
            msg = await canal_pontos.send(embed=embedsGenerator.join(member), silent=True)
            response = user_connected(id_user=member.id, id_message=msg.id)
            if response["valido"] is False:
                await clientImplements.delete_message(client, response["id_msg"])

        elif before.channel is not None and after.channel is None:
            response = user_desconected(id_user=member.id)
            if response["valido"] is True:
                await canal_pontos.send(embed=embedsGenerator.exit(member, response["duracao"]), silent=True)
            else:
                await clientImplements.delete_message(client=client, msg_id=response["id_msg"])
# ------------------------------------------------------





# === Comandos ===
@client.command()
async def oi(ctx):
    await clientImplements.oi(ctx)

# -----

@client.command()
async def relatorio(ctx):

    embed = clientImplements.relatorio_duracao_builder(member_id=ctx.author.id, member_name=ctx.author)
    await ctx.send(embed=embed, silent=True)
    
    # await ctx.send(ctx.author.id)

@client.command()
async def rank(ctx):
    embed = await clientImplements.relatorio_rank_builder(client)
    await ctx.send(embed=embed, silent=True)
    
    


# ------------------------------------------------------




# Executa o bot
client.run(clientImplements.BOT_TOKEN)