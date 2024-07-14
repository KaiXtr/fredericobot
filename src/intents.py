import discord

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

def getemb(ctx):
	emb = ''
	if len(ctx.message.attachments) > 0:
		if ctx.message.attachments[0].filename[-4:] in ('.jpg','.png','.gif'):
			emb = ctx.message.attachments[0].url
		elif "https://images-ext-1.discordapp.net" in ctx.message.content or "https://tenor.com/view/" in ctx.message.content:
			emb = ctx.message.content
	return emb

itts = discord.Intents.default()
itts.members = True
itts.typing = True
itts.presences = True

DPADRAO = 'd20'
FSELECT = {}
PALAVRA = ''
REVELADO = ''
ETIPO = ''

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
