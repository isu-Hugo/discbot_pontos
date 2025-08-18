import discord
import os
from dotenv import load_dotenv

# Carrega as variaveis de ambiente
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_PONTOS_ID = os.getenv("CANAL_PONTOS_ID")

# Cria as configuracoes padrão 
intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
client = discord.Client(intents=intents)


# Adiciona um evento ao bot
@client.event
async def on_ready():
    print(f'Bot conectado [{client.user}]')

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        print(f'{member} conectado id={member.id}')
    elif before.channel is not None and after.channel is None:
        print(f'{member} desconectado id={member.id}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print(message.content)
    canal = client.get_channel(CANAL_PONTOS_ID)
    await canal.send("bateu")
    # if message.content.startswith('&s'):
    #     await message.channel.send('mensagem em modo silent !', silent=True)

# Executa o bot
client.run(BOT_TOKEN)