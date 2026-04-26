import discord
from discord.ext import commands

class Moderacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("🔨 Cog Moderación inicializado")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, miembro: discord.Member, *, razon="Sin razón especificada"):
        print(f"👢 !kick ejecutado por {ctx.author} contra {miembro} | Razón: {razon}")
        await miembro.kick(reason=razon)
        await ctx.send(f"👢 {miembro.mention} fue expulsado. Razón: {razon}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, miembro: discord.Member, *, razon="Sin razón especificada"):
        print(f"🔨 !ban ejecutado por {ctx.author} contra {miembro} | Razón: {razon}")
        await miembro.ban(reason=razon)
        await ctx.send(f"🔨 {miembro.mention} fue baneado. Razón: {razon}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def limpiar(self, ctx, cantidad: int = 5):
        print(f"🧹 !limpiar ejecutado por {ctx.author} | Cantidad: {cantidad}")
        await ctx.channel.purge(limit=cantidad + 1)
        await ctx.send(f"🧹 Se borraron {cantidad} mensajes.", delete_after=3)

async def setup(bot):
    await bot.add_cog(Moderacion(bot))