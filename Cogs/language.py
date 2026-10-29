import discord
from discord.ext import commands
from Utils.translation import t, idiomas_disponibles, IDIOMA_DEFAULT

# ── Almacenamiento en memoria ───────────────────────────
idiomas_servidor = {}   # {guild_id: código}  (ej. "es", "en")
idiomas_usuario  = {}   # {user_id:  código}

def get_idioma(guild_id: int, user_id: int) -> str:
    """El idioma del usuario tiene prioridad sobre el del servidor."""
    if user_id in idiomas_usuario:
        return idiomas_usuario[user_id]
    if guild_id in idiomas_servidor:
        return idiomas_servidor[guild_id]
    return IDIOMA_DEFAULT

class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("🌐 Cog Language inicializado")

    @commands.command(name="language", aliases=["lang", "idioma"])
    async def idioma(self, ctx, lang: str = None, scope: str = "user"):
        id_actual = get_idioma(ctx.guild.id, ctx.author.id)
        disponibles = idiomas_disponibles()

        # Sin argumentos → muestra el idioma actual y los disponibles
        if lang is None:
            embed = discord.Embed(
                title=t(id_actual, "idioma_actual_titulo"),
                description=f"**{disponibles.get(id_actual, id_actual)}**",
                color=discord.Color.blurple()
            )
            embed.add_field(
                name=t(id_actual, "idioma_cambiar"),
                value="\n".join(f"`$language {codigo}` — {nombre}" for codigo, nombre in disponibles.items())
                      + f"\n\n{t(id_actual, 'idioma_servidor_hint')}",
                inline=False
            )
            return await ctx.send(embed=embed)

        lang = lang.lower()
        if lang not in disponibles:
            return await ctx.send(t(id_actual, "idioma_invalido", idiomas=", ".join(f"`{c}`" for c in disponibles)))

        # Cambiar idioma del servidor (solo admins)
        if scope == "server":
            if not ctx.author.guild_permissions.manage_guild:
                return await ctx.send(t(id_actual, "sin_permiso"))
            idiomas_servidor[ctx.guild.id] = lang
            await ctx.send(t(lang, "idioma_servidor"))
        # Cambiar idioma del usuario
        else:
            idiomas_usuario[ctx.author.id] = lang
            await ctx.send(t(lang, "idioma_cambiado"))

async def setup(bot):
    await bot.add_cog(Language(bot))