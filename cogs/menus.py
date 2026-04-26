import discord
from discord.ext import commands

# ── Comandos por categoría ──────────────────────────────
CATEGORIAS = {
    "🎵 Música": {
        "color": discord.Color.blue(),
        "comandos": [
            ("`!join`", "Unirse al canal de voz"),
            ("`!leave`", "Salir del canal de voz"),
            ("`!play <canción>`", "Reproducir o agregar a la cola"),
            ("`!pause`", "Pausar la música"),
            ("`!resume`", "Reanudar la música"),
            ("`!stop`", "Detener y limpiar la cola"),
            ("`!skip`", "Saltar canción"),
            ("`!cola`", "Ver la cola de reproducción"),
            ("`!loop`", "Activar/desactivar repetir"),
            ("`!limpiar_cola`", "Vaciar la cola"),
        ]
    },
    "📥 Descargas": {
        "color": discord.Color.green(),
        "comandos": [
            ("`!descargar <url>`", "Abre el panel de descarga"),
            ("`!descargar_ayuda`", "Muestra los límites y opciones"),
        ]
    },
    "🎮 Diversión": {
        "color": discord.Color.yellow(),
        "comandos": [
            ("`!chiste`", "Chiste aleatorio (ES/EN/Chuck)"),
            ("`!chiste es`", "Chiste en español"),
            ("`!chiste en`", "Chiste en inglés"),
            ("`!chiste chuck`", "Chiste de Chuck Norris"),
            ("`!dado <caras>`", "Tirar un dado"),
            ("`!moneda`", "Lanzar una moneda"),
            ("`!chistoso`", "Menciona a alguien gracioso"),
            ("`!eres_chistoso @usuario`", "Menciona a alguien específico"),
            ("`!quien <pregunta>`", "Elige un miembro aleatorio"),
        ]
    },
    "🎲 Juegos": {
        "color": discord.Color.purple(),
        "comandos": [
            ("`!tor @usuario`", "Verdad o Reto"),
            ("`!ship @u1 @u2`", "Compatibilidad entre dos personas"),
            ("`!versus @u1 @u2`", "Quién ganaría"),
            ("`!insultar @usuario`", "Insulto gracioso"),
            ("`!trivia`", "Pregunta de trivia"),
            ("`!conecta4 @usuario`", "Jugar Conecta 4"),
            ("`!ppt @usuario`", "Piedra Papel Tijeras"),
        ]
    },
    "🔨 Moderación": {
        "color": discord.Color.red(),
        "comandos": [
            ("`!kick @usuario <razón>`", "Expulsar miembro"),
            ("`!ban @usuario <razón>`", "Banear miembro"),
            ("`!limpiar <cantidad>`", "Borrar mensajes"),
        ]
    },
    "🤖 IA": {
        "color": discord.Color.teal(),
        "comandos": [
            ("`!ask <pregunta>`", "Pregúntale a Claude"),
        ]
    },
}

# ── Embed principal ─────────────────────────────────────
def embed_principal():
    embed = discord.Embed(
        title="🤖 Robolillo 2.0 — Ayuda",
        description="Selecciona una categoría para ver sus comandos.",
        color=discord.Color.blurple()
    )
    for categoria in CATEGORIAS:
        total = len(CATEGORIAS[categoria]["comandos"])
        embed.add_field(
            name=categoria,
            value=f"`{total}` comandos",
            inline=True
        )
    embed.set_footer(text="Usa los botones para navegar • 🗑️ para cerrar")
    return embed

# ── Embed de categoría ──────────────────────────────────
def embed_categoria(nombre: str):
    data = CATEGORIAS[nombre]
    embed = discord.Embed(
        title=f"{nombre} — Comandos",
        color=data["color"]
    )
    for cmd, desc in data["comandos"]:
        embed.add_field(name=cmd, value=desc, inline=False)
    embed.set_footer(text="⬅️ Regresar al menú principal • 🗑️ Cerrar")
    return embed

# ── Vista principal ─────────────────────────────────────
class AyudaView(discord.ui.View):
    def __init__(self, autor: discord.Member):
        super().__init__(timeout=60)
        self.autor = autor
        self._agregar_botones()

    def _agregar_botones(self):
        for categoria in CATEGORIAS:
            boton = discord.ui.Button(
                label=categoria,
                style=discord.ButtonStyle.primary,
                row=list(CATEGORIAS.keys()).index(categoria) // 3
            )
            boton.callback = self._hacer_callback(categoria)
            self.add_item(boton)

        cerrar = discord.ui.Button(
            label="🗑️ Cerrar",
            style=discord.ButtonStyle.danger,
            row=2
        )
        cerrar.callback = self.cerrar
        self.add_item(cerrar)

    def _hacer_callback(self, categoria: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.autor.id:
                return await interaction.response.send_message(
                    "❌ Este menú no es tuyo.", ephemeral=True
                )
            await interaction.response.edit_message(
                embed=embed_categoria(categoria),
                view=CategoriaView(self.autor, categoria)
            )
        return callback

    async def cerrar(self, interaction: discord.Interaction):
        if interaction.user.id != self.autor.id:
            return await interaction.response.send_message(
                "❌ Este menú no es tuyo.", ephemeral=True
            )
        await interaction.message.delete()

    async def on_timeout(self):
        try:
            await self.message.delete()
        except:
            pass

# ── Vista de categoría ──────────────────────────────────
class CategoriaView(discord.ui.View):
    def __init__(self, autor: discord.Member, categoria: str):
        super().__init__(timeout=60)
        self.autor = autor
        self.categoria = categoria

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.autor.id:
            await interaction.response.send_message(
                "❌ Este menú no es tuyo.", ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="⬅️ Regresar", style=discord.ButtonStyle.secondary)
    async def regresar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embed=embed_principal(),
            view=AyudaView(self.autor)
        )

    @discord.ui.button(label="🗑️ Cerrar", style=discord.ButtonStyle.danger)
    async def cerrar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()

    async def on_timeout(self):
        try:
            await self.message.delete()
        except:
            pass

# ── Cog ─────────────────────────────────────────────────
class Ayuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("📖 Cog Ayuda inicializado")

    @commands.command(name="ayuda")
    async def ayuda(self, ctx):
        print(f"📖 !ayuda por {ctx.author}")
        view = AyudaView(ctx.author)
        msg = await ctx.send(embed=embed_principal(), view=view)
        view.message = msg

async def setup(bot):
    await bot.add_cog(Ayuda(bot))