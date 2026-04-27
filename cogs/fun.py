import discord
from discord.ext import commands
import random
import aiohttp
import os

JOKEAPI_URL = os.getenv("JOKEAPI_URL", "https://v2.jokeapi.dev/joke")
CHUCKNORRIS_URL = os.getenv("CHUCKNORRIS_URL", "https://api.chucknorris.io/jokes/random")

class Diversion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("🎮 Cog Diversión inicializado")

    # ── Chiste con APIs rotando ─────────────────────────
    @commands.command()
    async def chiste(self, ctx, idioma: str = None):
        print(f"😂 !chiste por {ctx.author} | Idioma: {idioma}")

        if idioma is None:
            idioma = random.choice(["es", "en", "chuck"])

        async with aiohttp.ClientSession() as session:
            try:
                if idioma == "chuck":
                    async with session.get(CHUCKNORRIS_URL) as resp:
                        data = await resp.json()
                        chiste = data["value"]
                        flag = "🇺🇸 Chuck Norris"

                elif idioma == "en":
                    url = f"{JOKEAPI_URL}/Any?lang=en&type=single&blacklistFlags=nsfw,racist,sexist"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if data.get("error"):
                            return await ctx.send("❌ No pude obtener un chiste en inglés.")
                        chiste = data.get("joke") or f"{data['setup']}\n||{data['delivery']}||"
                        flag = "🇺🇸 Inglés"

                else:
                    url = f"{JOKEAPI_URL}/Any?lang=es&type=single"
                    async with session.get(url) as resp:
                        data = await resp.json()
                        if data.get("error"):
                            chistes_local = [
                                "¿Por qué los pájaros vuelan hacia el sur? ¡Porque es muy lejos para caminar!",
                                "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
                                "¿Cómo se despiden los químicos? Ácido un placer.",
                                "¿Qué le dice un techo a otro techo? Techo de menos.",
                            ]
                            return await ctx.send(f"😂 {random.choice(chistes_local)}")
                        chiste = data.get("joke") or f"{data['setup']}\n||{data['delivery']}||"
                        flag = "🇲🇽 Español"

                embed = discord.Embed(
                    description=f"😂 {chiste}",
                    color=discord.Color.yellow()
                )
                embed.set_footer(text=flag)
                await ctx.send(embed=embed)

            except Exception as e:
                print(f"  ❌ Error en chiste: {e}")
                await ctx.send("❌ No pude conectarme a la API de chistes.")

    # ── Dado ────────────────────────────────────────────
    @commands.command()
    async def dado(self, ctx, caras: int = 6):
        if caras < 2:
            return await ctx.send("❌ El dado necesita al menos 2 caras.")
        resultado = random.randint(1, caras)
        await ctx.send(f"🎲 Tiraste un dado de **{caras}** caras: **{resultado}**")

    # ── Moneda ──────────────────────────────────────────
    @commands.command()
    async def moneda(self, ctx):
        resultado = random.choice(["Cara 🪙", "Cruz 🔄"])
        await ctx.send(f"Resultado: **{resultado}**")

    # ── Gay ─────────────────────────────────────────────
    @commands.command()
    async def gay(self, ctx):
        await ctx.message.delete()
        blindwalker = discord.utils.get(ctx.guild.members, name="blindwalker")
        if not blindwalker:
            return
        msg = await ctx.send(f"🎉 {blindwalker.mention} eres guapo 😂")
        await msg.delete(delay=3)

    # ── Chistoso aleatorio ──────────────────────────────
    @commands.command()
    async def chistoso(self, ctx):
        miembros = [m for m in ctx.guild.members if not m.bot]
        if not miembros:
            return await ctx.send("❌ No hay miembros en el servidor.")
        elegido = random.choice(miembros)
        await ctx.send(f"🎉 {elegido.mention} eres chistoso 😂")

    # ── Eres chistoso ───────────────────────────────────
    @commands.command()
    async def eres_chistoso(self, ctx, miembro: discord.Member):
        await ctx.send(f"🎉 {miembro.mention} eres chistoso 😂")

    # ── Quien ───────────────────────────────────────────
    @commands.command()
    async def quien(self, ctx, *, pregunta: str):
        miembros = [m for m in ctx.guild.members if not m.bot]
        elegido = random.choice(miembros)
        await ctx.send(f"🎯 **{pregunta}**\n➡️ {elegido.mention}")

async def setup(bot):
    await bot.add_cog(Diversion(bot))