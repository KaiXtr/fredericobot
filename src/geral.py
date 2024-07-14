import random
import sqlite3
from intents import *

async def falef(ctx,*args):
	if args:
		resposta:str = ' '.join(args)
	else:
		falas:str = (
			'Concordo.',
			'Ah, nada ver isso daí!',
			'Pode ser que sim, pode ser que não.',
			'Pokas idéias, truta'
			)
		resposta:str = random.choice(falas)
	
	await ctx.send(resposta,tts=True)
	
async def calc(ctx,*args):
	if args:
		resposta:str = ' '.join(args)
		valor = resposta.replace('x','*')
		valor = valor.replace('^','**')
		resposta = f'_{resposta} = {eval(valor)}_'
	else: resposta = '...calcular o quê?'

	await ctx.send(resposta)

async def rolar(ctx,*args):
	global FSELECT
	global DPADRAO

	if len(args) == 0:
		await ctx.send("Pra rolar um dado, escreva nesses formatos: _4,d8,1d6,2d20+2 etc._\n" +\
			"Ah! E você também pode rolar o dado de dano de uma arma se escrever o nome dela!")
		return
	
	dado = ''
	itm = None
	kys = [i for i in STHENO.keys()] + [i for i in PRIMATERIA.keys()]

	if len(args) == 2:
		bonus = int(args[1])
	
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
					if int(res[0]) < 0:
						dado = DPADRAO.join(res[0])
					else:
						dado = DPADRAO.join("+" + res[0])
			else:
				await ctx.send("Não encontrei nenhum teste com esse nome.")
		else:
			await ctx.send("Nenhuma ficha foi selecionada.")

		tbl.commit()
		com.close()
		tbl.close()
	
	#ROLAR DADO NORMAL
	elif args[0][0] in 'Dd0123456789':
		dado = args[0].lower()
	
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
				if palavra.lower() in ('dano:','cura:','mana:'):
					find = True
					itm = res
				if i in ('|',',','.'):
					find = None
					palavra = ''

				if find and i != ' ':
					dado += i
				else:
					palavra += i
		
		tbl.commit()
		com.close()
		tbl.close()

	if dado and dado != '':
		#PROCESSAR DADOS
		resultado = 0
		maxres = 0
		lst = dado.split('-')
		for i in range(len(lst)):
			if i > 0:
				lst[i] = "-" + lst[i]
			
			for j in lst[i].split('+'):
				dd = j.split('d')
				if dd[0] == '':
					dd[0] = '1'
				
				if len(dd) == 2:
					for v in range(int(dd[0])):
						resultado += random.randint(1,int(dd[1]))
					maxres += int(dd[0]) * int(dd[1])
				else:
					resultado += int(dd[0])

		#COMENTAR E ENVIAR RESPOSTA
		if resultado >= maxres:
			comentario = random.choice(('em cheio!','na mosca!'))
		elif resultado <= 1:
			comentario = random.choice(('que azar!','ai caramba!','putzgrila!','se deu mal!'))
		elif resultado > int(maxres/2):
			comentario = random.choice(('boa!','isso aí!','legal!'))
		elif resultado == int(maxres/2):
			comentario = random.choice(('nada mal.','é.','ok.','beleza.'))
		elif resultado < int(maxres/2):
			comentario = random.choice(('eita...','vish...','putz...'))

		await ctx.send(f'**{dado} = **{resultado}, {comentario}')

async def setf(ctx,*args):
	global DPADRAO
	if len(args) > 0:
		if args[0] in ('-dado','-dice'):
			DPADRAO = args[1].lower()

async def ajuda(ctx,*args):
	await ctx.send("O que eu sei fazer? Sei fazer um monte de coisas, bebê!\n" +
		"**falef:** vou dizer qualquer coisa que digitar.\n" +
		"**calc:** vou calcular qualquer conta matemática que digitar.\n" +
		"**rolar:** vou rolar dados por você.\n\n" +
		
		"**lembref:** se precisar lembrar de algo, vou lembrar pra você.\n" +
		"**esquecaf:** se quiser que eu esqueça, eu faço também.\n" +
		"**lembretes:** mostro todos os lembretes pra você.\n\n" +
		
		"**addf:** crio uma tabela com itens e adiciono ele.\n" +
		"**renomearf:** troco o nome de uma tabela ou item.\n" +
		"**apagarf:** apago qualquer tabela ou item.\n" +
		"**tabelaf:** mostro uma tabela.\n\n" +
		
		"**enigmaf:** crio um quebra-cabeça de palavras para você resolver.\n" +
		"**fichaf:** mostro fichas de personagem salvas por você.\n" +
		"**invf:** gerencio os itens de seu personagem.\n" +
		"**magf:** gerencio magias e habilidades de seu personagem.\n\n" +
		
		"**radio:** toco músicas para animar a garotada.\n" +
		"**sfx:** por último, mas não menos importante, também sou sonoplasta do ratinho.\n")