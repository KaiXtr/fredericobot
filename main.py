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
FSELECT = {}
DPADRAO = 'd20'

bot = commands.Bot(command_prefix='',case_insensitive=True)

@bot.event
async def on_ready():
	for guild in bot.guilds:
		if guild.name == GUILD: break
	print(f'{bot.user} está conectado no seguinte servidor:\n{guild.name} (id: {guild.id})')

@bot.event
async def on_disconnect(): print(f'{bot.user} foi desconectado.')

#############################################

#FALAR
@bot.command(name='falef', help='Repete uma mensagem em voz alta')
async def falef(ctx,*args):
	if args: resposta = ' '.join(args)
	else: resposta = random.choice(('Concordo.','Ah, nada ver isso daí!','Pode ser que sim, pode ser que não.','Pokas idéias, truta'))
	await ctx.send(resposta,tts=True)

#CALCULAR
@bot.command(name='calc', help='Resolve um problema matemático')
async def calc(ctx,*args):
	if args:
		resposta = ' '.join(args)
		valor = resposta.replace('x','*')
		valor = valor.replace('^','**')
		resposta = '_' + resposta + ' = ' + str(eval(valor)) + '_'
	else: resposta = '...calcular o quê?'
	await ctx.send(resposta)

#DADOS
@bot.command(name='rolar', aliases=['dicef'], help='Rola dados de testes e itens')
async def rolar(ctx,*args):
	global FSELECT
	global DPADRAO
	if len(args) == 0:
		await ctx.send("Pra rolar um dado, escreva nesses formatos: _4,d8,1d6,2d20+2 etc._\n" +\
			"Ah! E você também pode rolar o dado de dano de uma arma se escrever o nome dela!")
	else:
		dado = ''
		itm = None
		kys = [i for i in STHENO.keys()] + [i for i in PRIMATERIA.keys()]

		if len(args) == 2: bonus = int(args[1])
		#ROLAR TESTE DE FICHA
		if stripacc(' '.join(args[0:])).lower() in [stripacc(i).lower() for i in kys if isinstance(i,str)] + \
		[stripacc(' '.join(i).lower()) for i in kys if isinstance(i,tuple)]:
			tbl = sqlite3.connect('data.db')
			com = tbl.cursor()
			fkey = str(ctx.message.author.id)
			if fkey in FSELECT.keys():
				find = None
				for i in eval(f"{FSELECT[fkey][1].upper()}.items()"):
					if isinstance(i[0],tuple) and stripacc(' '.join(args[0:])).upper() == stripacc(' '.join(i[0])).upper():
						find = i[1]
						break
					if isinstance(i[0],str) and stripacc(args[0]).upper() == stripacc(i[0]).upper():
						find = i[1]
						break
				if find:
					com.execute(f"SELECT {find} FROM {FSELECT[fkey][1]} WHERE jogador='{fkey}' AND id='{FSELECT[fkey][0]}' ORDER BY id")
					res = com.fetchone()
					if len(res) > 0:
						if int(res[0]) < 0: dado = DPADRAO + res[0]
						else: dado = DPADRAO + "+" + res[0]
				else: await ctx.send("Não encontrei nenhum teste com esse nome.")
			else: await ctx.send("Nenhuma ficha foi selecionada.")

			tbl.commit()
			com.close()
			tbl.close()
		#ROLAR DADO NORMAL
		elif args[0][0] in 'Dd0123456789': dado = args[0].lower()
		#ROLAR ITEM
		else:
			tbl = sqlite3.connect('data.db')
			com = tbl.cursor()

			com.execute(f"SELECT propriedades,nome FROM items WHERE nome='{args[0]}' ORDER BY nome")
			res = com.fetchone()
			if res:
				palavra = ''
				find = None
				for i in res[0]:
					if palavra.lower() in ('dano:','cura:','mana:'): find = True; itm = res
					if i in ('|',',','.'): find = None; palavra = ''

					if find and i != ' ': dado += i
					else: palavra += i
			tbl.commit()
			com.close()
			tbl.close()

		if dado and dado != '':
			#PROCESSAR DADOS
			resultado = 0
			maxres = 0
			lst = dado.split('-')
			for i in range(len(lst)):
				if i > 0: lst[i] = "-" + lst[i]
				for j in lst[i].split('+'):
					dd = j.split('d')
					if dd[0] == '': dd[0] = '1'
					if len(dd) == 2:
						for v in range(int(dd[0])): resultado += random.randint(1,int(dd[1]))
						maxres += int(dd[0]) * int(dd[1])
					else: resultado += int(dd[0])

			#COMENTAR E ENVIAR RESPOSTA
			if resultado >= maxres: comentario = random.choice(('em cheio!','na mosca!'))
			elif resultado <= 1: comentario = random.choice(('que azar!','ai caramba!','putzgrila!','se deu mal!'))
			elif resultado > int(maxres/2): comentario = random.choice(('boa!','isso aí!','legal!'))
			elif resultado == int(maxres/2): comentario = random.choice(('nada mal.','é.','ok.','beleza.'))
			elif resultado < int(maxres/2): comentario = random.choice(('eita...','vish...','putz...'))

			await ctx.send('**' + dado + ' = **' + str(resultado) + ', ' + comentario)

#############################################

#FREDERICO
@bot.command(name='frederico', aliases=['fred'], help='Responde á um chamado')
async def frederico(ctx): await ctx.send("Me chamaram?")

#SALVE
@bot.command(name='salve', help='Manda um salve')
async def salve(ctx): await ctx.send("Salve salve")

#ABRAÇO
@bot.command(name='abraço', aliases=['abraco'], help='Manda um abraço')
async def abraco(ctx): await ctx.send("Um forte abraço, galera")

#GAY
@bot.command(name='gay', help='gay')
async def gay(ctx): await ctx.send("Gay? Quem?")

#LIMPAR
@bot.command(name='limpaf', help='Apaga todas as mensagens enviadas pelo Frederico')
async def limpaf(ctx):
	await ctx.message.delete()
	for i in await ctx.channel.history(limit=200).flatten():
		if i.author.name == '𝕱𝖗𝖊𝖉𝖊𝖗𝖎𝖈𝖔': await i.delete()

#############################################

def getemb(ctx):
	emb = ''
	if len(ctx.message.attachments) > 0:
		if ctx.message.attachments[0].filename[-4:] in ('.jpg','.png','.gif'):
			emb = ctx.message.attachments[0].url
		elif "https://images-ext-1.discordapp.net" in ctx.message.content or "https://tenor.com/view/" in ctx.message.content:
			emb = ctx.message.content
	return emb

#LEMBRAR
@bot.command(name='lembref', help='Cria um lembrete')
async def lembref(ctx,*args):
	if len(args) == 0: await ctx.send("Para me fazer me lembrar de alguma coisa, dê um nome ao lembrete e depois escreva qualquer mensagem!")
	elif len(args) == 1: await ctx.send("Você deu um marcador ao lembrete, mas não me disse do que eu devo me lembrar!")
	elif args[0] != '-tudo':
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()
		emb = getemb(ctx)

		com.execute("CREATE TABLE IF NOT EXISTS lembretes (id text,mensagem text,embed text)")
		com.execute(f"DELETE FROM lembretes WHERE id='{args[0]}'")
		com.execute(f"INSERT INTO lembretes VALUES ('{args[0]}','{' '.join(args[1:])}','{emb}')")

		tbl.commit()
		com.close()
		tbl.close()
		await ctx.send(random.choice(('Pode contar comigo!','Não vou me esquecer!','Pode deixar!')))
	else: await ctx.send("Você pode dar o nome que quiser para seu marcador, menos esse aqui, ok?")

#ESQUECER
@bot.command(name='esquecaf', help='Apaga um lembrete')
async def esquecaf(ctx,*args):
	if len(args) == 0: await ctx.send("Se quiser que eu me esqueça de um lembrete, escreva o marcador que deu para ele.")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		if args[0] == '-tudo': com.execute("DELETE FROM lembretes")
		else: com.execute(f"DELETE FROM lembretes WHERE id='{args[0]}'")
		await ctx.send(random.choice(('Hã? Esquecer o quê?','Me esqueci de alguma coisa?')))

		tbl.commit()
		com.close()
		tbl.close()

#MOSTRAR LEMBRETES
@bot.command(name='lembretes', help='Mostra todos os lembretes')
async def lembretes(ctx):
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()

	com.execute("SELECT * FROM lembretes ORDER BY id")
	res = com.fetchall()
	if res:
		await ctx.send("**Estes são os seus lembretes:**")
		for i in res:
			await ctx.send(i[0] + ': ' + i[1])
			if i[2] != '':
				emb = discord.Embed()
				emb.set_image(url=i[2])
				await ctx.send(embed=emb)
	else: await ctx.send(random.choice(("Você não me pediu para me lembrar de nada.","Que lembretes?","Você não tem lembretes.")))

	tbl.commit()
	com.close()
	tbl.close()

#############################################

#ADICIONAR Á TABELA
@bot.command(name='adicionarf', aliases=['addf'], help='Cria uma tabela ou adiciona um item')
async def adicionarf(ctx,*args):
	if len(args) == 0:
		await ctx.send("Não sabe adicionar um item?\n" +\
			"Se liga: é só escrever em qual tabela quer adicionar, o nome do item, o preço e as outras coisinhas\n" +\
			"Tipo o dano da arma, o bônus de CA, sei lá... mas só se quiser, pode deixar vazio.")
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
@bot.command(name='renomearf', aliases=['renamef'], help='Renomeia uma tabela ou item')
async def renomearf(ctx,*args):
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
@bot.command(name='apagarf', aliases=['delf'], help='Apaga uma tabela ou item')
async def apagarf(ctx,*args):
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
@bot.command(name='tabelaf', aliases=['tablef'], help='Mostra tabelas criadas')
async def tabelaf(ctx,*args):
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()
	if len(args) == 0:
		com.execute(f"SELECT DISTINCT tabela FROM items ORDER BY tabela")
		res = com.fetchall()
		if res and len(res) > 0:
			if len(res) == 1: resposta = '**Você tem apenas uma tabela:**\n'
			else: resposta = '**Estas são as suas tabelas:**\n'
			for i in res: resposta += f"• _{i[0]}_\n"
			await ctx.send(resposta)
		else: await ctx.send("Você ainda não criou nenhuma tabela.")
	else:

		if len(args) == 2: com.execute(f"SELECT * FROM items WHERE nome='{args[1]}' ORDER BY nome")
		else: com.execute(f"SELECT * FROM items WHERE tabela='{args[0]}' ORDER BY nome")
		res = com.fetchall()
		if res:
			await ctx.send(f"**{args[0]}**")
			txt = ''
			for i in res:
				if len(txt) > 1500:
					await ctx.send(txt)
					txt = ''
				if i[3]: txt += f"**{i[1]}:** {i[2]}$ | _{i[3]}_\n"
				else: txt += f"**{i[1]}:** {i[2]}$\n"
			await ctx.send(txt)
		else: await ctx.send("Eu não consegui encontrar nada...")
	tbl.commit()
	com.close()
	tbl.close()

#############################################

PALAVRA = ''
REVELADO = ''
ETIPO = ''

#ENIGMA
@bot.command(name='enigmaf', help='Cria um enigma para ser resolvido')
async def enigmaf(ctx,*args):
	global PALAVRA
	global REVELADO
	global ETIPO

	if PALAVRA:
		txt = ' '.join(args).upper()
		if txt == '-DICA':
			rr = 0
			while REVELADO[rr] != '-': rr = random.randint(0,len(PALAVRA))
			REVELADO = REVELADO[:rr] + PALAVRA[rr] + REVELADO[rr + 1:]
			await ctx.send(f"**{REVELADO}**")
		elif len(txt) == 1 and ETIPO == 'FORCA':
			for i in range(len(PALAVRA)):
				if PALAVRA[i] == args[0].upper():
					REVELADO = REVELADO[:i] + args[0].upper() + REVELADO[i + 1:]
			await ctx.send(f"**{REVELADO}**")
		elif txt == PALAVRA:
			await ctx.send(f"Você acertou! A palavra/frase era **{PALAVRA}**")
			PALAVRA = ''
			REVELADO = ''
			ETIPO = ''
		else: await ctx.send(random.choice("Nope, essa não é a palavra/frase.","Não é essa palavra/frase.","Resposta incorreta."))
	else:
		if len(args) == 0: await ctx.send("Escreva se é um jogo de forca ou anagrama.")
		elif len(args) == 1: await ctx.send("Me manda uma frase ou palavra e vou criar um enigma a partir disso.")
		else:
			await ctx.message.delete()
			ETIPO = stripacc(args[0]).upper()
			if ETIPO in ['FORCA','ANAGRAMA']:
				PALAVRA = ' '.join(args[1:]).upper()
				if PALAVRA != '-DICA':
					if ETIPO == 'FORCA':
						for i in PALAVRA:
							if i == ' ': REVELADO += ' '
							else: REVELADO += '-'
					elif ETIPO == 'ANAGRAMA':
						REVELADO = ''.join(random.sample(PALAVRA,len(PALAVRA)))
					await ctx.send("Enigma criado! Quero ver vocês resolverem!")
					if ETIPO == 'FORCA': await ctx.send(f"A palavra/frase contém **{len(PALAVRA.replace(' ',''))} letras.**")
					if ETIPO == 'ANAGRAMA': await ctx.send(f"O enigma é **{REVELADO}.**")
				else: await ctx.send("Calmae bródi, você não pode fazer isso.")
			else: await ctx.send("O tipo de enigma é inválido.")

#############################################

STHENO = {
	'Jogador': 'jogador','Personagem': 'personagem','Nome': 'personagem','Classe': 'classe','Raça': 'raca','Nível': 'nivel',
	'Idade': 'idade','CA': 'armadura','PV': 'vida','PM': 'mana','Mana': 'mana','Benção': 'bencao','Morte': 'morte',
	'Adrenalina': 'adrenalina','Sanidade': 'sanidade','Condição': 'condicao',('Pontos','de','destino'): 'destino',
	'Ouro': 'ouro',('PA','diário'): 'ourodiario',

	'Combate': 'combate',('Combate','ágil'): 'combateagil','Disparo': 'disparo','Venefíces': 'venefices',
	'Força': 'forca','Destreza': 'destreza','Constituição': 'constituicao','Inteligência': 'inteligencia','Sabedoria': 'sabedoria','Carisma': 'carisma','Sorte': 'sorte',
	'Atletismo': 'atletismo','Vontade': 'vontade','Forja': 'forja','Mineração': 'mineracao',
	'Cavalgar': 'cavalgar','Acrobacia': 'acrobacia','Furtividade': 'furtividade','Furto': 'furto','Reflexos': 'reflexos','Coleta': 'coleta','Cozinha': 'cozinha','Artesanato': 'artesanato',
	'Fortitude': 'fortitude','Imunidade': 'imunidade',
	'História': 'historia','Investigação': 'investigacao','Medicina': 'medicina','Percepção': 'percepcao','Sobrevivência': 'sobrevivencia','Jogatina': 'jogatina','Fabricação': 'fabricacao','Mecânica': 'mecanica',
	'Natureza': 'natureza','Religião': 'religiao',('Lidar','com','animais'): 'animais','Ocultismo': 'ocultismo','Arcanismo': 'arcanismo','Intuição': 'intuicao','Encantamento': 'encantamento','Alquimia': 'alquimia',
	'Persuasão': 'persuasao','Intimidação': 'intimidacao','Blefar': 'blefar','Atuação': 'atuacao',('Saber','das','ruas'): 'ruas','Liderança': 'lideranca','Treinamento': 'treinamento','Nobreza': 'nobreza',
	'Loot': 'loot','Viagem': 'viagem','Descanso': 'descanso',
	'Aparência': 'aparencia','Passado': 'passado','Anotações': 'anotacoes'
}
TORMENTA = {
	'Jogador': 'jogador','Personagem': 'personagem','Nome': 'personagem','Classe': 'classe','Nível': 'nivel','Raça': 'raca',
	'Origem': 'origem','Divindade': 'divindade',
	'PV': 'vida','Condição': 'condicao','PM': 'mana','Mana': 'mana','Benção': 'bencao','CA': 'armadura','Defesa': 'armadura',
	'Ouro': 'ouro',

	'Força': 'forca','Destreza': 'destreza','Constituição': 'constituicao',
	'Inteligência': 'inteligencia','Sabedoria': 'sabedoria','Carisma': 'carisma',
	'Atletismo': 'atletismo','Acrobacia': 'acrobacia','Atuação': 'atuacao','Cavalgar': 'cavalgar','Cura': 'cura',
	'Diplomacia': 'diplomacia','Enganação': 'enganacao','Fortitude': 'fortitude','Furtividade': 'furtividade',
	'Iniciativa': 'iniciativa','Intimidação': 'intimidacao','Intuição': 'intuicao','Investigação': 'investigacao',
	'Luta': 'luta','Pontaria': 'pontaria','Reflexos': 'reflexos','Sobrevivência': 'sobrevivencia','Vontade': 'vontade',

	'Alquimia': 'alquimia','Culinária': 'culinaria','Ladinagem': 'ladinagem','Misticismo': 'misticismo','Percepção': 'percepcao',
	'Aparência': 'aparencia','Personalidade': 'personalidade','Anotações': 'anotacoes'
}
PRIMATERIA = {
	'Jogador': 'jogador','Personagem': 'personagem','Nome': 'personagem','Vocação': 'vocacao','Nível': 'nivel','Espécie': 'especie',
	'Idade': 'idade','Gênero': 'genero','Signo': 'signo',('Tipo','Sanguíneo'): 'sangue',
	'Vitalidade': 'vitalidade','Condição': 'condicao','Sanidade': 'sanidade','Benção': 'bencao','Ética': 'etica',
	'Fome': 'fome','Sede': 'sede','Sono': 'sono','Ouro': 'ouro',

	'Força': 'forca','Atletismo': 'atletismo','Atitude': 'atitude','Luta': 'luta',
	'Agilidade': 'agilidade','Acrobacia': 'acrobacia','Reflexos': 'reflexos','Furtividade': 'furtividade','Pontaria': 'pontaria',
	'Resistência': 'resistencia','Fortitude': 'fortitude','Disposição': 'disposicao','Imunidade': 'imunidade','Tolerância': 'tolerancia',
	'Sabedoria': 'sabedoria','Intuição': 'intuicao','Percepção': 'percepcao','Investigação': 'investigacao',
	'Carisma': 'carisma','Inspiração': 'inspiracao','Intimidação': 'intimidacao','Negociação': 'negociacao','Persuasão': 'persuasao',
	'Aparência': 'aparencia','Personalidade': 'personalidade','Anotações': 'anotacoes'
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

#FICHA DE PERSONAGEM
@bot.command(name='fichaf', help='Gerencia informações e testes do personagem')
async def fichaf(ctx,*args):
	global FSELECT

	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()
	fkey = str(ctx.message.author.id)
	if len(args) == 0:
		find = True
		if fkey in [i for i in FSELECT.keys()]:
			fsys = FSELECT[fkey][1]
			fname = FSELECT[fkey][0]
			com.execute(f"SELECT * FROM {fsys} WHERE id='{fname}'")
			res = com.fetchone()
		else: res = None

		#MOSTRAR FICHA
		if res and fsys and len(res) > 0:
			if ('Mestres' in [i.name for i in ctx.message.author.roles]) or (res[2] == fkey):
				k = 2
				resposta = ''
				for i in eval(f"{fsys.upper()}.items()"):
					if len(resposta) > 1500:
						await ctx.send(resposta)
						resposta = ''
					if i[0] not in ('Mana','Nome','Defesa'):
						go = False
						if find == True: go = True
						elif i[1] == find: go = True
						if go:
							#FORMATAÇÃO STHENO
							if fsys == 'stheno':
								if k > 18 and k < 71: resposta += "• "

								if k == 2: resposta += f"_**{i[0]}:** {ctx.message.author.name}"
								elif isinstance(i[0],tuple): resposta += f"_**{' '.join(i[0])}:** {res[k]}"
								else: resposta += f"_**{i[0]}:** {res[k]}"

								if k in (17,18): resposta += f"$_\n"
								else: resposta += f"_\n"

								if find == True:
									if k == 16: resposta += "\n"
									if k == 18: resposta += "\n**CAPACIDADES**\n"
									if k == 22: resposta += "\n**TESTES**\n"
									if k == 29: resposta += "\n**FORÇA**\n"
									if k == 33: resposta += "\n**DESTREZA**\n"
									if k == 41: resposta += "\n**CONSTITUIÇÃO**\n"
									if k == 43: resposta += "\n**INTELIGÊNCIA**\n"
									if k == 51: resposta += "\n**SABEDORIA**\n"
									if k == 59: resposta += "\n**CARISMA**\n"
									if k == 67: resposta += "\n**SORTE**\n"
									if k == 70: resposta += "\n**SOBRE**\n"
							#FORMATAÇÃO TORMENTA
							if fsys == 'tormenta':
								if k > 14 and k < 44: resposta += "• "

								if k == 2: resposta += f"_**{i[0]}:** {ctx.message.author.name}"
								elif isinstance(i[0],tuple): resposta += f"_**{' '.join(i[0])}:** {res[k]}"
								else: resposta += f"_**{i[0]}:** {res[k]}"

								if k in (14,): resposta += f"T$_\n"
								else: resposta += f"_\n"

								if find == True and k in (14,20,43,): resposta += "\n"
							#FORMATAÇÃO PRIMATERIA
							if fsys == 'primateria':
								if k > 20 and k < 43 and k not in (24,29,34,38): resposta += "• "

								if k == 2: resposta += f"_**{i[0]}:** {ctx.message.author.name}"
								elif isinstance(i[0],tuple): resposta += f"_**{' '.join(i[0])}:** {res[k]}"
								elif k in (20,24,29,34,38,): resposta += f"**{i[0].upper()}:** {res[k]}"
								else: resposta += f"_**{i[0]}:** {res[k]}"

								if k == 19: resposta += f"T$_"
								elif k not in (20,24,29,34,38,): resposta += f"_"

								if find == True:
									if k in (3,6,): resposta += "\n"
									elif k in (10,19,23,28,33,37,42): resposta += "\n\n"
									elif k < 20: resposta += " | "
									else: resposta += "\n"
						k += 1
						if k >= len(res): break
				await ctx.send(resposta)
				if res[1] != '':
					emb = discord.Embed()
					emb.set_image(url=res[1])
					await ctx.send(embed=emb)
			else: await ctx.send("Essa ficha não é sua, apenas o dono dela pode visualizá-la.")
		else:
			#LISTAR FICHAS
			com.execute(f"SELECT id FROM stheno")
			lst = [(i[0],'stheno') for i in com.fetchall()]
			com.execute(f"SELECT id FROM tormenta")
			lst += [(i[0],'tormenta') for i in com.fetchall()]
			com.execute(f"SELECT id FROM primateria")
			lst += [(i[0],'primateria') for i in com.fetchall()]
			if lst and len(lst) > 0:
				resposta = "**Fichas salvas:**\n"
				for i in lst: resposta += f"• _{i[0]}: {i[1]}_\n"
				await ctx.send(resposta)
			else: await ctx.send("Para criar uma ficha, escreva _\"stheno\", \"tormenta\" ou \"primateria\"_ para escolher um sistema de ficha, " +\
		"em seguida, dê um nome para a ficha e me mande ela para eu poder processá-la e guardar na minha memória super inteligente!\n" +\
		"Após criada, escreva o nome da ficha para ver ela completa. Se quiser ver apenas um único atributo da ficha, escreva o atributo em seguida.\n" +\
		"Se quiser mudar o valor desse atributo, insira o novo valor em seguida. Não é difícil!\n" +\
		"Escreva _\"apagar\"_ e o nome da ficha caso queira apagá-la.")
	else:
		#ADICIONAR FICHA
		if args[0].lower() in ('stheno','tormenta','primateria') and len(args) > 2:
			async with ctx.typing():
				txt = ' '.join(args[2:])
				emb = getemb(ctx)

				#CRIAR TABELAS
				add = 'jogador text,'
				ins = f"'{ctx.message.author.id}',"
				for i in eval(f"{args[0].upper()}.items()"):
					if i[0] not in ('Jogador','Nome','Mana','Defesa'): add += i[1] + ' text,'; ins += "'0',"
				com.execute(f"CREATE TABLE IF NOT EXISTS {args[0].lower()} (id text,embed text,{add[:-1]})")
				com.execute("CREATE TABLE IF NOT EXISTS fselect (id text,ficha text,tbl text)")
				com.execute("CREATE TABLE IF NOT EXISTS inventario (id text,nome text,quantidade text,propriedades text)")
				com.execute("CREATE TABLE IF NOT EXISTS magias (id text,nome text,propriedades text,mana text)")
				for i in ('stheno','primateria','tormenta','inventory'):
					try: com.execute(f"DELETE FROM {i} WHERE id='{stripacc(args[1]).lower()}'")
					except: pass
				com.execute(f"INSERT INTO {args[0].lower()} VALUES ('{stripacc(args[1]).lower()}','{emb}',{ins[:-1]})")
				com.execute(f"DELETE FROM fselect WHERE id='{ctx.message.author.id}'")
				com.execute(f"INSERT INTO fselect VALUES ('{ctx.message.author.id}','{stripacc(args[1]).lower()}','{args[0].lower()}')")
				FSELECT[fkey] = [stripacc(args[1]).lower(),args[0].lower()]

				#LER FICHA
				palavra = ''
				valor = ''
				find = None
				lista = {}

				for caractere in range(len(txt)):
					#CRIAR NOME E VALOR DA VARIÁVEL
					if find != 'ABRPAR' and txt[caractere] not in ('•','\n','(','|'):
						if find == None: palavra += txt[caractere]
						else: valor += txt[caractere]
					
					#ENCONTROU UM ATRIBUTO NO TEXTO
					if find == None and stripacc(palavra).upper() not in lista.keys():
						for i in eval(f"{args[0].upper()}.items()"):
							if isinstance(i[0],tuple):
								if stripacc(palavra).upper() == stripacc(' '.join(i[0])).upper() + ':':
									find = i[1]
									break
							else:
								if stripacc(palavra).upper() == stripacc(i[0]).upper() + ':':
									find = i[1]
									break

					#TERMINAR DE LER VARIÁVEL
					if txt[caractere] in ('\n','(',' ','|'):
						if find and find != 'ABRPAR' and find not in lista and len(valor.replace(' ','')) > 0:
							if find != 'jogador':
								com.execute(f"UPDATE {args[0].lower()} SET {find}='{valor.replace(' ','')}' WHERE id='{stripacc(args[1]).lower()}'")
								lista[find] = valor
							valor = ''
							find = None
						if palavra not in [j for i in eval(f"{args[0].upper()}.keys()") if isinstance(i,tuple) for j in i]:
							palavra = ''

					#IGNORAR TUDO ENTRE PARÊNTESES
					if find == None and txt[caractere] == '(': find = 'ABRPAR'
					if find == 'ABRPAR' and txt[caractere] == ')': find = None

			await ctx.message.delete()
			await ctx.send(f"Salvei a ficha do personagem **{args[1]}** aqui comigo! ;)")

		#APAGAR FICHA
		elif args[0] == 'apagar':
			if fkey in [i for i in FSELECT.keys()]:
				fsys = FSELECT[fkey][1]
				fname = FSELECT[fkey][0]
				com.execute(f"SELECT jogador FROM {fsys} WHERE id='{fname}' AND jogador='{fkey}'")
				res = com.fetchone()
			elif len(args) > 1:
				res = None
				fsys = None
				fname = stripacc(args[1]).lower()
				for i in ('stheno','tormenta','primateria'):
					com.execute(f"SELECT jogador FROM {i} WHERE id='{fname}'")
					res = com.fetchone()
					if res and len(res) > 0: fsys = i; break
			else: res = None

			if res and len(res) > 0:
				if 'Mestres' in [i.name for i in ctx.message.author.roles] or res[0] == fkey:
					com.execute(f"DELETE FROM {fsys} WHERE id='{fname}'")
					com.execute(f"DELETE FROM inventario WHERE id='{fname}'")
					await ctx.send(f"Apaguei a ficha **{fname}**.")
				else: await ctx.send("Essa ficha não é sua, apenas o dono dela pode apagá-la.")
			else: await ctx.send("Eu não tenho nenhuma ficha salva comigo.")

		#DEBUG
		elif args[0] == 'sql':
			com.execute(' '.join(args[1:]))
			res = com.fetchall()
			if len(res) > 0:
				for i in res: await ctx.send(i)

		#SELECIONAR/ALTERAR FICHA
		else:
			res = None
			fsys = None
			fname = stripacc(args[0]).lower()
			if fkey in FSELECT.keys():
				res = (fkey,)
				fsys = FSELECT[fkey][1]
				fname = FSELECT[fkey][0]
			for i in ('stheno','tormenta','primateria'):
				com.execute(f"SELECT jogador,personagem,nivel FROM {i} WHERE id='{fname}'")
				res = com.fetchone()
				if res and len(res) > 0: fsys = i; break

			if res and fsys and len(res) > 0:
				find = None
				for i in eval(f"{fsys.upper()}.items()"):
					if isinstance(i[0],str) and stripacc(args[0]).upper() == stripacc(i[0]).upper():
						find = i; break
				if ('Mestres' in [i.name for i in ctx.message.author.roles]) or (res[0] == fkey):
					#ALTERAR FICHA
					if len(args) > 1:
						com.execute(f"UPDATE {fsys} SET {find[1]}='{' '.join(args[1:])}' WHERE id='{fname}'")
						await ctx.send(f"**{find[0]}** alterado para _{' '.join(args[1:])}_")
					#MOSTRAR ATRIBUTO
					elif find:
						com.execute(f"SELECT {find[1]} FROM {fsys} WHERE id='{fname}' AND jogador='{fkey}'")
						ff = com.fetchone()
						if ff and len(ff) > 0: await ctx.send(f"_**{find[0]}**: {ff[0]}_")
						else: await ctx.send(f"Não consegui encontrar essa informação.")
					#SELECTIONAR FICHA
					else:
						FSELECT[fkey] = [stripacc(args[0]).lower(),fsys]
						#await ctx.author.edit(nick=f"{res[1]} lv.{res[2]}")
						await ctx.send(f"Você selecionou a ficha **{stripacc(args[0]).lower()}**")
				else: await ctx.send("Essa ficha não é sua, apenas o dono dela pode visualizá-la.")
			else:
				if fkey not in FSELECT.keys():
					await ctx.send("Parece que você não selecionou sua ficha. Para selecionar, escreva \"fichaf\" e veja a lista de fichas.")
				else: await ctx.send("Eu não consegui encontrar sua ficha.")

	tbl.commit()
	com.close()
	tbl.close()

#INVENTÁRIO DE PERSONAGEM
@bot.command(name='inventariof', aliases=['invf'], help='Gerencia o inventário do personagem')
async def inventariof(ctx,*args):
	'''if len(args) == 0: await ctx.send("Insira o nome da sua ficha para visualizá-la.\n\
		Caso queira comprar algo, escreva \"comprar\" e em seguida o nome do item.\n\
		Para remover um item, escreva \"remover\" e em seguida o nome do item.")
	else:'''
	global FSELECT
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()
	fkey = str(ctx.message.author.id)

	#VALIDAR FICHA
	res = None
	fname = None
	if len(args) > 0: fname = stripacc(args[0]).lower()
	fsys = None
	find = True
	if fkey in FSELECT.keys():
		fsys = FSELECT[fkey][1]
		fname = FSELECT[fkey][0]
	if fname:
		for i in ('stheno','tormenta','primateria'):
			com.execute(f"SELECT jogador,ouro FROM {i} WHERE id='{fname}'")
			res = com.fetchone()
			if res and len(res) > 0: fsys = i; break
	if res and len(res) > 0:
		if 'Mestres' in [i.name for i in ctx.message.author.roles] or res[0] == fkey:
			#PEGAR/COMPRAR ITEM
			if len(args) > 1 and args[0] in ('pegar','comprar'):
				qnt = 1
				tb = None
				if len(args) > 2:
					try: qnt = int(args[2])
					except: tb = args[2]

				#VERIFICAR ITENS REPETIDOS
				if tb: com.execute(f"SELECT nome,propriedades,preco,tabela FROM items WHERE nome='{args[1]}' AND tabela='{tb}'")
				else: com.execute(f"SELECT nome,propriedades,preco,tabela FROM items WHERE nome='{args[1]}'")
				itm = com.fetchall()
				if not itm or len(itm) == 0: await ctx.send("Não consegui encontrar o item desejado.")
				elif len(itm) > 1:
					resposta = "Opa! Existem mais itens com o mesmo nome:\n"
					for i in itm: resposta += f"_{i[0]}: {i[3]}_\n"
					resposta += "Para prosseguir, repita o comando adicionando o nome da tabela."
					await ctx.send(resposta)
				else: itm = itm[0]
				
				#VERIFICAR PREÇO
				if args[0] == 'comprar': preco = int(itm[2]) * qnt
				else: preco = 0
				if not itm or len(itm) == 0: await ctx.send("Não consegui encontrar o item desejado.")
				elif float(res[1]) < preco:
					if qnt > 1: await ctx.send(f"Você não tem dinheiro suficiente!\n_{qnt}x{itm[0]} = {preco}$_")
					else: await ctx.send(f"Você não tem dinheiro suficiente!\n_{itm[0]} = {int(itm[2])}$_")
				else:
					#AUMENTAR QUANTIDADE OU ADICIONAR
					com.execute(f"SELECT quantidade FROM inventario WHERE id='{fname}' AND nome='{args[1]}'")
					inv = com.fetchall()
					if inv and len(inv) > 0:
						com.execute(f"UPDATE inventario SET quantidade='{qnt}' WHERE id='{fname}' AND nome='{args[1]}'")
					else: com.execute(f"INSERT INTO inventario VALUES ('{fname}','{itm[0]}','{qnt}','{itm[1]}')")

					com.execute(f"UPDATE {fsys} SET ouro='{float(res[1]) - preco}' WHERE id='{fname}'")
					if preco == 0: await ctx.send(f"Você adicionou **{itm[0]}** no seu inventário!")
					else: await ctx.send(f"Você gastou -{preco}$ e adicionou **{itm[0]}** no seu inventário!")
			
			#REMOVER ITEM
			elif len(args) > 1 and args[0] == 'remover':
				com.execute(f"SELECT quantidade FROM inventario WHERE id='{fname}' AND nome='{args[1]}'")
				itm = com.fetchone()
				if itm and len(itm) > 0:
					qnt = 1
					if len(args) > 2:
						try: qnt = int(args[2])
						except: qnt = 1
					if int(itm[0]) > qnt:
						com.execute(f"UPDATE inventario SET quantidade='{int(itm[0]) - qnt}' WHERE id='{fname}' AND nome='{args[1]}'")
						await ctx.send(f"Você tem atualmente {int(itm[0]) - qnt}x**{args[1]}**.")
					else:
						com.execute(f"DELETE FROM inventario WHERE id='{fname}' AND nome='{args[1]}'")
						await ctx.send(f"**{args[1]}** foi apagado do seu inventário.")
				else: await ctx.send("Relaxa, você nem tem esse item.")
			
			#ALTERAR/MOSTRAR ITEM
			elif len(args) > 0:
				com.execute(f"SELECT * FROM inventario WHERE id='{fname}' AND nome='{args[0]}'")
				itm = com.fetchone()
				if itm and len(itm) > 0:
					#ALTERAR ITEM
					if len(args) > 1:
						com.execute(f"UPDATE inventario SET propriedades='{' '.join(args[1:])}' WHERE id='{fname}' AND nome='{args[0]}'")
					#MOSTRAR ITEM
					else:
						txt = ''
						if int(itm[2]) > 1: txt += f"• {itm[2]}x**{itm[1]}**"
						else: txt += f"• **{itm[1]}**"
						if itm[3]: txt += f" | _{itm[3]}_\n"
						else: txt += "\n"
						await ctx.send(txt)
				else: await ctx.send(f"Não consegui encontrar esse item.")

			#MOSTRAR INVENTÁRIO
			else:
				com.execute(f"SELECT * FROM inventario WHERE id='{fname}' ORDER BY nome")
				itm = com.fetchall()
				if len(itm) > 0:
					txt = ''
					peso = 0
					for i in itm:
						if int(i[2]) > 1: txt += f"• {i[2]}x**{i[1]}**"
						else: txt += f"• **{i[1]}**"
						if i[3]:
							txt += f" | _{i[3]}_\n"
							#SOMAR PESO
							palavra = ''
							fpeso = ''
							find = None
							for i in i[3]:
								if palavra.lower() == 'peso:': find = True
								if i in ('|','.'): find = None; palavra = ''

								if find and i not in (' ','k','g'): fpeso += i
								elif i not in (' ','|'): palavra += i
							if fpeso: peso += float(fpeso.replace(',','.'))
						else: txt += "\n"
					await ctx.send(f"**INVENTÁRIO DE {fname.upper()}** _(Peso: {str(peso).replace('.',',')}kg)_\n" + txt)
				else: await ctx.send("O seu inventário está vazio!")
		else: await ctx.send("Essa ficha não é sua, apenas o dono dela pode visualizá-la.")
	else: await ctx.send("Eu não consegui encontrar sua ficha.")

	tbl.commit()
	com.close()
	tbl.close()

#HABILIDADES DO PERSONAGEM
@bot.command(name='magiasf', aliases=['magf','habilidadesf','habf'], help='Gerencia as habilidades, características e magias do personagem')
async def magiasf(ctx,*args):
	global FSELECT
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()
	fkey = str(ctx.message.author.id)

	#VALIDAR FICHA
	res = None
	fname = None
	if len(args) > 0: fname = stripacc(args[0]).lower()
	fsys = None
	find = True
	if fkey in FSELECT.keys():
		fsys = FSELECT[fkey][1]
		fname = FSELECT[fkey][0]
	if fname:
		for i in ('stheno','tormenta','primateria'):
			com.execute(f"SELECT jogador,ouro FROM {i} WHERE id='{fname}'")
			res = com.fetchone()
			if res and len(res) > 0: fsys = i; break
	if res and len(res) > 0:
		if 'Mestres' in [i.name for i in ctx.message.author.roles] or res[0] == fkey:
			#ADICIONAR MAGIA
			if len(args) > 3 and args[0] in ('adicionar','add'):
				com.execute(f"INSERT INTO magias VALUES ('{fname}','{args[1]}','{' '.join(args[3:])}','{args[2]}')")
				await ctx.send(f"Você aprendeu a usar **{args[1]}**!")
			
			#REMOVER MAGIA
			elif len(args) > 1 and args[0] in ('remover','del'):
				com.execute(f"SELECT nome FROM magias WHERE id='{fname}' AND nome='{args[1]}'")
				itm = com.fetchone()
				if itm and len(itm) > 0:
					com.execute(f"DELETE FROM magias WHERE id='{fname}' AND nome='{args[1]}'")
					await ctx.send(f"Você esqueceu como fazer **{args[1]}**.")
				else: await ctx.send("Relaxa, você nem tem essa habilidade.")
			
			#ALTERAR/MOSTRAR ITEM
			elif len(args) > 0:
				com.execute(f"SELECT * FROM magias WHERE id='{fname}' AND nome='{args[0]}'")
				itm = com.fetchone()
				if itm and len(itm) > 0:
					#ALTERAR ITEM
					if len(args) > 1:
						com.execute(f"UPDATE magias SET propriedades='{' '.join(args[1:])}' WHERE id='{fname}' AND nome='{args[0]}'")
					#MOSTRAR ITEM
					else:
						txt = f"• **{itm[1]}** | _{itm[2]}_"
						if itm[3]: txt += f" _-{itm[3]}PM_\n"
						else: txt += "\n"
						await ctx.send(txt)
				else: await ctx.send(f"Não consegui encontrar esse item.")

			#MOSTRAR MAGIAS
			else:
				com.execute(f"SELECT * FROM magias WHERE id='{fname}' ORDER BY nome")
				itm = com.fetchall()
				if len(itm) > 0:
					txt = ''
					for i in itm:
						txt += f"• **{i[1]}** | _{i[2]}_"
						if i[3]: txt += f" _-{i[3]}PM_\n"
						else: txt += "\n"
					await ctx.send(f"**MAGIAS & HABILIDADES DE {fname.upper()}**\n" + txt)
				else: await ctx.send("Você não tem habilidades!")
		else: await ctx.send("Essa ficha não é sua, apenas o dono dela pode visualizá-la.")
	else: await ctx.send("Eu não consegui encontrar sua ficha.")

	tbl.commit()
	com.close()
	tbl.close()

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

async def entrarvoz(ctx,aviso=False):
	voice_client = ctx.message.guild.voice_client
	if not ctx.message.author.voice:
		await ctx.send("{}, entre num chat de voz primeiro!".format(ctx.message.author.name))
	elif voice_client and voice_client.is_connected():
		if aviso: await ctx.send("Eu já tô aqui, truta!")
	else: await ctx.message.author.voice.channel.connect()

#TOCAR MÚSICA
@bot.command(name='radio', help='Toca uma música')
async def radio(ctx,*args):
	if len(args) == 0: await ctx.send("Escreva _\"play\"_ e insira um url do YouTube para eu tocar uma música!\n\
		Escreva _\"pause\"_,_\"play\"_ ou _\"pare\"_ para eu pausar, continuar ou parar uma música.")
	else:
		voice_client = ctx.message.guild.voice_client
		if args[0] == 'entrar': await entrarvoz(ctx,True)

		elif args[0] == 'sair':
			if voice_client and voice_client.is_connected(): await voice_client.disconnect()
			else: await ctx.send("Oxe, eu já saí!")
		
		elif args[0] == 'play':
			await entrarvoz(ctx)
			if voice_client and voice_client.is_connected():
				if voice_client.is_paused(): await voice_client.resume()
				else:
					async with ctx.typing():
						filename = await YTDLSource.from_url(args[1], loop=bot.loop)
						voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"downloads/{filename}"))
					await ctx.send('**DJ Frederico lançou a braba:** {}'.format(YTDLSource.title))
			else: await ctx.send("Eu não estou em nenhum chat de voz.")
		
		elif args[0] == 'pause':
			if voice_client and voice_client.is_connected() and voice_client.is_playing(): await voice_client.pause()
			else: await ctx.send("Eu não estou tocando nada, cara!")
		elif args[0] == 'pare':
			if voice_client and voice_client.is_connected() and voice_client.is_playing(): await voice_client.stop()
			else: await ctx.send("Eu não estou tocando nada, cara!")

#SONOPLASTIA
@bot.command(name='sfx', help='Toca um efeito sonoro')
async def sfx(ctx,*args):
	if len(args) == 0: await ctx.send("Digite o nome de um áudio pra eu poder tocar pra você.")
	else:
		await entrarvoz(ctx)
		voice_client = ctx.message.guild.voice_client
		if voice_client and voice_client.is_connected():
			if voice_client.is_playing(): voice_client.stop()
			try:
				filename = "C:\\Users\\kaixtr\\Music\\Defeitos Sonoros\\" + stripacc(' '.join(args)).lower() + ".mp3"
				voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
			except: await ctx.send("Foi mal, não encontrei esse áudio.")

#############################################

#CONFIGURAR
@bot.command(name='setf', aliases=['configf'], help='Configura o Frederico')
async def setf(ctx,*args):
	global DPADRAO
	if len(args) > 0:
		if args[0] in ('-dado','-dice'): DPADRAO = args[1].lower()

#HELP
@bot.command(name='ajudaf', aliases=['helpf'], help='Mostra todos os comandos')
async def ajuda(ctx,*args):
	await ctx.send("O que eu sei fazer? Sei fazer um monte de coisas, bebê!\n\
**falef:** vou dizer qualquer coisa que digitar.\n\
**calc:** vou calcular qualquer conta matemática que digitar.\n\
**rolar:** vou rolar dados por você.\n\
\n\
**lembref:** se precisar lembrar de algo, vou lembrar pra você.\n\
**esquecaf:** se quiser que eu esqueça, eu faço também.\n\
**lembretes:** mostro todos os lembretes pra você.\n\
\n\
**addf:** crio uma tabela com itens e adiciono ele.\n\
**renomearf:** troco o nome de uma tabela ou item.\n\
**apagarf:** apago qualquer tabela ou item.\n\
**tabelaf:** mostro uma tabela.\n\
\n\
**enigmaf:** crio um quebra-cabeça de palavras para você resolver.\n\
**fichaf:** mostro fichas de personagem salvas por você.\n\
**invf:** gerencio os itens de seu personagem.\n\
**magf:** gerencio magias e habilidades de seu personagem.\n\
\n\
**radio:** toco músicas para animar a garotada.\n\
**sfx:** por último, mas não menos importante, também sou sonoplasta do ratinho.\n")

if __name__ == "__main__": bot.run(TOKEN)