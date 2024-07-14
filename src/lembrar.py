import sqlite3
import random
import discord
from intents import *

async def lembre(ctx,*args):
	if len(args) == 0:
		await ctx.send("Para me fazer me lembrar de alguma coisa, dê um nome ao lembrete e depois escreva qualquer mensagem!\n" + 
			"Lembrando que, se você me mandar uma imagem, eu também vou guardar ela comigo!")
	elif len(args) == 1:
		await ctx.send("Você deu um marcador ao lembrete, mas não me disse do que eu devo me lembrar!")
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
	else:
		await ctx.send("Você pode dar o nome que quiser para seu marcador, menos esse nome aqui, ok?")
		
async def esqueca(ctx,*args):
	if len(args) == 0:
		await ctx.send("Se quiser que eu me esqueça de um lembrete, escreva o marcador que deu para ele.")
		return
	
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()

	if args[0] == '-tudo':
		com.execute("DELETE FROM lembretes")
	else:
		com.execute(f"DELETE FROM lembretes WHERE id='{args[0]}'")

	ff = (
		'Hã? Esquecer o quê?',
		'Me esqueci de alguma coisa?',
		'Isso nunca passou pela minha cabeça.',
		'Vou fingir que não vi nada.'
		)
	await ctx.send(random.choice(ff))

	tbl.commit()
	com.close()
	tbl.close()

async def lembretes(ctx,*args):
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()

	com.execute("SELECT * FROM lembretes ORDER BY id")
	res = com.fetchall()
	if res:
		await ctx.send("**Estes são os seus lembretes:**")
		for i in res:
			await ctx.send(f'{i[0]}: {i[1]}')
			if i[2] != '':
				emb = discord.Embed()
				emb.set_image(url=i[2])
				await ctx.send(embed=emb)
	else:
		ff = (
			"Você não me pediu para me lembrar de nada.",
			"Que lembretes?",
			"Você não tem lembretes."
			)
		await ctx.send(random.choice(ff))

	tbl.commit()
	com.close()
	tbl.close()