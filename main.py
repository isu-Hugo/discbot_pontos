from modules import clientImplements
from modules.log import log

client = clientImplements.load_Bot()

# === Eventos ===
@client.event
async def on_ready():
    print(f'Online como [{client.user}]')

# -----

@client.event
async def on_voice_state_update(member, before, after):
    clientImplements.voice_state(member, before, after)
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