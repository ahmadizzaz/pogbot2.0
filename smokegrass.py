from discord.ext import commands
import discord

class SmokeGrass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Smoke Grass(Josh server) module loaded")

    @commands.Cog.listener()
    async def on_message(self,ctx):
        if str(ctx.guild.id) == '221656082282446850': #Josh server (SMOKE GRASS)
            if ctx.content.lower() == ('justin'):
                await ctx.channel.send(f'is gei lou')

            if ctx.content.lower() == ('brian'):
                await ctx.channel.send(f'is stupit')

            if ctx.content.lower() == ('dan'):
                await ctx.channel.send(f'is studying or probably in UK dy')
            
            if ctx.content.lower() == ('waihoe'):
                await ctx.channel.send(f'wants to TFT mou')

            if ctx.content.lower() == ('josh'):
                await ctx.channel.send(f'wants to grab biscuit')
            
            if ctx.content.lower() == ('joshua'):
                await ctx.channel.send(f'will be right back to get water')

            if ctx.content.lower() == ('lee'):
                await ctx.channel.send(f'already knows')
            
            if ctx.content.lower() == ('izzaz'):
                await ctx.channel.send(f'‎')

            if ctx.content.lower() == ('jordan'):
                await ctx.channel.send(f'')

            if ctx.content.lower() == ('nic'):
                await ctx.channel.send(f'needs to wait for annie to grow older')

    
def setup(bot):
    bot.add_cog(SmokeGrass(bot))