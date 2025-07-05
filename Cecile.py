import discord
from discord.ext import commands
import asyncio

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Configuration personnalisable
import os
TOKEN = os.getenv("TOKEN")
PREFIX = "!"
CHANNEL_ID = 1386108008676855930  # Canal pour les commandes
ROLE_ID = 987654321098765432     # (Option : pour attribution de rôles)

# Instanciation
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# 📊 Initialise les compteurs
counters = {
    "verif": 0,     # pour les vérifications réussies
    "important": 0  # pour les messages jugés importants
}

# 🟢 Evenement prêt
@bot.event
async def on_ready():
    print(f"{bot.user} connecté !")

@bot.command(name="verif")
@commands.has_permissions(manage_messages=True)
async def cmd_verif(ctx):
    if ctx.channel.id != CHANNEL_ID:
        return  # Ignore si ce n’est pas le bon salon
    counters["verif"] += 1
    await ctx.send(f"🔢 Compteur 'verif' : {counters['verif']}")

# 🔥 Commande pour incrémenter le compteur 'important'
@bot.command(name="important")
@commands.has_permissions(manage_messages=True)
async def cmd_important(ctx):
    counters["important"] += 1
    await ctx.send(f"🔢 Compteur 'important' : {counters['important']}")

# 📋 Afficher l’état des compteurs
@bot.command(name="stats")
async def cmd_stats(ctx):
    await ctx.send(
        f"📊 **Statistiques actuelles** :\n"
        f"- verif : {counters['verif']}\n"
        f"- important : {counters['important']}"
    )

# 🔄 Réinitialiser un compteur
@bot.command(name="reset")
@commands.has_permissions(manage_messages=True)
async def cmd_reset(ctx, which: str):
    which = which.lower()
    if which in counters:
        counters[which] = 0
        await ctx.send(f"🔁 Le compteur **{which}** a été remis à zéro.")
    else:
        await ctx.send(f"❌ Le compteur **{which}** n'existe pas : {', '.join(counters.keys())}")

# 🚫 Gestion des erreurs pour permissions
@cmd_verif.error
@cmd_important.error
@cmd_reset.error
async def perms_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("JE TE FRIEND ZONE BATARD")

# 🔐 Commande pour autoriser un rôle spécifique (exemple d'utilisation)
@bot.command(name="giverole")
@commands.has_permissions(manage_roles=True)
async def cmd_giverole(ctx, member: discord.Member):
    role = ctx.guild.get_role(ROLE_ID)
    if role:
        await member.add_roles(role)
        await ctx.send(f"✅ {member.mention} a reçu le rôle **{role.name}**.")
    else:
        await ctx.send("❌ Rôle introuvable.")

bot.run(TOKEN)