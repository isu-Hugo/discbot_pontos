import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from modules import db
from modules.log import log
from modules import embedsGenerator


# Carregamento de variaveis de ambiente
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_PONTOS_ID = int(os.getenv("CANAL_PONTOS_ID"))
BOT_PREFIXO = os.getenv("BOT_PREFIXO")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


# -----

# Cria o objeto bot
def load_Bot():
    """Cria o objeto que representa o bot que se conecta ao discord, não são necessarios parametros."""

    db.load()

    intents = discord.Intents.default()
    intents.voice_states = True
    intents.message_content = True
    return commands.Bot(intents=intents, command_prefix=BOT_PREFIXO)
# ------------------------------------------------------


# Implementação dos eventos e comandos
def voice_state(member, before, after):
    if before.channel is None and after.channel is not None:
        voice_update(user_id=member.id, acao=True)
    elif before.channel is not None and after.channel is None:
        voice_update(user_id=member.id, acao=False)


# -----

async def oi(ctx):
    # await ctx.send(f"""Olá {ctx.author}
    #                 digo {ctx.author.display_name}
    #                 você disse em {ctx.channel}do servidor {ctx.guild}
    #                 "{ctx.message.content}"
    #                 com o id {ctx.author.id}""")
    embed = discord.Embed(
        description=f"vai dar oi na cadeia {ctx.author}:thumbsup:",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)
    
# -----

def relatorio_duracao_builder(member_id, member_name):
    tempo =  db.user_relatorio_permanencia(member_id)
    embed = embedsGenerator.user_relatorio(member_name, tempo)
    return embed

async def relatorio_rank_builder(client):
    data = db.relatorio_rank()
    newData = []
    for i in data:
        name = await getNameById(client, i.get('id_user'))
        newData.append({
            "name": name,
            "perma": i.get('perma')
        })

    return embedsGenerator.rank(newData)


    

# ------------------------------------------------------

# Funções auxiliares
async def voice_update(user_id:int, acao:bool, message_id=None, client=None):
    if acao is True:
        print(f"o usuario com o id {user_id} se conectou")
        db.user_connected(id_user=user_id, id_message=message_id)
        
    elif acao is False:
        print(f"o usuario com o id {user_id} se desconectou")
        return await db.user_desconected(id_user=user_id, client=client)

async def delete_message(client, msg_id):
    try:
        channel = client.get_channel(CANAL_PONTOS_ID)
        delete_message = await channel.fetch_message(msg_id)
        await delete_message.delete()
    except Exception as er:
        log(f"Erro ao apagar mesagem id={msg_id}, erro={er}")

async def getNameById(client, id):
    user = client.get_user(id)
    if user is None:
        user = await client.fetch_user(id)
    return user.name
