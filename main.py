from modules import clientImplements
from modules.log import log

client = clientImplements.load_Bot()
CONECTADO = True
DESCONECTADO = False

# === Eventos ===
@client.event
async def on_ready():
    print(f'Online como [{client.user}]')

# -----

@client.event
async def on_voice_state_update(member, before, after):

    if before.channel is None and after.channel is not None:
    
        channel = client.get_channel(clientImplements.CANAL_PONTOS_ID)
        # print(channel.id)
        msg = await channel.send("Entrou", silent=True)
        await clientImplements.voice_update(user_id=member.id, acao=CONECTADO, message_id=msg.id)

    elif before.channel is not None and after.channel is None:
        await clientImplements.voice_update(user_id=member.id, acao=DESCONECTADO, client=client)
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