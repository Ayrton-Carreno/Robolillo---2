import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Robolillo conectado como {bot.user}")
    print(f"📡 Servidores conectados: {[g.name for g in bot.guilds]}")
    
    cogs = cogs = ["cogs.music", "cogs.fun", "cogs.moderation", "cogs.download", "cogs.menus", "cogs.games"]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f"  ✅ Cog cargado: {cog}")
        except Exception as e:
            print(f"  ❌ Error cargando {cog}: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"📨 Mensaje | Canal: #{message.channel.name} | Autor: {message.author} | '{message.content}'")
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    print(f"⚙️  Comando: '{ctx.command}' por {ctx.author} en #{ctx.channel.name}")

@bot.event
async def on_command_error(ctx, error):
    print(f"❌ Error en comando '{ctx.command}': {error}")
    await ctx.send(f"❌ Error: `{error}`")

bot.run(TOKEN)