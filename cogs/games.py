import discord
from discord.ext import commands
import random
import aiohttp
import asyncio
import os
import html

OPENTDB_URL = "https://opentdb.com/api.php"

# ── Categorías OpenTDB ──────────────────────────────────
CATEGORIAS_TRIVIA = {
    "🎮 Videojuegos": 15,
    "🎬 Películas": 11,
    "📺 Series": 14,
    "🎌 Anime": 31,
    "🎵 Música": 12,
    "🔬 Ciencia": 17,
    "🏆 Deportes": 21,
    "🌍 Geografía": 22,
    "🎭 General": 9,
}

# ── Verdades y Retos ────────────────────────────────────
VERDADES = [
    "¿Cuál es tu mayor vergüenza?",
    "¿A quién le tienes más confianza en este servidor?",
    "¿Cuál es la cosa más rara que has googleado?",
    "¿Alguna vez le has mentido a un amigo cercano? ¿Sobre qué?",
    "¿Cuál es tu peor hábito?",
    "¿A quién de aquí mandarías a una isla desierta?",
    "¿Cuál es tu mayor miedo que nadie sabe?",
    "¿Qué es lo más estúpido que has hecho por impresionar a alguien?",
    "¿Cuál es el contacto más raro que tienes en el teléfono?",
    "¿Alguna vez has llorado por una película/serie? ¿Cuál?",
    "¿Cuál es tu opinión real sobre cada persona de este servidor?",
    "¿Qué canción escuchas pero nunca admitirías en público?",
]

RETOS = [
    "Escribe un mensaje de amor a la última persona que te escribió.",
    "Imita a alguien del servidor por 1 minuto.",
    "Manda una foto de tu escritorio ahora mismo.",
    "Escribe tu próximo mensaje solo con emojis.",
    "Confiesa algo que nunca hayas dicho en este servidor.",
    "Manda el meme más raro que tengas guardado.",
    "Escribe un poema de 4 líneas sobre alguien del servidor.",
    "Cambia tu apodo a algo que elija el servidor por 1 hora.",
    "Manda un audio cantando 10 segundos de cualquier canción.",
    "Etiqueta a alguien y dile algo bonito.",
    "Escribe con los codos tu próximo mensaje.",
    "Pon tu canción más escuchada de Spotify.",
]

INSULTOS = [
    "eres tan lento que Google Maps te da indicaciones en pasado.",
    "tienes cara de captcha.",
    "eres la razón por la que los shampoos tienen instrucciones.",
    "si la estupidez fuera un deporte, serías olímpico.",
    "pareces error 404 pero de personalidad.",
    "eres tan aburrido que hasta tu sombra se queda dormida.",
    "tienes más excusas que resultados.",
    "eres como el WiFi del vecino, apareces pero nunca funciona.",
    "si el cerebro fuera gasolina, no tendrías para arrancar la moto.",
    "eres tan predecible que hasta el horóscopo se aburre de ti.",
]

COMENTARIOS_SHIP = [
    "¡Son la pareja perfecta! 💕",
    "Mmm... hay química ahí 👀",
    "Honestamente no sé qué pensar 😂",
    "El universo dice que no 💀",
    "Mejor quédense como amigos 😅",
    "¡Alguien llame a un notario! 💍",
    "Se complementan perfectamente 🔥",
    "Eso sería un desastre épico 😬",
]

CONTEXTOS_VERSUS = [
    "en una pelea de almohadas",
    "en un concurso de comer tacos",
    "en un debate de quién tiene más razón",
    "en un torneo de piedra papel tijeras",
    "en un concurso de chistes malos",
    "escapando de un zombie",
    "en un karaoke sin preparación",
    "cocinando con los ojos vendados",
]

# ── Conecta 4 ───────────────────────────────────────────
VACIO = "⚫"
JUGADOR = "🔴"
BOT_FICHA = "🟡"
FILAS = 6
COLUMNAS = 7

def crear_tablero():
    return [[VACIO] * COLUMNAS for _ in range(FILAS)]

def tablero_a_string(tablero):
    numeros = "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
    resultado = numeros + "\n"
    for fila in tablero:
        resultado += "".join(fila) + "\n"
    return resultado

def colocar_ficha(tablero, columna, ficha):
    for fila in range(FILAS - 1, -1, -1):
        if tablero[fila][columna] == VACIO:
            tablero[fila][columna] = ficha
            return fila
    return -1

def verificar_ganador(tablero, ficha):
    # Horizontal
    for f in range(FILAS):
        for c in range(COLUMNAS - 3):
            if all(tablero[f][c+i] == ficha for i in range(4)):
                return True
    # Vertical
    for f in range(FILAS - 3):
        for c in range(COLUMNAS):
            if all(tablero[f+i][c] == ficha for i in range(4)):
                return True
    # Diagonal /
    for f in range(3, FILAS):
        for c in range(COLUMNAS - 3):
            if all(tablero[f-i][c+i] == ficha for i in range(4)):
                return True
    # Diagonal \
    for f in range(FILAS - 3):
        for c in range(COLUMNAS - 3):
            if all(tablero[f+i][c+i] == ficha for i in range(4)):
                return True
    return False

def columnas_disponibles(tablero):
    return [c for c in range(COLUMNAS) if tablero[0][c] == VACIO]

def movimiento_bot(tablero):
    disponibles = columnas_disponibles(tablero)

    # Intentar ganar
    for col in disponibles:
        temp = [fila[:] for fila in tablero]
        colocar_ficha(temp, col, BOT_FICHA)
        if verificar_ganador(temp, BOT_FICHA):
            return col

    # Bloquear al jugador
    for col in disponibles:
        temp = [fila[:] for fila in tablero]
        colocar_ficha(temp, col, JUGADOR)
        if verificar_ganador(temp, JUGADOR):
            return col

    # Centro o aleatorio
    if 3 in disponibles:
        return 3
    return random.choice(disponibles)


class Juegos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("🎲 Cog Juegos inicializado")

    # ── Piedra Papel Tijeras ────────────────────────────
    @commands.command(name="ppt")
    async def piedra_papel_tijeras(self, ctx):
        print(f"✊ !ppt por {ctx.author}")
        embed = discord.Embed(
            title="✊ Piedra Papel Tijeras",
            description=f"{ctx.author.mention} ¡elige!",
            color=discord.Color.blue()
        )
        view = PPTView(ctx.author)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

    # ── Verdad o Reto ───────────────────────────────────
    @commands.command(name="tor")
    async def verdad_o_reto(self, ctx, miembro: discord.Member = None):
        objetivo = miembro or ctx.author
        print(f"🎭 !tor por {ctx.author} | Objetivo: {objetivo}")
        embed = discord.Embed(
            title="🎭 Verdad o Reto",
            description=f"{objetivo.mention} ¿qué eliges?",
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Pedido por {ctx.author.display_name}")
        view = VerdadORetoView(objetivo)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

    # ── Insultar ────────────────────────────────────────
    @commands.command()
    async def insultar(self, ctx, miembro: discord.Member):
        insulto = random.choice(INSULTOS)
        await ctx.send(f"🔥 {miembro.mention} {insulto}")

    # ── Ship ────────────────────────────────────────────
    @commands.command()
    async def ship(self, ctx, miembro1: discord.Member, miembro2: discord.Member):
        porcentaje = random.randint(0, 100)
        comentario = random.choice(COMENTARIOS_SHIP)
        barra_llena = "💗" * (porcentaje // 10)
        barra_vacia = "🖤" * (10 - porcentaje // 10)
        embed = discord.Embed(title="💕 Shipómetro", color=discord.Color.pink())
        embed.add_field(name="La pareja", value=f"{miembro1.mention} + {miembro2.mention}", inline=False)
        embed.add_field(name=f"Compatibilidad: {porcentaje}%", value=f"{barra_llena}{barra_vacia}", inline=False)
        embed.add_field(name="Veredicto", value=comentario, inline=False)
        await ctx.send(embed=embed)

    # ── Versus ──────────────────────────────────────────
    @commands.command()
    async def versus(self, ctx, miembro1: discord.Member, miembro2: discord.Member):
        ganador = random.choice([miembro1, miembro2])
        contexto = random.choice(CONTEXTOS_VERSUS)
        margen = random.randint(1, 99)
        embed = discord.Embed(
            title="⚔️ Versus",
            description=f"**{miembro1.display_name}** vs **{miembro2.display_name}**",
            color=discord.Color.red()
        )
        embed.add_field(name="Contexto", value=f"_{contexto}_", inline=False)
        embed.add_field(name="🏆 Ganador", value=f"{ganador.mention} gana con **{margen}%** de diferencia", inline=False)
        await ctx.send(embed=embed)

    # ── Trivia ──────────────────────────────────────────
    @commands.command()
    async def trivia(self, ctx):
        print(f"❓ !trivia por {ctx.author}")
        embed = discord.Embed(
            title="❓ Trivia — Elige una categoría",
            color=discord.Color.gold()
        )
        view = TriviaCategoriasView(ctx.author, self.bot)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

    # ── Conecta 4 ───────────────────────────────────────
    @commands.command(name="conecta4")
    async def conecta4(self, ctx):
        print(f"🔴 !conecta4 por {ctx.author}")
        tablero = crear_tablero()
        embed = discord.Embed(
            title="🔴🟡 Conecta 4",
            description=f"{ctx.author.mention} 🔴 vs 🟡 Bot\n\n{tablero_a_string(tablero)}",
            color=discord.Color.red()
        )
        embed.set_footer(text="¡Tú primero! Elige una columna.")
        view = Conecta4View(ctx.author, tablero, self.bot)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg


# ── Vista PPT ───────────────────────────────────────────
class PPTView(discord.ui.View):
    OPCIONES = {"✊ Piedra": "piedra", "📄 Papel": "papel", "✂️ Tijeras": "tijeras"}
    GANA = {"piedra": "tijeras", "papel": "piedra", "tijeras": "papel"}

    def __init__(self, autor):
        super().__init__(timeout=30)
        self.autor = autor
        for label in self.OPCIONES:
            boton = discord.ui.Button(label=label, style=discord.ButtonStyle.primary)
            boton.callback = self._hacer_callback(self.OPCIONES[label])
            self.add_item(boton)

    def _hacer_callback(self, eleccion):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.autor.id:
                return await interaction.response.send_message("❌ No es tu juego.", ephemeral=True)

            bot_eleccion = random.choice(list(self.OPCIONES.values()))
            emojis = {"piedra": "✊", "papel": "📄", "tijeras": "✂️"}

            if eleccion == bot_eleccion:
                resultado = "¡Empate! 🤝"
                color = discord.Color.yellow()
            elif self.GANA[eleccion] == bot_eleccion:
                resultado = "¡Ganaste! 🎉"
                color = discord.Color.green()
            else:
                resultado = "¡Perdiste! 💀"
                color = discord.Color.red()

            embed = discord.Embed(title=f"✊ PPT — {resultado}", color=color)
            embed.add_field(name="Tu elección", value=emojis[eleccion], inline=True)
            embed.add_field(name="Bot eligió", value=emojis[bot_eleccion], inline=True)
            await interaction.response.edit_message(embed=embed, view=None)

        return callback

    async def on_timeout(self):
        try:
            await self.message.edit(content="⏰ Tiempo agotado.", view=None)
        except:
            pass


# ── Vista Verdad o Reto ─────────────────────────────────
class VerdadORetoView(discord.ui.View):
    def __init__(self, objetivo):
        super().__init__(timeout=30)
        self.objetivo = objetivo

    async def interaction_check(self, interaction):
        if interaction.user.id != self.objetivo.id:
            await interaction.response.send_message("❌ Este panel no es para ti.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="🤔 Verdad", style=discord.ButtonStyle.primary)
    async def btn_verdad(self, interaction, button):
        embed = discord.Embed(title="🤔 Verdad", description=random.choice(VERDADES), color=discord.Color.blue())
        embed.set_footer(text=f"Para {self.objetivo.display_name}")
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="😈 Reto", style=discord.ButtonStyle.danger)
    async def btn_reto(self, interaction, button):
        embed = discord.Embed(title="😈 Reto", description=random.choice(RETOS), color=discord.Color.red())
        embed.set_footer(text=f"Para {self.objetivo.display_name}")
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(label="😱 Sorpréndeme", style=discord.ButtonStyle.success)
    async def btn_sorpresa(self, interaction, button):
        if random.choice([True, False]):
            embed = discord.Embed(title="🤔 Verdad", description=random.choice(VERDADES), color=discord.Color.blue())
        else:
            embed = discord.Embed(title="😈 Reto", description=random.choice(RETOS), color=discord.Color.red())
        embed.set_footer(text=f"Para {self.objetivo.display_name}")
        await interaction.response.edit_message(embed=embed, view=None)

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            pass


# ── Vista Trivia Categorías ─────────────────────────────
class TriviaCategoriasView(discord.ui.View):
    def __init__(self, autor, bot):
        super().__init__(timeout=30)
        self.autor = autor
        self.bot = bot
        for i, categoria in enumerate(CATEGORIAS_TRIVIA):
            boton = discord.ui.Button(
                label=categoria,
                style=discord.ButtonStyle.primary,
                row=i // 3
            )
            boton.callback = self._hacer_callback(categoria)
            self.add_item(boton)

    def _hacer_callback(self, categoria):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.autor.id:
                return await interaction.response.send_message("❌ No es tu trivia.", ephemeral=True)
            await interaction.response.edit_message(
                content="🔍 Buscando pregunta...", embed=None, view=None
            )
            await self._cargar_pregunta(interaction, categoria)
        return callback

    async def _cargar_pregunta(self, interaction, categoria):
        cat_id = CATEGORIAS_TRIVIA[categoria]
        url = f"{OPENTDB_URL}?amount=1&category={cat_id}&type=multiple"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        if data["response_code"] != 0:
            return await interaction.edit_original_response(content="❌ No pude obtener una pregunta.")

        pregunta_data = data["results"][0]
        pregunta = html.unescape(pregunta_data["question"])
        correcta = html.unescape(pregunta_data["correct_answer"])
        incorrectas = [html.unescape(x) for x in pregunta_data["incorrect_answers"]]
        opciones = incorrectas + [correcta]
        random.shuffle(opciones)

        embed = discord.Embed(
            title=f"❓ Trivia — {categoria}",
            description=f"**{pregunta}**",
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Dificultad: {pregunta_data['difficulty'].capitalize()}")

        view = TriviaRespuestaView(self.autor, opciones, correcta)
        msg = await interaction.edit_original_response(content=None, embed=embed, view=view)
        view.message = msg

    async def on_timeout(self):
        try:
            await self.message.edit(content="⏰ Tiempo agotado.", embed=None, view=None)
        except:
            pass


# ── Vista Trivia Respuesta ──────────────────────────────
class TriviaRespuestaView(discord.ui.View):
    def __init__(self, autor, opciones, correcta):
        super().__init__(timeout=20)
        self.autor = autor
        self.correcta = correcta
        for opcion in opciones:
            boton = discord.ui.Button(label=opcion[:80], style=discord.ButtonStyle.secondary)
            boton.callback = self._hacer_callback(opcion)
            self.add_item(boton)

    def _hacer_callback(self, opcion):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.autor.id:
                return await interaction.response.send_message("❌ No es tu trivia.", ephemeral=True)

            if opcion == self.correcta:
                embed = discord.Embed(
                    title="✅ ¡Correcto!",
                    description=f"La respuesta era: **{self.correcta}**",
                    color=discord.Color.green()
                )
            else:
                embed = discord.Embed(
                    title="❌ ¡Incorrecto!",
                    description=f"La respuesta correcta era: **{self.correcta}**",
                    color=discord.Color.red()
                )
            await interaction.response.edit_message(embed=embed, view=None)
        return callback

    async def on_timeout(self):
        try:
            embed = discord.Embed(
                title="⏰ Tiempo agotado",
                description=f"La respuesta era: **{self.correcta}**",
                color=discord.Color.orange()
            )
            await self.message.edit(embed=embed, view=None)
        except:
            pass


# ── Vista Conecta 4 ─────────────────────────────────────
class Conecta4View(discord.ui.View):
    def __init__(self, autor, tablero, bot):
        super().__init__(timeout=120)
        self.autor = autor
        self.tablero = tablero
        self.bot_discord = bot
        self._agregar_botones()

    def _agregar_botones(self):
        self.clear_items()
        disponibles = columnas_disponibles(self.tablero)
        for col in range(COLUMNAS):
            boton = discord.ui.Button(
                label=str(col + 1),
                style=discord.ButtonStyle.primary if col in disponibles else discord.ButtonStyle.secondary,
                disabled=col not in disponibles,
                row=0
            )
            boton.callback = self._hacer_callback(col)
            self.add_item(boton)

        rendirse = discord.ui.Button(label="🏳️ Rendirse", style=discord.ButtonStyle.danger, row=1)
        rendirse.callback = self.rendirse
        self.add_item(rendirse)

    def _hacer_callback(self, col):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.autor.id:
                return await interaction.response.send_message("❌ No es tu juego.", ephemeral=True)

            # Turno del jugador
            colocar_ficha(self.tablero, col, JUGADOR)

            if verificar_ganador(self.tablero, JUGADOR):
                embed = discord.Embed(
                    title="🎉 ¡Ganaste!",
                    description=tablero_a_string(self.tablero),
                    color=discord.Color.green()
                )
                return await interaction.response.edit_message(embed=embed, view=None)

            if not columnas_disponibles(self.tablero):
                embed = discord.Embed(
                    title="🤝 ¡Empate!",
                    description=tablero_a_string(self.tablero),
                    color=discord.Color.yellow()
                )
                return await interaction.response.edit_message(embed=embed, view=None)

            # Turno del bot
            col_bot = movimiento_bot(self.tablero)
            colocar_ficha(self.tablero, col_bot, BOT_FICHA)

            if verificar_ganador(self.tablero, BOT_FICHA):
                embed = discord.Embed(
                    title="💀 ¡Perdiste!",
                    description=tablero_a_string(self.tablero),
                    color=discord.Color.red()
                )
                return await interaction.response.edit_message(embed=embed, view=None)

            if not columnas_disponibles(self.tablero):
                embed = discord.Embed(
                    title="🤝 ¡Empate!",
                    description=tablero_a_string(self.tablero),
                    color=discord.Color.yellow()
                )
                return await interaction.response.edit_message(embed=embed, view=None)

            # Actualizar tablero
            self._agregar_botones()
            embed = discord.Embed(
                title="🔴🟡 Conecta 4",
                description=f"{self.autor.mention} 🔴 vs 🟡 Bot\n\n{tablero_a_string(self.tablero)}",
                color=discord.Color.red()
            )
            embed.set_footer(text="¡Tu turno!")
            await interaction.response.edit_message(embed=embed, view=self)

        return callback

    async def rendirse(self, interaction: discord.Interaction):
        if interaction.user.id != self.autor.id:
            return await interaction.response.send_message("❌ No es tu juego.", ephemeral=True)
        embed = discord.Embed(
            title="🏳️ Te rendiste",
            description=tablero_a_string(self.tablero),
            color=discord.Color.grays()
        )
        await interaction.response.edit_message(embed=embed, view=None)

    async def on_timeout(self):
        try:
            await self.message.edit(content="⏰ Juego expirado.", view=None)
        except:
            pass


async def setup(bot):
    await bot.add_cog(Juegos(bot))