import os
import sys
import random
import sqlite3

sys.path.insert(0,"C:/Users/kaixtr/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0/LocalCache/local-packages/Python310/site-packages")
import discord
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
PERMISSIONS = os.getenv('DISCORD_PERMISSIONS')

bot = commands.Bot(command_prefix='',case_insensitive=True)

@bot.event
async def on_ready():
	for guild in bot.guilds:
		if guild.name == GUILD:
			break
	print(
		f'{bot.user} está conectado no seguinte servidor:\n'
		f'{guild.name} (id: {guild.id})'
	)

@bot.event
async def on_disconnect():
	print(
		f'{bot.user} foi desconectado.'
	)

#FALAR
@bot.command(name='falef')
async def falar(ctx,*args):
	if args: resposta = ' '.join(args)
	else: resposta = random.choice(('Concordo.','Ah, nada ver isso daí!','Pode ser que sim, pode ser que não.','Pokas idéias, truta'))
	await ctx.send(resposta,tts=True)

#CALCULAR
@bot.command(name='calc')
async def falar(ctx,*args):
	if args:
		resposta = ' '.join(args)
		valor = resposta.replace('x','*')
		valor = valor.replace('^','**')
		resposta = '_' + resposta + ' = ' + str(eval(valor)) + '_'
	else: resposta = '...calcular o quê?'
	await ctx.send(resposta)

#DADOS
@bot.command(name='rolar')
async def rolada(ctx,*args):
	if len(args) == 0:
		await ctx.send("Pra rolar um dado, escreva nesses formatos: _4,d8,1d6,2d20+2 etc._")
		await ctx.send("Ah! E você também pode rolar o dado de dano de uma arma se escrever o nome dela!")
	else:
		dado = ''
		bonus = 0
		if len(args) == 2: bonus = int(args[1])
		if args[0][0] in 'd0123456789': dado = args[0]
		else:
			tbl = sqlite3.connect('data.db')
			com = tbl.cursor()

			com.execute(f"SELECT * FROM items WHERE nome='{args[0]}' ORDER BY nome")
			res = com.fetchall()
			if res:
				palavra = ''
				find = None
				for i in res[0][3]:
					if palavra.lower() == 'dano:': find = True
					if i in ('|',',','.'): find = None; palavra = ''

					if find and i != ' ': dado += i
					else: palavra += i
			tbl.commit()
			com.close()
			tbl.close()

		if len(dado) > 1 and dado[1] == 'd':
			vezes = int(dado[0])
			dado = int(dado[2])
		else:
			vezes = 1
			dado = int(dado.replace('d',''))

		resultado = 0
		for i in range(vezes): resultado += random.randint(1,dado)
		resultado += int(bonus)

		if resultado >= (dado * vezes): comentario = 'em cheio!'
		elif resultado <= 1: comentario = 'que azar!'
		elif resultado > int((dado * vezes)/2): comentario = 'boa!'
		elif resultado == int((dado * vezes)/2): comentario = 'nada mal.'
		elif resultado < int((dado * vezes)/2): comentario = 'eita...'

		if int(bonus) < 0: dd = 'd' + str(dado) + str(bonus)
		elif int(bonus) > 0: dd = 'd' + str(dado) + '+' + str(bonus)
		else: dd = 'd' + str(dado)
		if vezes > 1: dd = str(vezes) + dd
		await ctx.send('**' + dd + ' = **' + str(resultado) + ', ' + comentario)

#############################################

#ABRAÇO
@bot.command(name='abraço')
async def falar(ctx,):
	await ctx.send("Abraço, galera")

#GAY
@bot.command(name='gay')
async def falar(ctx,):
	await ctx.send("Gay? Quem?")

#############################################

#LEMBRAR
@bot.command(name='lembref')
async def lembrar(ctx,*args):
	if len(args) == 0: await ctx.send("Para me fazer me lembrar de alguma coisa, dê um nome ao lembrete e depois escreva qualquer mensagem!")
	elif len(args) == 1: await ctx.send("Você deu um marcador ao lembrete, mas não me disse do que eu devo me lembrar!")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		com.execute("CREATE TABLE IF NOT EXISTS lembretes (id text,mensagem text)")
		com.execute(f"DELETE FROM lembretes WHERE id='{args[0]}'")
		com.execute(f"INSERT INTO lembretes VALUES ('{args[0]}','{' '.join(args[1:])}')")

		tbl.commit()
		com.close()
		tbl.close()
		await ctx.send(random.choice(('Pode contar comigo!','Não vou me esquecer!','Pode deixar!')))

#ESQUECER
@bot.command(name='esquecaf')
async def esquecer(ctx,*args):
	if len(args) == 0: await ctx.send("Se quiser que eu me esqueça de um lembrete, escreva o marcador que deu para ele.")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		com.execute(f"DELETE FROM lembretes WHERE id='{args[0]}'")
		await ctx.send(random.choice(('Hã? Esquecer o quê?','Me esqueci de alguma coisa?')))

		tbl.commit()
		com.close()
		tbl.close()

#MOSTRAR LEMBRETES
@bot.command(name='lembretes')
async def lembretes(ctx):
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()

	com.execute("SELECT * FROM lembretes ORDER BY id")
	res = com.fetchall()
	if res:
		await ctx.send("**Estes são os seus lembretes:**")
		for i in res: await ctx.send(i[0] + ': ' + i[1])
	else: await ctx.send(random.choice(("Você não me pediu para me lembrar de nada.","Que lembretes?","Você não tem lembretes.")))

	tbl.commit()
	com.close()
	tbl.close()

#############################################

#ADICIONAR Á TABELA
@bot.command(name='adicionarf')
async def adicionar(ctx,*args):
	if len(args) == 0:
		await ctx.send("Não sabe adicionar um item?")
		await ctx.send("Se liga: é só escrever em qual tabela quer adicionar, o nome do item, o preço e as outras coisinhas")
		await ctx.send("Tipo o dano da arma, o bônus de CA, sei lá... mas só se quiser, pode deixar vazio.")
	elif len(args) == 1: await ctx.send("Você escreveu a tabela onde vai colocar, mas ainda falta o nome, o preço e o resto.")
	elif len(args) == 2: await ctx.send("Você escreveu a tabela e o nome do item, mas falta o preço. O resto é opcional.")
	elif len(args) >= 3:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()
		txt = ''
		if len(args) > 3: txt = ' '.join(args[3:])

		com.execute("CREATE TABLE IF NOT EXISTS items (tabela text,nome text,preco text,propriedades text)")
		com.execute(f"DELETE FROM items WHERE tabela='{args[0]}' AND nome='{args[1]}'")
		com.execute(f"INSERT INTO items VALUES ('{args[0]}','{args[1]}','{args[2]}','{txt}')")

		tbl.commit()
		com.close()
		tbl.close()
		await ctx.send(f"**{args[1]}** foi adicionado na tabela **{args[0]}**!")

#RENOMEAR TABELAS
@bot.command(name='renomearf')
async def renomear(ctx,*args):
	if len(args) == 0: await ctx.send(f"Quer renomear uma tabela ou um item?")
	elif len(args) == 1: await ctx.send(f"Digite um nome antigo e depois o nome novo")
	elif len(args) == 2: await ctx.send(f"Digite um nome antigo e depois o nome novo")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		if args[0].lower() == 'tabela': com.execute(f"UPDATE items SET tabela='{args[2]}' WHERE tabela='{args[1]}'")
		if args[0].lower() == 'item': com.execute(f"UPDATE items SET nome='{args[2]}' WHERE nome='{args[1]}'")
		await ctx.send("Já mudei o nome!")

		tbl.commit()
		com.close()
		tbl.close()

#APAGAR DA TABELA
@bot.command(name='apagarf')
async def apagar(ctx,*args):
	if len(args) == 0:
		await ctx.send(f"Se quiser tirar uma tabela, digite só o nome dela.")
		await ctx.send(f"Mas se quiser tirar apenas um item dela, escreva a tabela e depois o nome do item.")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		if len(args) == 2: com.execute(f"DELETE FROM items WHERE tabela='{args[0]}' AND nome='{args[1]}'")
		else: com.execute(f"DELETE FROM items WHERE tabela='{args[0]}'")
		await ctx.send("Sumiu para sempre, papai!")

		tbl.commit()
		com.close()
		tbl.close()

#MOSTRAR TABELAS
@bot.command(name='mostrarf')
async def mostrar(ctx,*args):
	if len(args) == 0: await ctx.send(f"Você quer que eu mostre qual tabela ou item?")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		if len(args) == 2: com.execute(f"SELECT * FROM items WHERE nome='{args[1]}' ORDER BY nome")
		else: com.execute(f"SELECT * FROM items WHERE tabela='{args[0]}' ORDER BY nome")
		res = com.fetchall()
		if res:
			await ctx.send(f"**{args[0]}**")
			txt = ''
			for i in res: txt += f"**{i[1]}:** {i[2]}$ | _{i[3]}_\n"
			await ctx.send(txt)
		else: await ctx.send("Eu não consegui encontrar nada...")

		tbl.commit()
		com.close()
		tbl.close()

#############################################

ATRIBUTOS = {
	'JOGADOR': 'jogador','PERSONAGEM': 'personagem','CLASSE': 'classe','RACA': 'raca','NIVEL': 'nivel',
	'CA': 'armadura','PV': 'vida','MANA': 'mana','ADRENALINA': 'adrenalina','SANIDADE': 'sanidade','IDADE': 'idade',
	'CONDICAO': 'condicao','MORTE': 'morte','BENCAO': 'bencao','DESTINO': 'destino','OURO': 'ouro','DIA': 'ourodiario','APARENCIA': 'aparencia',
	'HISTORIA': 'historia','ANOTACOES': 'anotacoes',

	'COMBATE': 'combate','AGIL': 'combateagil','DISPARO': 'disparo','VENEFICES': 'venefices',
	'FORCA': 'forca','DESTREZA': 'destreza','CONSTITUICAO': 'constituicao','INTELIGENCIA': 'inteligencia','SABEDORIA': 'sabedoria','CARISMA': 'carisma','SORTE': 'sorte',
	'ATLETISMO': 'atletismo','VONTADE': 'vontade','FORJA': 'forja','MINERACAO': 'mineracao',
	'CAVALGAR': 'cavalgar','ACROBACIA': 'acrobacia','FURTIVIDADE': 'furtividade','FURTO': 'furto','REFLEXOS': 'reflexos','COLETA': 'coleta','COZINHA': 'cozinha','ARTESANATO': 'artesanato',
	'FORTITUDE': 'fortitude','IMUNIDADE': 'imunidade',
	'HISTORIA': 'historia','INVESTIGACAO': 'investigacao','MEDICINA': 'medicina','PERCEPCAO': 'percepcao','SOBREVIVENCIA': 'sobrevivencia','JOGATINA': 'jogatina','FABRICACAO': 'fabricacao','MECANICA': 'mecanica',
	'NATUREZA': 'natureza','RELIGIAO': 'religiao','ANIMAIS': 'animais','OCULTISMO': 'ocultismo','ARCANISMO': 'arcanismo','INTUICAO': 'intuicao','ENCANTAMENTO': 'encantamento','ALQUIMIA': 'alquimia',
	'PERSUASAO': 'persuasao','INTIMIDACAO': 'intimidacao','BLEFAR': 'blefar','ATUACAO': 'atuacao','RUAS': 'ruas','LIDERANCA': 'lideranca','TREINAMENTO': 'treinamento','NOBREZA': 'nobreza',
	'LOOT': 'loot','VIAGEM': 'viagem','DESCANSO': 'descanso',
}

def stripacc(text):
	new = ''
	for i in text.lower():
		if i in 'äåæªáãàâ': new += 'a'
		elif i in 'ëėēèéêę': new += 'e'
		elif i in 'ćçč': new += 'c'
		elif i in 'íìîįïī': new += 'i'
		elif i in 'ñń': new += 'n'
		elif i in 'ºōœøöòôóõ': new += 'o'
		elif i in 'ūùúüû': new += 'u'
		else: new += i
	return new

#ADICIONAR FICHA DE PERSONAGEM
@bot.command(name='fichaf')
async def ficha(ctx,cmd,name,*args):
	#ADICIONAR FICHA
	if cmd == 'add':
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()
		txt = ' '.join(args)

		#CRIAR TABELAS
		add = ''
		ins = ''
		for i in ATRIBUTOS.items(): add += i[1] + ' text,'; ins += "'',"
		com.execute(f"CREATE TABLE IF NOT EXISTS ficha (id text,{add[:-1]})")
		com.execute(f"INSERT INTO ficha VALUES ({name},{ins[:-1]})")

		com.execute("CREATE TABLE IF NOT EXISTS inventario (id text,nome text,quantidade text,preco text,peso text)")
		com.execute("CREATE TABLE IF NOT EXISTS magias (id text,nome text,dano text,mana text)")

		#ADICIONAR FICHA
		palavra = ''
		valor = ''
		find = None
		dd = {}
		for caractere in range(len(txt)):
			if txt[caractere] not in (':','•','\n','(','-'):
				if find == None and txt[caractere] != ' ': palavra += txt[caractere]
				else: valor += txt[caractere]
			
			if palavra not in dd and stripacc(palavra).upper() in ATRIBUTOS:
				find = ATRIBUTOS[stripacc(palavra).upper()]

			if txt[caractere] in ('\n','•','(','-'):
				if find and palavra not in dd:
					com.execute(f"UPDATE ficha SET {ATRIBUTOS[stripacc(palavra).upper()]}='{valor}' WHERE id={name}")
					dd[palavra] = valor
					valor = ''
					find = None
				palavra = ''

		tbl.commit()
		com.close()
		tbl.close()
		await ctx.send(f"Salvei a ficha do personagem **{name}** aqui comigo! ;)")

	#MOSTRAR FICHA
	if cmd == 'show':
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()
		resposta = ''

		com.execute(f"SELECT * FROM ficha WHERE id={name}")
		res = com.fetchall()
		for i in res: resposta += 'i' + '\n'

		tbl.commit()
		com.close()
		tbl.close()
		await ctx.send(resposta)

#############################################

youtube_dl.utils.bug_reports_message = lambda: ''
options = {
	'format': 'bestaudio/best',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes 
}
ffmpeg_options = {
	'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(options)
class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = ""
	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
		filename = data['title'] if stream else ytdl.prepare_filename(data)
		return filename

#TOCAR MÚSICA
@bot.command(name='radio', help='To play song')
async def radio(ctx,*args):
	voice_client = ctx.message.guild.voice_client
	if args[0] == 'entrar':
		if not ctx.message.author.voice:
			await ctx.send("{}, entre num chat de voz primeiro!".format(ctx.message.author.name))
		elif voice_client and voice_client.is_connected(): await ctx.send("Eu já tô aqui, truta!")
		else: await ctx.message.author.voice.channel.connect()

	elif args[0] == 'sair':
		if voice_client and voice_client.is_connected(): await voice_client.disconnect()
		else: await ctx.send("Oxe, eu já saí!")
	
	elif args[0] == 'play':
		if ctx.message.author.voice:
			await ctx.message.author.voice.channel.connect()
			voice_client = ctx.message.guild.voice_client
		if voice_client and voice_client.is_connected():
			async with ctx.typing():
				filename = await YTDLSource.from_url(args[1], loop=bot.loop)
				voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
			await ctx.send('**DJ Frederico lançou a braba:** {}'.format(filename))
		else: await ctx.send("Eu não estou em nenhum chat de voz.")
	
	elif args[0] == 'pause':
		if voice_client and voice_client.is_connected() and voice_client.is_playing(): await voice_client.pause()
		else: await ctx.send("Eu não estou tocando nada, cara!")
	elif args[0] == 'resume':
		if voice_client and voice_client.is_connected() and voice_client.is_paused(): await voice_client.resume()
		else: await ctx.send("Eu não estou tocando nada, cara!")
	elif args[0] == 'pare':
		if voice_client and voice_client.is_connected() and voice_client.is_playing(): await voice_client.stop()
		else: await ctx.send("Eu não estou tocando nada, cara!")

#SONOPLASTIA
@bot.command(name='sfx')
async def sfx(ctx,audio):
	await ctx.message.author.voice.channel.connect()
	voice_client = ctx.message.guild.voice_client
	if voice_client:
		filename = "C:\\Users\\kaixtr\\Music\\Defeitos Sonoros\\" + audio.lower() + ".mp3"
		voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
	else: await ctx.send("Entre em um chat de voz aí!")

#############################################

#HELP
@bot.command(name='ajudaf')
async def ajuda(ctx,*args):
	await ctx.send("O que eu sei fazer? Sei fazer um monte de coisas, bebê!\n\
**falef:** vou dizer qualquer coisa que digitar.\n\
**calc:** vou calcular qualquer conta matemática que digitar.\n\
**rolar:** vou rolar dados por você.\n\
**lembref:** se precisar lembrar de algo, vou lembrar pra você.\n\
**esquecaf:** se quiser que eu esqueça, eu faço também.\n\
**lembretes:** mostro todos os lembretes pra você.\n\
**adicionarf:** crio uma tabela com itens e adiciono ele.\n\
**renomearf:** troco o nome de uma tabela ou item.\n\
**apagarf:** apago qualquer tabela ou item.\n\
**mostrarf:** mostro uma tabela.\n\
**fichaf:** mostro fichas de personagem salvas por você.\n\
**radio:** toco músicas para animar a garotada.\n\
**sfx:** por último, mas não menos importante, também sou sonoplasta do ratinho.\n")

if __name__ == "__main__": bot.run(TOKEN)