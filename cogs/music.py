import discord
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

FFMPEG_PATH = r"C:\Users\gerya\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cola = deque()          # Cola de canciones
        self.actual = None           # Canción actual
        self.loop = False            # Modo repetir
        print("🎵 Cog Música inicializado")

    # ── Buscar canción ──────────────────────────────────
    async def buscar(self, busqueda: str) -> dict:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(YTDL_OPTIONS) as ydl:
            info = await loop.run_in_executor(
                None, lambda: ydl.extract_info(f"ytsearch:{busqueda}", download=False)
            )
            return info["entries"][0]

    # ── Reproducir siguiente en cola ────────────────────
    def reproducir_siguiente(self, ctx):
        if self.loop and self.actual:
            self.cola.appendleft(self.actual)

        if self.cola:
            siguiente = self.cola.popleft()
            self.actual = siguiente
            source = discord.FFmpegPCMAudio(
                siguiente["url"], executable=FFMPEG_PATH, **FFMPEG_OPTIONS
            )
            ctx.voice_client.play(
                source,
                after=lambda e: asyncio.run_coroutine_threadsafe(
                    self.anunciar_siguiente(ctx), self.bot.loop
                )
            )
            asyncio.run_coroutine_threadsafe(
                ctx.send(f"▶️ Reproduciendo: **{siguiente['titulo']}**"),
                self.bot.loop
            )
        else:
            self.actual = None
            asyncio.run_coroutine_threadsafe(
                ctx.send("✅ Cola vacía, no hay más canciones."),
                self.bot.loop
            )

    async def anunciar_siguiente(self, ctx):
        self.reproducir_siguiente(ctx)

    # ── Comandos ────────────────────────────────────────
    @commands.command()
    async def join(self, ctx):
        print(f"🔊 !join por {ctx.author}")
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            await ctx.send(f"🎵 Me uní a **{ctx.author.voice.channel.name}**")
        else:
            await ctx.send("❌ Primero únete a un canal de voz.")

    @commands.command()
    async def leave(self, ctx):
        print(f"🚪 !leave por {ctx.author}")
        if ctx.voice_client:
            self.cola.clear()
            self.actual = None
            await ctx.voice_client.disconnect()
            await ctx.send("👋 Me fui del canal y limpié la cola.")
        else:
            await ctx.send("❌ No estoy en ningún canal de voz.")

    @commands.command()
    async def play(self, ctx, *, busqueda):
        print(f"▶️ !play por {ctx.author} | '{busqueda}'")

        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("❌ No estás en un canal de voz.")

        async with ctx.typing():
            try:
                info = await self.buscar(busqueda)
                cancion = {"url": info["url"], "titulo": info["title"]}
                print(f"  ✅ Encontrado: {cancion['titulo']}")

                if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                    self.cola.append(cancion)
                    await ctx.send(f"➕ Agregado a la cola: **{cancion['titulo']}** (posición {len(self.cola)})")
                else:
                    self.actual = cancion
                    source = discord.FFmpegPCMAudio(
                        cancion["url"], executable=FFMPEG_PATH, **FFMPEG_OPTIONS
                    )
                    ctx.voice_client.play(
                        source,
                        after=lambda e: asyncio.run_coroutine_threadsafe(
                            self.anunciar_siguiente(ctx), self.bot.loop
                        )
                    )
                    await ctx.send(f"▶️ Reproduciendo: **{cancion['titulo']}**")

            except Exception as e:
                print(f"  ❌ Error: {e}")
                await ctx.send(f"❌ Error: `{e}`")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("⏸️ Pausado.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("▶️ Reanudado.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            self.cola.clear()
            self.actual = None
            ctx.voice_client.stop()
            await ctx.send("⏹️ Detenido y cola limpiada.")

    @commands.command()
    async def skip(self, ctx):
        print(f"⏭️ !skip por {ctx.author}")
        if ctx.voice_client and (ctx.voice_client.is_playing() or ctx.voice_client.is_paused()):
            ctx.voice_client.stop()
            await ctx.send("⏭️ Canción saltada.")
        else:
            await ctx.send("❌ No hay nada reproduciéndose.")

    @commands.command()
    async def queue(self, ctx):
        print(f"📋 !cola por {ctx.author}")
        if not self.actual and not self.cola:
            return await ctx.send("📋 La cola está vacía.")

        embed = discord.Embed(title="🎵 Cola de reproducción", color=discord.Color.blurple())

        if self.actual:
            embed.add_field(
                name="▶️ Reproduciendo ahora",
                value=self.actual["titulo"],
                inline=False
            )

        if self.cola:
            lista = "\n".join(
                [f"`{i+1}.` {c['titulo']}" for i, c in enumerate(self.cola)]
            )
            embed.add_field(name="📋 En cola", value=lista, inline=False)
        else:
            embed.add_field(name="📋 En cola", value="No hay más canciones.", inline=False)

        embed.set_footer(text=f"🔁 Repetir: {'Activado' if self.loop else 'Desactivado'}")
        await ctx.send(embed=embed)

    @commands.command()
    async def loop(self, ctx):
        print(f"🔁 !loop por {ctx.author}")
        self.loop = not self.loop
        estado = "✅ activado" if self.loop else "❌ desactivado"
        await ctx.send(f"🔁 Modo repetir {estado}.")

    @commands.command()
    async def clear(self, ctx):
        print(f"🧹 !limpiar_cola por {ctx.author}")
        self.cola.clear()
        await ctx.send("🧹 Cola limpiada.")

async def setup(bot):
    await bot.add_cog(Musica(bot))