import sqlite3

tbl = sqlite3.connect('data.db')
com = tbl.cursor()

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
STHENO = [i[1] for i in STHENO.items()]

com.execute("SELECT * FROM stheno")
res = com.fetchall()
for i in res:
	c = 0
	for j in i:
		if isinstance(STHENO[c],str): t = STHENO[c]
		else: t = STHENO[c][0]
		print(t + ": " + str(j))
		c += 1
	print('\n----------------------------------\n')
tbl.commit()
com.close()
tbl.close()