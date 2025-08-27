from modules import clientImplements
from modules.log import log
from modules.webhooks import join_message, leave_message
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

        if before.channel is None and after.channel is not None:
            msg = await join_message(member)
            await clientImplements.voice_update(user_id=member.id, acao=CONECTADO, message_id=msg.id)

        elif before.channel is not None and after.channel is None:
            ponto_valido = await clientImplements.voice_update(user_id=member.id, acao=DESCONECTADO, client=client)
            if ponto_valido:
                await leave_message(member)
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