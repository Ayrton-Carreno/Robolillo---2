import discord
from discord.ext import commands
import yt_dlp
import os
import asyncio

MAX_TAMANIO_MB = 25
MAX_DURACION_SEG = 600
CARPETA_DESCARGAS = "descargas"

def obtener_opciones(modo: str, calidad: str) -> dict:
    formato = {
        "720":   "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]",
        "1080":  "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
        "audio": "bestaudio[ext=m4a]/bestaudio",
    }
    return {
        "format": formato.get(calidad, formato["720"]),
        "outtmpl": f"{CARPETA_DESCARGAS}/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": "mp4" if modo == "video" else None,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }] if modo == "audio" else [],
    }

# ── Panel de botones ────────────────────────────────────
class PanelDescarga(discord.ui.View):
    def __init__(self, cog, ctx, url):
        super().__init__(timeout=30)
        self.cog = cog
        self.ctx = ctx
        self.url = url
        self.modo = None
        self.calidad = None

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(content="⏰ Panel expirado.", embed=None, view=self)

    # ── Fila 1: Modo ───────────────────────────────────
    @discord.ui.button(label="🎬 Video", style=discord.ButtonStyle.primary, row=0)
    async def btn_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.modo = "video"
        await interaction.response.edit_message(
            embed=self._embed_calidad(),
            view=self._vista_calidad()
        )

    @discord.ui.button(label="🎵 Solo Audio", style=discord.ButtonStyle.success, row=0)
    async def btn_audio(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.modo = "audio"
        self.calidad = "audio"
        await interaction.response.edit_message(
            embed=self._embed_advertencia_audio(),
            view=self._vista_confirmar()
        )

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.danger, row=0)
    async def btn_cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Descarga cancelada.", embed=None, view=None)

    # ── Embed inicial ───────────────────────────────────
    def embed_inicial(self):
        embed = discord.Embed(
            title="📥 ¿Qué quieres descargar?",
            description=f"🔗 `{self.url[:60]}...`" if len(self.url) > 60 else f"🔗 `{self.url}`",
            color=discord.Color.blurple()
        )
        embed.add_field(name="⚠️ Límites", value=f"📦 Máx: **{MAX_TAMANIO_MB} MB**\n⏱️ Máx: **{MAX_DURACION_SEG // 60} min**", inline=False)
        embed.set_footer(text="Este panel expira en 30 segundos.")
        return embed

    # ── Embed selección calidad ─────────────────────────
    def _embed_calidad(self):
        embed = discord.Embed(
            title="🎬 Selecciona la calidad del video",
            color=discord.Color.blurple()
        )
        embed.add_field(name="⚠️ Límites", value=f"📦 Máx: **{MAX_TAMANIO_MB} MB**\n⏱️ Máx: **{MAX_DURACION_SEG // 60} min**", inline=False)
        embed.set_footer(text="Este panel expira en 30 segundos.")
        return embed

    def _vista_calidad(self):
        view = discord.ui.View(timeout=30)

        async def btn_720(interaction, button=None):
            self.calidad = "720"
            await interaction.response.edit_message(content="⬇️ Iniciando descarga...", embed=None, view=None)
            await self.cog.ejecutar_descarga(self.ctx, self.modo, self.calidad, self.url, interaction.message)

        async def btn_1080(interaction, button=None):
            self.calidad = "1080"
            await interaction.response.edit_message(content="⬇️ Iniciando descarga...", embed=None, view=None)
            await self.cog.ejecutar_descarga(self.ctx, self.modo, self.calidad, self.url, interaction.message)

        async def btn_cancelar(interaction, button=None):
            await interaction.response.edit_message(content="❌ Descarga cancelada.", embed=None, view=None)

        b720 = discord.ui.Button(label="📺 720p", style=discord.ButtonStyle.primary)
        b720.callback = btn_720
        b1080 = discord.ui.Button(label="🖥️ 1080p", style=discord.ButtonStyle.primary)
        b1080.callback = btn_1080
        bcancel = discord.ui.Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
        bcancel.callback = btn_cancelar

        view.add_item(b720)
        view.add_item(b1080)
        view.add_item(bcancel)
        return view

    # ── Embed advertencia audio ─────────────────────────
    def _embed_advertencia_audio(self):
        embed = discord.Embed(
            title="🎵 Solo Audio — MP3",
            description="Se extraerá únicamente el audio en formato MP3.",
            color=discord.Color.green()
        )
        embed.add_field(
            name="⚠️ Advertencias",
            value=(
                f"📦 Tamaño máximo: **{MAX_TAMANIO_MB} MB**\n"
                f"⏱️ Duración máxima: **{MAX_DURACION_SEG // 60} minutos**\n"
                f"💾 El archivo se enviará directo por Discord."
            ),
            inline=False
        )
        embed.set_footer(text="¿Confirmas la descarga?")
        return embed

    def _vista_confirmar(self):
        view = discord.ui.View(timeout=30)

        async def btn_confirmar(interaction, button=None):
            await interaction.response.edit_message(content="⬇️ Iniciando descarga...", embed=None, view=None)
            await self.cog.ejecutar_descarga(self.ctx, self.modo, self.calidad, self.url, interaction.message)

        async def btn_cancelar(interaction, button=None):
            await interaction.response.edit_message(content="❌ Descarga cancelada.", embed=None, view=None)

        bconf = discord.ui.Button(label="✅ Confirmar", style=discord.ButtonStyle.success)
        bconf.callback = btn_confirmar
        bcancel = discord.ui.Button(label="❌ Cancelar", style=discord.ButtonStyle.danger)
        bcancel.callback = btn_cancelar

        view.add_item(bconf)
        view.add_item(bcancel)
        return view


class Descargas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs(CARPETA_DESCARGAS, exist_ok=True)
        print("📥 Cog Descargas inicializado")

    def validar_info(self, info: dict):
        duracion = info.get("duration", 0)
        print(f"  ⏱️ Duración: {duracion}s | Límite: {MAX_DURACION_SEG}s")
        if duracion > MAX_DURACION_SEG:
            return f"❌ El video dura **{duracion // 60} min**, el límite es {MAX_DURACION_SEG // 60} min."

        tamanio = info.get("filesize") or info.get("filesize_approx") or 0
        tamanio_mb = tamanio / (1024 * 1024)
        print(f"  📦 Tamaño estimado: {tamanio_mb:.1f} MB | Límite: {MAX_TAMANIO_MB} MB")
        if tamanio_mb > MAX_TAMANIO_MB:
            return f"❌ El archivo pesa aprox. **{tamanio_mb:.1f} MB**, el límite es {MAX_TAMANIO_MB} MB."

        return None

    @commands.command(name="download")
    async def descargar(self, ctx, *, url: str):
        print(f"📥 !descargar | {ctx.author} | URL: {url}")
        panel = PanelDescarga(self, ctx, url)
        msg = await ctx.send(embed=panel.embed_inicial(), view=panel)
        panel.message = msg

    async def ejecutar_descarga(self, ctx, modo, calidad, url, msg):
        opciones = obtener_opciones(modo, calidad)
        loop = asyncio.get_event_loop()
        archivo_path = None

        try:
            with yt_dlp.YoutubeDL({**opciones, "simulate": True}) as ydl:
                print(f"  🔍 Obteniendo info de: {url}")
                info = await loop.run_in_executor(
                    None, lambda: ydl.extract_info(url, download=False)
                )

            error = self.validar_info(info)
            if error:
                return await msg.edit(content=error)

            titulo = info.get("title", "video")[:50]
            print(f"  ✅ Video válido: {titulo}")
            await msg.edit(content=f"⬇️ Descargando **{titulo}**...")

            def descargar_sync():
                nonlocal archivo_path
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    info_dl = ydl.extract_info(url, download=True)
                    archivo_path = ydl.prepare_filename(info_dl)
                    if modo == "audio":
                        archivo_path = os.path.splitext(archivo_path)[0] + ".mp3"
                print(f"  💾 Archivo en: {archivo_path}")

            await loop.run_in_executor(None, descargar_sync)

            if not os.path.exists(archivo_path):
                return await msg.edit(content="❌ No se encontró el archivo descargado.")

            tamanio_real_mb = os.path.getsize(archivo_path) / (1024 * 1024)
            print(f"  📦 Tamaño real: {tamanio_real_mb:.1f} MB")

            if tamanio_real_mb > MAX_TAMANIO_MB:
                os.remove(archivo_path)
                return await msg.edit(content=f"❌ El archivo pesa **{tamanio_real_mb:.1f} MB** y supera el límite de {MAX_TAMANIO_MB} MB.")

            await msg.edit(content=f"📤 Enviando **{titulo}**...")
            await ctx.send(file=discord.File(archivo_path))
            await msg.delete()
            print(f"  ✅ Enviado exitosamente")

        except yt_dlp.utils.DownloadError as e:
            print(f"  ❌ DownloadError: {e}")
            await msg.edit(content=f"❌ Error al descargar: `{e}`")
        except Exception as e:
            print(f"  ❌ Error inesperado: {e}")
            await msg.edit(content=f"❌ Error inesperado: `{e}`")
        finally:
            if archivo_path and os.path.exists(archivo_path):
                os.remove(archivo_path)
                print(f"  🧹 Temporal eliminado")

async def setup(bot):
    await bot.add_cog(Descargas(bot))