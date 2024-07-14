from discord.ext import commands
from dotenv import load_dotenv
import os

import intents
import geral
import lembrar
import tabela
import audio
import rpg

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PERMISSIONS = os.getenv('DISCORD_PERMISSIONS')

bot = commands.Bot(command_prefix='',case_insensitive=True,intents=intents.itts)

@bot.event
async def on_ready():
	guild = None
	for guild in bot.guilds:
		if guild.name == GUILD: break
	if guild:
		print(f'{bot.user} está conectado no servidor {guild.name} (id: {guild.id})')
	else:
		print(f"{bot.user} não encontrou nenhum servidor para participar. =(\nCtrl+C para finalizar.")

@bot.event
async def on_disconnect(): print(f'{bot.user} foi desconectado.')

#############################################

@bot.command(name='falef', help='Repete uma mensagem em voz alta')
async def falef(ctx,*args): await geral.falef(ctx,*args)

@bot.command(name='calc', help='Resolve um problema matemático')
async def calc(ctx,*args): await geral.calc(ctx,*args)

@bot.command(name='rolar', aliases=['dicef'], help='Rola dados de testes e itens')
async def rolar(ctx,*args): await geral.rolar(ctx,*args)

@bot.command(name='setf', aliases=['configf'], help='Configura o Frederico')
async def setf(ctx,*args): await geral.setf(ctx,*args)

@bot.command(name='ajudaf', aliases=['helpf'], help='Mostra todos os comandos')
async def ajuda(ctx,*args): await geral.ajuda(ctx,*args)

#############################################

@bot.command(name='frederico', aliases=['fred'], help='Responde á um chamado')
async def frederico(ctx): await geral.frederico(ctx)

@bot.command(name='salve', help='Manda um salve')
async def salve(ctx): await geral.salve(ctx)

@bot.command(name='abraço', aliases=['abraco'], help='Manda um abraço')
async def abraco(ctx): await geral.abraco(ctx)

@bot.command(name='gay', help='gay')
async def gay(ctx): await geral.gay(ctx)

@bot.command(name='limpaf', help='Apaga todas as mensagens enviadas pelo Frederico')
async def limpaf(ctx): await geral.limpaf(ctx)

#############################################

@bot.command(name='lembref', help='Cria um lembrete')
async def lembref(ctx,*args): await lembrar.lembre(ctx,*args)

@bot.command(name='esquecaf', help='Apaga um lembrete')
async def esquecaf(ctx,*args): await lembrar.esqueca(ctx,*args)

@bot.command(name='lembretes', help='Mostra todos os lembretes')
async def lembretes(ctx,*args): await lembrar.lembretes(ctx,*args)

#############################################

@bot.command(name='adicionarf', aliases=['addf'], help='Cria uma tabela ou adiciona um item')
async def adicionarf(ctx,*args): await tabela.adicionar(ctx,*args)

@bot.command(name='renomearf', aliases=['renamef'], help='Renomeia uma tabela ou item')
async def renomearf(ctx,*args): await tabela.renomear(ctx,*args)

@bot.command(name='apagarf', aliases=['delf'], help='Apaga uma tabela ou item')
async def apagarf(ctx,*args): await tabela.apagar(ctx,*args)

@bot.command(name='tabelaf', aliases=['tablef'], help='Mostra tabelas criadas')
async def tabelaf(ctx,*args): await tabela.mostrar(ctx,*args)

#############################################

@bot.command(name='enigmaf', help='Cria um enigma para ser resolvido')
async def enigmaf(ctx,*args): await rpg.enigma(ctx,*args)

@bot.command(name='fichaf', help='Gerencia informações e testes do personagem')
async def fichaf(ctx,*args): await rpg.ficha(ctx,*args)

@bot.command(name='inventariof', aliases=['invf'], help='Gerencia o inventário do personagem')
async def inventariof(ctx,*args): await rpg.inventario(ctx,*args)

@bot.command(name='magiasf', aliases=['magf','habilidadesf','habf'], help='Gerencia as habilidades, características e magias do personagem')
async def magiasf(ctx,*args): await rpg.magias(ctx,*args)

#############################################

@bot.command(name='radio', help='Toca uma música')
async def radio(ctx,*args): await audio.radio(ctx,*args)

@bot.command(name='sfx', help='Toca um efeito sonoro')
async def sfx(ctx,*args): await audio.sfx(ctx,*args)

#############################################

if __name__ == "__main__":
	bot.run(TOKEN)