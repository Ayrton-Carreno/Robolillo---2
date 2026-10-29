import discord
from discord.ext import commands
from Utils.translation import t

# ── Comandos por categoría ──────────────────────────────
# (comando, argumentos) → la descripción sale de Utils/lang/<idioma>.json: "cmd_<comando>"
CATEGORIAS = {
    "cat_musica": {
        "color": discord.Color.blue(),
        "comandos": [
            ("join", ""),
            ("leave", ""),
            ("play", "<song>"),
            ("pause", ""),
            ("resume", ""),
            ("stop", ""),
            ("skip", ""),
            ("queue", ""),
            ("loop", ""),
            ("clear", ""),
        ]
    },
    "cat_descargas": {
        "color": discord.Color.green(),
        "comandos": [
            ("download", "<url>"),
        ]
    },
    "cat_diversion": {
        "color": discord.Color.yellow(),
        "comandos": [
            ("joke", "[es|en|chuck]"),
            ("dice", "[sides]"),
            ("coin", ""),
            ("funny", ""),
            ("youre_funny", "@user"),
            ("who", "<question>"),
        ]
    },
    "cat_juegos": {
        "color": discord.Color.purple(),
        "comandos": [
            ("tor", "[@user]"),
            ("ship", "@user1 @user2"),
            ("versus", "@user1 @user2"),
            ("insult", "@user"),
            ("trivia", ""),
            ("connect4", ""),
            ("rps", ""),
        ]
    },
    "cat_moderacion": {
        "color": discord.Color.red(),
        "comandos": [
            ("kick", "@user [reason]"),
            ("ban", "@user [reason]"),
            ("purge", "[amount]"),
        ]
    },
    "cat_idioma": {
        "color": discord.Color.blurple(),
        "comandos": [
            ("language", "[es|en] [server]"),
        ]
    },
    "cat_ia": {
        "color": discord.Color.teal(),
        "comandos": [
            ("ask", "<question>"),
        ]
    },
}

def uso(comando: str, args: str) -> str:
    return f"`${comando} {args}`" if args else f"`${comando}`"

def buscar_comando(nombre: str):
    for categoria, data in CATEGORIAS.items():
        for comando, args in data["comandos"]:
            if comando == nombre:
                return categoria, comando, args
    return None

# ── Embed principal ─────────────────────────────────────
def embed_principal(idioma: str):
    embed = discord.Embed(
        title=t(idioma, "ayuda_titulo"),
        description=f"{t(idioma, 'ayuda_desc')}\n{t(idioma, 'ayuda_detalle_hint')}",
        color=discord.Color.blurple()
    )
    for categoria, data in CATEGORIAS.items():
        embed.add_field(
            name=t(idioma, categoria),
            value=t(idioma, "ayuda_num_comandos", total=len(data["comandos"])),
            inline=True
        )
    embed.set_footer(text=t(idioma, "ayuda_footer"))
    return embed

# ── Embed de categoría ──────────────────────────────────
def embed_categoria(idioma: str, categoria: str):
    data = CATEGORIAS[categoria]
    embed = discord.Embed(
        title=t(idioma, "ayuda_comandos_titulo", categoria=t(idioma, categoria)),
        color=data["color"]
    )
    for comando, args in data["comandos"]:
        embed.add_field(name=uso(comando, args), value=t(idioma, f"cmd_{comando}"), inline=False)
    embed.set_footer(text=t(idioma, "comandos_footer"))
    return embed

# ── Embed de un comando ─────────────────────────────────
def embed_comando(idioma: str, cmd: commands.Command):
    encontrado = buscar_comando(cmd.name)
    categoria, comando, args = encontrado if encontrado else (None, cmd.name, "")
    embed = discord.Embed(
        title=f"${comando}",
        description=t(idioma, f"cmd_{comando}"),
        color=CATEGORIAS[categoria]["color"] if categoria else discord.Color.blurple()
    )
    embed.add_field(name=t(idioma, "ayuda_uso"), value=uso(comando, args), inline=False)
    if cmd.aliases:
        embed.add_field(
            name=t(idioma, "ayuda_alias"),
            value=", ".join(f"`${a}`" for a in cmd.aliases),
            inline=False
        )
    if categoria:
        embed.set_footer(text=t(idioma, categoria))
    return embed

# ── Vista principal ─────────────────────────────────────
class AyudaView(discord.ui.View):
    def __init__(self, autor: discord.Member, idioma: str):
        super().__init__(timeout=60)
        self.autor = autor
        self.idioma = idioma
        self.message = None
        self._agregar_botones()

    def _agregar_botones(self):
        for i, categoria in enumerate(CATEGORIAS):
            boton = discord.ui.Button(
                label=t(self.idioma, categoria),
                style=discord.ButtonStyle.primary,
                row=i // 3
            )
            boton.callback = self._hacer_callback(categoria)
            self.add_item(boton)

        cerrar = discord.ui.Button(
            label=t(self.idioma, "btn_cerrar"),
            style=discord.ButtonStyle.danger,
            row=2
        )
        cerrar.callback = self.cerrar
        self.add_item(cerrar)

    def _hacer_callback(self, categoria: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.autor.id:
                return await interaction.response.send_message(
                    t(self.idioma, "menu_no_tuyo"), ephemeral=True
                )
            vista = CategoriaView(self.autor, self.idioma, interaction.message)
            await interaction.response.edit_message(
                embed=embed_categoria(self.idioma, categoria),
                view=vista
            )
        return callback

    async def cerrar(self, interaction: discord.Interaction):
        if interaction.user.id != self.autor.id:
            return await interaction.response.send_message(
                t(self.idioma, "menu_no_tuyo"), ephemeral=True
            )
        await interaction.message.delete()

    async def on_timeout(self):
        try:
            await self.message.delete()
        except:
            pass

# ── Vista de categoría ──────────────────────────────────
class CategoriaView(discord.ui.View):
    def __init__(self, autor: discord.Member, idioma: str, message=None):
        super().__init__(timeout=60)
        self.autor = autor
        self.idioma = idioma
        self.message = message
        self.regresar.label = t(idioma, "btn_regresar")
        self.cerrar.label = t(idioma, "btn_cerrar")

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.autor.id:
            await interaction.response.send_message(
                t(self.idioma, "menu_no_tuyo"), ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="⬅️ Regresar", style=discord.ButtonStyle.secondary)
    async def regresar(self, interaction: discord.Interaction, button: discord.ui.Button):
        vista = AyudaView(self.autor, self.idioma)
        vista.message = interaction.message
        await interaction.response.edit_message(
            embed=embed_principal(self.idioma),
            view=vista
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

    @commands.command(name="help", aliases=["ayuda"])
    async def help(self, ctx, comando: str = None):
        print(f"📖 $help por {ctx.author} | Comando: {comando}")
        # Import aquí: load_extension crea su propio módulo, así se usan los mismos diccionarios del cog
        from Cogs.language import get_idioma
        idioma = get_idioma(ctx.guild.id if ctx.guild else 0, ctx.author.id)

        # $help <comando> → detalles de un comando
        if comando:
            cmd = self.bot.get_command(comando.lstrip("$").lower())
            if cmd is None or (buscar_comando(cmd.name) is None and cmd.name != "help"):
                return await ctx.send(t(idioma, "ayuda_no_encontrado", comando=comando))
            return await ctx.send(embed=embed_comando(idioma, cmd))

        view = AyudaView(ctx.author, idioma)
        msg = await ctx.send(embed=embed_principal(idioma), view=view)
        view.message = msg

async def setup(bot):
    await bot.add_cog(Ayuda(bot))
