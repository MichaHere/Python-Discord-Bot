import discord
from discord.ext import commands

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print("Bot is ready")


@client.command()
async def hello(ctx):
    await ctx.send("Hi!")

client.run("NTM1NDg4MjYxODc1ODI2Njk5.Xwhpyw.rF1OTvcCTyh22RFwBBe55EDHtww")