import discord
from discord.ext import commands
import anthropic
import os

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        print("🤖 Cog IA inicializado")

    @commands.command()
    async def ask(self, ctx, *, pregunta):
        print(f"🤖 !ask ejecutado por {ctx.author} | Pregunta: '{pregunta}'")
        async with ctx.typing():
            try:
                mensaje = self.client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=500,
                    messages=[{"role": "user", "content": pregunta}]
                )
                respuesta = mensaje.content[0].text
                print(f"  ✅ Respuesta generada ({len(respuesta)} chars)")
                await ctx.send(f"🤖 {respuesta}")
            except Exception as e:
                print(f"  ❌ Error en IA: {e}")
                await ctx.send(f"❌ Error con la IA: `{e}`")

async def setup(bot):
    await bot.add_cog(IA(bot))