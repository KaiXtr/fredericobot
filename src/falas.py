async def frederico(ctx):
    await ctx.send("Me chamaram?")

async def salve(ctx):
    await ctx.send("Salve salve")

async def abraco(ctx):
    await ctx.send("Um forte abraço, galera")

async def gay(ctx):
    await ctx.send("Gay? Quem?")

async def limpaf(ctx):
    await ctx.message.delete()
    for i in await ctx.channel.history(limit=200).flatten():
        if i.author.name == '𝕱𝖗𝖊𝖉𝖊𝖗𝖎𝖈𝖔':
            await i.delete()