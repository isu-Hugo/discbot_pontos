import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from modules import db


# Carregamento de variaveis de ambiente
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CANAL_PONTOS_ID = int(os.getenv("CANAL_PONTOS_ID"))
BOT_PREFIXO = os.getenv("BOT_PREFIXO")


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
    await ctx.send(f"""Olá {ctx.author}
                    digo {ctx.author.display_name}
                    você disse em {ctx.channel}do servidor {ctx.guild}
                    "{ctx.message.content}"
                    com o id {ctx.author.id}""")
    
# -----

async def relatorio(ctx):
    await ctx.send(f"não existe isso ai ainda não {ctx.author.display_name}")

# ------------------------------------------------------

# Funções auxiliares
async def voice_update(user_id:int, acao:bool, message_id=None, client=None):
    if acao is True:
        print(f"o usuario com o id {user_id} se conectou")
        db.user_connected(id_user=user_id, id_message=message_id)
        
    elif acao is False:
        print(f"o usuario com o id {user_id} se desconectou")
        await db.user_desconected(id_user=user_id, client=client)