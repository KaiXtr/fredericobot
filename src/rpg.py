import sqlite3
import random
from intents import *

async def enigma(ctx,*args):
	global PALAVRA
	global REVELADO
	global ETIPO

	if PALAVRA:
		txt = ' '.join(args).upper()
		if txt == '-DICA':
			rr = 0
			while REVELADO[rr] != '-':
				rr = random.randint(0,len(PALAVRA))
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
		else:
			await ctx.send(random.choice("Nope, essa não é a palavra/frase.","Não é essa palavra/frase.","Resposta incorreta."))
		return
	
	if len(args) == 0:
		await ctx.send("Escreva se é um jogo de forca ou anagrama.")
		return
	
	if len(args) == 1:
		await ctx.send("Me manda uma frase ou palavra e vou criar um enigma a partir disso.")
		return
	
	ETIPO = stripacc(args[0]).upper()
	if ETIPO not in ['FORCA','ANAGRAMA']:
		await ctx.send("O tipo de enigma é inválido.")
		return
	
	await ctx.message.delete()
	PALAVRA = ' '.join(args[1:]).upper()
	if PALAVRA != '-DICA':
		if ETIPO == 'FORCA':
			for i in PALAVRA:
				if i == ' ':
					REVELADO += ' '
				else:
					REVELADO += '-'
		
		elif ETIPO == 'ANAGRAMA':
			REVELADO = ''.join(random.sample(PALAVRA,len(PALAVRA)))
		await ctx.send("Enigma criado! Quero ver vocês resolverem!")
		
		if ETIPO == 'FORCA':
			await ctx.send(f"A palavra/frase contém **{len(PALAVRA.replace(' ',''))} letras.**")
		if ETIPO == 'ANAGRAMA':
			await ctx.send(f"O enigma é **{REVELADO}.**")
	else:
		await ctx.send("Calmae bródi, você não pode fazer isso.")

async def ficha(ctx,*args):
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

async def inventario(ctx,*args):
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
	if len(args) > 0:
		fname = stripacc(args[0]).lower()
	fsys = None
	find = True
	
	if fkey in FSELECT.keys():
		fsys = FSELECT[fkey][1]
		fname = FSELECT[fkey][0]
	
	if fname:
		for i in ('stheno','tormenta','primateria'):
			com.execute(f"SELECT jogador,ouro FROM {i} WHERE id='{fname}'")
			res = com.fetchone()
			if res and len(res) > 0:
				fsys = i
				break
	
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
				if not itm or len(itm) == 0:
					await ctx.send("Não consegui encontrar o item desejado.")
				elif len(itm) > 1:
					resposta = "Opa! Existem mais itens com o mesmo nome:\n"
					for i in itm:
						resposta += f"_{i[0]}: {i[3]}_\n"
					resposta += "Para prosseguir, repita o comando adicionando o nome da tabela."
					await ctx.send(resposta)
				else:
					itm = itm[0]
				
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

async def magias(ctx,*args):
	global FSELECT
	
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()
	fkey = str(ctx.message.author.id)

	#VALIDAR FICHA
	res = None
	fname = None
	if len(args) > 0:
		fname = stripacc(args[0]).lower()
	fsys = None
	find = True
	
	if fkey in FSELECT.keys():
		fsys = FSELECT[fkey][1]
		fname = FSELECT[fkey][0]
	
	if fname:
		for i in ('stheno','tormenta','primateria'):
			com.execute(f"SELECT jogador,ouro FROM {i} WHERE id='{fname}'")
			res = com.fetchone()
			if res and len(res) > 0:
				fsys = i
				break
	
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
						if i[3]:
							txt += f" _-{i[3]}PM_\n"
						else:
							txt += "\n"
					await ctx.send(f"**MAGIAS & HABILIDADES DE {fname.upper()}**\n" + txt)
				else:
					await ctx.send("Você não tem habilidades!")
		else:
			await ctx.send("Essa ficha não é sua, apenas o dono dela pode visualizá-la.")
	else:
		await ctx.send("Eu não consegui encontrar sua ficha.")

	tbl.commit()
	com.close()
	tbl.close()
