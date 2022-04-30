from contextlib import suppress
from discord.ext import commands
import requests
import json
import discord
import re
import asyncio
import sqlite3

from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption


DiscordComponents(commands.Bot)


class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Valorant module loaded")

    @commands.command()
    async def valorant(self, ctx, *arg):
        dbClient = sqlite3.connect("discord.db")
        pattern = re.compile("<@\d+>")
        print(arg)

        if not arg:
            print("2")
            arg = [f"<@{ctx.author.id}>"]
        arg = arg[0]
        if pattern.match(arg):
            print("3")             
           
            argument = arg
            argument = argument.replace('<',"")
            argument = argument.replace('>',"")
            argument = argument.replace('@',"")
            print(argument)   
            cursor = dbClient.cursor()
            cursor.execute(f"SELECT * FROM VALORANT WHERE DISCORDID = {argument}")
            rows = cursor.fetchall()
            embedAccountList = []
            idAccountList = []
            print("5")
            if len(rows) == 0:
                return await ctx.send("User has no linked valorant account(s)")
            for x in rows:
                print(x)
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                valoAccountUrl = "https://api.henrikdev.xyz/valorant/v1/account/" + x[1] + "/"+ x[2]
                valorantAccountResponse = requests.get(valoAccountUrl,headers=headers)
                if valorantAccountResponse.json()["status"] == 200:
                    print("Got data from get Account api")
                    data = valorantAccountResponse.json()["data"]
                    valoRankUrl = "https://api.henrikdev.xyz/valorant/v1/mmr/"+data["region"]+"/"+ x[1] + "/"+ x[2]
                    valorantRankResponse = requests.get(valoRankUrl,headers=headers)
                    if valorantRankResponse.json()["status"] == 200:
                        print("Got data from get mmr api")
                        rankData = valorantRankResponse.json()["data"]
                        embed = discord.Embed(title=f"{rankData['name']}#{rankData['tag']}")
                        compTierUrl = "https://valorant-api.com/v1/competitivetiers/e4e9a692-288f-63ca-7835-16fbf6234fda"
                        compTierResponse = requests.get(compTierUrl,headers=headers)
                        # print(compTierResponse.json()["data"]["tiers"][rankData['currenttier']]["smallIcon"])
                        embed.set_thumbnail(url=compTierResponse.json()["data"]["tiers"][rankData['currenttier']]["largeIcon"])

                        try:
                            # embed.set_thumbnail(url=data["card"]["small"])
                            embed.set_image(url=data["card"]["wide"])
                        except:
                            cardUrl = "https://valorant-api.com/v1/playercards/9fb348bc-41a0-91ad-8a3e-818035c4e561"
                            cardResponse = requests.get(cardUrl,headers=headers)
                            # embed.set_thumbnail(url=cardResponse.json()["data"]["smallArt"])
                            embed.set_image(url=cardResponse.json()["data"]["wideArt"])
                            print("No card data")
                        print("startEmbed")
                        embed.add_field(name="Options",value= "◀️:Previous page 🗑️:Remove from account\n▶️:Next Page ❎:Close")
                        embed.add_field(name="Username",value= f"{rankData['name']}#{rankData['tag']}",inline=False)
                        embed.add_field(name="Account Level",value=f"{data['account_level']}",inline=True)
                        embed.add_field(name="Rank",value=f"{rankData['currenttierpatched']}",inline=True)
                        embedAccountList.append(embed)
                        idAccountList.append(str(data['puuid']))

                    elif valorantRankResponse.json()["status"] == 403:
                        await ctx.send('API on maintenance. Try again later')
                    elif valorantRankResponse.json()["status"] == 404:
                        await ctx.send('User not found!')
                    else:
                        await ctx.send('Something went wrong. Please contact Lv99Magikarp#6969.')              
                elif valorantAccountResponse.json()["status"] == 403:
                    await ctx.send('API on maintenance. Try again later')
                elif valorantAccountResponse.json()["status"] == 404:
                    await ctx.send('User not found!')
                else:
                    await ctx.send('Something went wrong. Please contact Lv99Magikarp#6969.')
            
            print("6")
            if len(embedAccountList) == 0:
                return await ctx.send("User has no linked valorant account(s)")
            else:
                print(embedAccountList)
                print(idAccountList)
                index = 0
                msg = await ctx.send("‎",embed = embedAccountList[index])
                BUTTONS = ["◀️", "🗑️","❎","▶️"]
                for b in BUTTONS:
                    await msg.add_reaction(b)
                
                while True:
                    if len(embedAccountList) == 0:
                        await msg.clear_reactions()
                        return await msg.edit("User has no linked valorant account(s)" ,suppress=True)
                    try:
                        react, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=lambda r, u: r.message.id == msg.id and u.id == ctx.author.id and r.emoji in BUTTONS)
                        await msg.remove_reaction(react.emoji, user) #Removes the user reaction after he/she reacts the message
                    
                    except asyncio.TimeoutError:
                        return await msg.delete()

                    else:
                        if react.emoji == BUTTONS[0] and index > 0: #if current page is the first page this will not work
                            index -= 1
                        elif react.emoji == BUTTONS[1]:
                            if len(embedAccountList) == 0:
                                await msg.clear_reactions()
                                return await msg.edit("User has no linked valorant account(s)",suppress=True)
                            
                            cursor = dbClient.cursor()
                            cursor.execute(f"DELETE FROM VALORANT WHERE ID='{idAccountList[index]}'")
                            dbClient.commit()
                            embedAccountList.pop(index)
                            idAccountList.pop(index)
                            if len(embedAccountList) == 0:
                                await msg.clear_reactions()
                                return await msg.edit("User has no linked valorant account(s)",suppress=True)
                            index = 0
                        elif react.emoji == BUTTONS[3] and index < len(embedAccountList) - 1: #checking if current page is not the last one
                            index += 1
                        elif react.emoji == BUTTONS[2]:
                            return await msg.delete()

                        await msg.edit(embed=embedAccountList[index]) #editing message content
                

        elif " " in arg or "#" not in arg:
            await ctx.send('Please type using the following format : name#tag')
        else:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            username = arg.split("#")
            print(username)
            valoAccountUrl = "https://api.henrikdev.xyz/valorant/v1/account/" + username[0]+ "/"+ username[1]
            valorantAccountResponse = requests.get(valoAccountUrl,headers=headers)
            print(valorantAccountResponse.json())
            if valorantAccountResponse.json()["status"] == 200:
                data = valorantAccountResponse.json()["data"]
                valoRankUrl = "https://api.henrikdev.xyz/valorant/v1/mmr/"+data["region"]+"/"+ username[0]+ "/"+ username[1]
                valorantRankResponse = requests.get(valoRankUrl,headers=headers)
                if valorantRankResponse.json()["status"] == 200:
                    rankData = valorantRankResponse.json()["data"]
                    icoUrl = data["card"]["large"]
                    embed=discord.Embed(title=(f"{data['name']}#{data['tag']}"), url=icoUrl, description=f'Account Level : {data["account_level"]}\nRegion : {data["region"]}\nRank : {rankData["currenttierpatched"]}')
                    embed.set_thumbnail(url=data["card"]["small"])
                    embed.set_image(url=data["card"]["wide"])
                    await ctx.send(embed=embed)
                elif valorantRankResponse.json()["status"] == 403:
                    await ctx.send('API on maintenance. Try again later')
                elif valorantRankResponse.json()["status"] == 404:
                    await ctx.send('User not found!')
                else:
                    await ctx.send('Something went wrong. Please contact Lv99Magikarp#6969.')              
            elif valorantAccountResponse.json()["status"] == 403:
                await ctx.send('API on maintenance. Try again later')
            elif valorantAccountResponse.json()["status"] == 404:
                await ctx.send('User not found!')
            else:
                await ctx.send('Something went wrong. Please contact Lv99Magikarp#6969.')
        dbClient.close()


    @valorant.error
    async def valorant_error(cog,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type using the following format : name#tag')


    @commands.command()
    async def valolink(self, ctx, arg1 ):
        dbClient = sqlite3.connect("discord.db")

        if " " in arg1 or "#" not in arg1:
            print(ctx.__dict__)
            print(arg1)
            await ctx.send('Please type using the following format : name#tag')
        else:
            print(ctx.author.id)
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            username = arg1.split("#")
            valoAccountUrl = "https://api.henrikdev.xyz/valorant/v1/account/" + username[0]+ "/"+ username[1]
            valorantAccountResponse = requests.get(valoAccountUrl,headers=headers)
            print(valorantAccountResponse.json())
            if valorantAccountResponse.json()["status"] == 200:
                data = valorantAccountResponse.json()["data"]
                dbClient.execute(f"INSERT INTO VALORANT (ID,NAME,TAG,DISCORDID) VALUES ('{data['puuid']}','{username[0]}','{username[1]}','{ctx.author.id}')")
                dbClient.commit()

                await ctx.send(f"Valorant account {arg1} saved for <@{ctx.author.id}>")
 
            elif valorantAccountResponse.json()["status"] == 403:
                await ctx.send('API on maintenance. Try again later')
            elif valorantAccountResponse.json()["status"] == 404:
                await ctx.send('User not found!')
            else:
                await ctx.send('Something went wrong. Please contact Lv99Magikarp#6969.')
        dbClient.close()


    @valolink.error
    async def valolink_error(cog,ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please type using the following format : name#tag')

    
    

def setup(bot):
    bot.add_cog(Valorant(bot))