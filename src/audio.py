from intents import *
import youtube_dl

SFX_PATH = "/home/kaixtr/Music/Defeitos Sonoros/" #"C:\\Users\\kaixtr\\Music\\Defeitos Sonoros\\"

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

async def radio(ctx,*args):
	if len(args) == 0:
		await ctx.send('Escreva _"play"_ e insira um url do YouTube para eu tocar uma música!\n' +
		'Escreva _"pause"_, _"play"_ ou _"pare"_ para eu pausar, continuar ou parar uma música.')
		return
	
	try:
		voice_client = ctx.message.guild.voice_client
	except:
		await ctx.send('Não tem nenhum canal de voz disponível para eu entrar =P')
		return

	if args[0] == 'entrar':
		await entrarvoz(ctx,True)

	elif args[0] == 'sair':
		if voice_client and voice_client.is_connected():
			await voice_client.disconnect()
		else:
			await ctx.send("Oxe, eu já saí!")
	
	elif args[0] == 'play':
		await entrarvoz(ctx)
		if voice_client and voice_client.is_connected():
			if voice_client.is_paused():
				await voice_client.resume()
			else:
				async with ctx.typing():
					filename = await YTDLSource.from_url(args[1], loop=bot.loop)
					voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=f"downloads/{filename}"))
				await ctx.send('**DJ Frederico lançou a braba:** {}'.format(YTDLSource.title))
		else:
			await ctx.send("Eu não estou em nenhum chat de voz.")
	
	elif args[0] == 'pause':
		if voice_client and voice_client.is_connected() and voice_client.is_playing():
			await voice_client.pause()
		else:
			await ctx.send("Eu não estou tocando nada, cara!")
	
	elif args[0] == 'pare':
		if voice_client and voice_client.is_connected() and voice_client.is_playing():
			await voice_client.stop()
		else:
			await ctx.send("Eu não estou tocando nada, cara!")

async def sfx(ctx,*args):
	global SFX_PATH
	
	if len(args) == 0:
		await ctx.send("Digite o nome de um áudio pra eu poder tocar pra você.")
		return
	
	await entrarvoz(ctx)
	voice_client = ctx.message.guild.voice_client
	if voice_client and voice_client.is_connected():
		if voice_client.is_playing():
			voice_client.stop()
		try:
			filename = f"{SFX_PATH}{stripacc(' '.join(args)).lower()}.mp3"
			voice_client.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
		except:
			await ctx.send("Foi mal, não encontrei esse áudio.")