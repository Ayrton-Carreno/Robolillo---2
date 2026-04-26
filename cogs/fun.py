import discord
from discord.ext import commands
import random

class Diversion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("🎮 Cog Diversión inicializado")

    @commands.command()
    async def hola(self, ctx):
        print(f"👋 !hola ejecutado por {ctx.author} en #{ctx.channel.name}")
        await ctx.send(f"¡Hola, {ctx.author.mention}! 👋")

    @commands.command()
    async def dado(self, ctx, caras: int = 6):
        print(f"🎲 !dado ejecutado por {ctx.author} con {caras} caras")
        resultado = random.randint(1, caras)
        await ctx.send(f"🎲 Tiraste un dado de {caras} caras y salió: **{resultado}**")

    @commands.command()
    async def moneda(self, ctx):
        print(f"🪙 !moneda ejecutado por {ctx.author}")
        resultado = random.choice(["Cara 🪙", "Cruz 🔄"])
        await ctx.send(f"Resultado: **{resultado}**")

    @commands.command()
    async def chiste(self, ctx):
        print(f"😂 !chiste ejecutado por {ctx.author}")
        chistes = [
            "¿Por qué los pájaros vuelan hacia el sur? ¡Porque es muy lejos para caminar!",
            "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
            "¿Cómo se despiden los químicos? Ácido un placer.", 
        ]
        await ctx.send(random.choice(chistes))

    @commands.command()
    async def gay(self, ctx):
        blindwalker = discord.utils.get(ctx.guild.members, name="blindwalker")
        if not blindwalker:
            return await ctx.send("❌ No encontré a mobleminik en el servidor.")
        print(f"😂 !gay por {ctx.author}")
        await ctx.send(f"🎉 {blindwalker.mention} eres putisimo😂")

async def setup(bot):
    await bot.add_cog(Diversion(bot))