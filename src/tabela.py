import sqlite3

async def adicionar(ctx,*args):
	if len(args) == 0:
		await ctx.send("Não sabe adicionar um item?\n" +
			"Se liga: é só escrever em qual tabela quer adicionar, o nome do item, o preço e as outras coisinhas\n" +
			"Tipo o dano da arma, o bônus de CA, sei lá... mas só se quiser, pode deixar vazio.")
	
	elif len(args) == 1:
		await ctx.send("Você escreveu a tabela onde vai colocar, mas ainda falta o nome, o preço e o resto.")
	
	elif len(args) == 2:
		await ctx.send("Você escreveu a tabela e o nome do item, mas falta o preço. O resto é opcional.")
	
	elif len(args) >= 3:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()
		txt = ''
		if len(args) > 3:
			txt = ' '.join(args[3:])

		com.execute("CREATE TABLE IF NOT EXISTS items (tabela text,nome text,preco text,propriedades text)")
		com.execute(f"DELETE FROM items WHERE tabela='{args[0]}' AND nome='{args[1]}'")
		com.execute(f"INSERT INTO items VALUES ('{args[0]}','{args[1]}','{args[2]}','{txt}')")

		tbl.commit()
		com.close()
		tbl.close()
		
		await ctx.send(f"**{args[1]}** foi adicionado na tabela **{args[0]}**!")

async def renomear(ctx,*args):
	if len(args) == 0:
		await ctx.send(f"Quer renomear uma tabela ou um item?")
	elif len(args) == 1:
		await ctx.send(f"Digite um nome antigo e depois o nome novo")
	elif len(args) == 2:
		await ctx.send(f"Digite um nome antigo e depois o nome novo")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		if args[0].lower() == 'tabela':
			com.execute(f"UPDATE items SET tabela='{args[2]}' WHERE tabela='{args[1]}'")
		if args[0].lower() == 'item':
			com.execute(f"UPDATE items SET nome='{args[2]}' WHERE nome='{args[1]}'")
		await ctx.send("Já mudei o nome!")

		tbl.commit()
		com.close()
		tbl.close()
		
async def apagar(ctx,*args):
	if len(args) == 0:
		await ctx.send("Se quiser tirar uma tabela, digite só o nome dela.\n" +
			"Mas se quiser tirar apenas um item dela, escreva a tabela e depois o nome do item.")
	else:
		tbl = sqlite3.connect('data.db')
		com = tbl.cursor()

		if len(args) == 2:
			com.execute(f"DELETE FROM items WHERE tabela='{args[0]}' AND nome='{args[1]}'")
		else:
			com.execute(f"DELETE FROM items WHERE tabela='{args[0]}'")
		
		await ctx.send("Sumiu para sempre, papai!")

		tbl.commit()
		com.close()
		tbl.close()
		
async def mostrar(ctx,*args):
	tbl = sqlite3.connect('data.db')
	com = tbl.cursor()
	
	if len(args) == 0:
		com.execute(f"SELECT DISTINCT tabela FROM items ORDER BY tabela")
		res = com.fetchall()
		
		if res and len(res) > 0:
			if len(res) == 1:
				resposta = '**Você tem apenas uma tabela:**\n'
			else:
				resposta = '**Estas são as suas tabelas:**\n'
			for i in res:
				resposta += f"• _{i[0]}_\n"
			await ctx.send(resposta)
		else:
			await ctx.send("Você ainda não criou nenhuma tabela.")
		return
	
	if len(args) == 2:
		com.execute(f"SELECT * FROM items WHERE nome='{args[1]}' ORDER BY nome")
	else:
		com.execute(f"SELECT * FROM items WHERE tabela='{args[0]}' ORDER BY nome")
	
	res = com.fetchall()
	if res:
		await ctx.send(f"**{args[0]}**")
		txt = ''
		for i in res:
			if len(txt) > 1500:
				await ctx.send(txt)
				txt = ''
			if i[3]:
				txt += f"**{i[1]}:** {i[2]}$ | _{i[3]}_\n"
			else:
				txt += f"**{i[1]}:** {i[2]}$\n"
		await ctx.send(txt)
	else:
		await ctx.send("Eu não consegui encontrar nada...")
	
	tbl.commit()
	com.close()
	tbl.close()
