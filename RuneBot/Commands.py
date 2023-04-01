import discord
from discord.ext import commands

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        print (dir(ctx))
        print (ctx.channel)
        await ctx.send('pong')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if 'blank' in message.content.lower():
            print('yu boy')
            await message.channel.send('Hello!')

    @commands.Cog.listener()
    async def on_slash_command(self, ctx: discord.slash_command()):
        if ctx.name == 'ping':
            await ctx.send('Pong!')

def setup(bot):
    bot.add_cog(ExampleCog(bot))