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
    lock = locks.setdefault(member.id, asyncio.Lock())

    async with lock:
        canal_pontos = await client.fetch_channel(clientImplements.CANAL_PONTOS_ID)
        if before.channel is None and after.channel is not None:
            # 
            msg = await canal_pontos.send(embed=embedsGenerator.join(member), silent=True)
            user_connected(id_user=member.id, id_message=msg.id)
            # 
        elif before.channel is not None and after.channel is None:
            # 
            delete_message_id = user_desconected(id_user=member.id)
            if delete_message_id is None:
                await canal_pontos.send(embed=embedsGenerator.exit(member), silent=True)
            else:
                try:
                    channel = client.get_channel(clientImplements.CANAL_PONTOS_ID)
                    delete_message = await channel.fetch_message(delete_message_id)
                    await delete_message.delete()
                except Exception as er:
                    log(f"Erro ao apagar mesagem id={delete_message_id}, erro={er}")
# ------------------------------------------------------





# === Comandos ===
@client.command()
async def oi(ctx):
    await clientImplements.oi(ctx)

# -----

@client.command()
async def relatorio(ctx):
    await clientImplements.relatorio(ctx)





# ------------------------------------------------------




# Executa o bot
client.run(clientImplements.BOT_TOKEN)