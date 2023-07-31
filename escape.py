#Zombie Escape Discord Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.0 - December 6, 2022

# bot.py
import os
import random
import urllib.request
import time
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from dotenv import load_dotenv
import psycopg2
import json
import requests
import datetime
import asyncio

load_dotenv()

TOKEN = os.environ.get('ESCAPE_TOKEN')
DATABASETOKEN = os.getenv('DATABASE_URL')
niftysAuthorization = os.getenv('NIFTYS_BEARER_TOKEN')
niftysAuthKeyID = os.getenv('NIFTYS_AUTH_KEY')

niftysAPIHeaders = {
    'accept': 'application/json',
    'Authorization': niftysAuthorization,
    'auth-key-id': niftysAuthKeyID,
}


#global variable to set number of seconds before bot times out
responseTime = 60

async def voteMessage(ctx, title, description, choiceA, choiceB, waitTime):
    room = discord.Embed(title=title, description=description, color=0x000000)
    choices = {"🇦": choiceA,
           "🇧": choiceB}
    value = "\n".join("- {} {}".format(*item) for item in choices.items()) 
    room.add_field(name="You must vote as a group by reacting accordingly. You have " + str(waitTime) + " seconds to decide:", value=value, inline=True)
    message_1 = await ctx.send(embed=room)
    for choice in choices:
        await message_1.add_reaction(choice)
    message_2 = await ctx.send("**"+str(waitTime)+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    message_2 = await message_2.edit("**"+str(int(int(waitTime)/4*3))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    message_2 = await message_2.edit("**"+str(int(int(waitTime)/2))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    message_2 = await message_2.edit("**"+str(int(int(waitTime)/4))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    message_1 = await ctx.fetch_message(message_1.id)
    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(choices, key=counts.get)
    return winner

async def voteMessageThreeOptions(ctx, title, description, choiceA, choiceB, choiceC, waitTime):
    room = discord.Embed(title=title, description=description, color=0x000000)
    choices = {"🇦": choiceA,
           "🇧": choiceB,
           "🇨": choiceC}
    value = "\n".join("- {} {}".format(*item) for item in choices.items()) 
    room.add_field(name="You must vote as a group by reacting accordingly. You have " + str(waitTime) + " seconds to decide:", value=value, inline=True)
    message_1 = await ctx.send(embed=room)
    for choice in choices:
        await message_1.add_reaction(choice)
    message_2 = await ctx.send("**"+str(waitTime)+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_2 = await ctx.send("**"+str(int(int(waitTime)/4*3))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_2 = await ctx.send("**"+str(int(int(waitTime)/2))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_2 = await ctx.send("**"+str(int(int(waitTime)/4))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_1 = await ctx.fetch_message(message_1.id)
    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(choices, key=counts.get)
    return winner

async def voteMessageFiveOptions(ctx, title, description, choiceA, choiceB, choiceC, choiceD, choiceE, waitTime):
    room = discord.Embed(title=title, description=description, color=0x000000)
    choices = {"🇦": choiceA,
           "🇧": choiceB,
           "🇨": choiceC,
           "🇩": choiceD,
           "🇪": choiceE}
    value = "\n".join("- {} {}".format(*item) for item in choices.items()) 
    room.add_field(name="You must vote as a group by reacting accordingly. You have " + str(waitTime) + " seconds to decide:", value=value, inline=True)
    message_1 = await ctx.send(embed=room)
    for choice in choices:
        await message_1.add_reaction(choice)
    message_2 = await ctx.send("**"+str(waitTime)+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_2 = await ctx.send("**"+str(int(int(waitTime)/4*3))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_2 = await ctx.send("**"+str(int(int(waitTime)/2))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_2 = await ctx.send("**"+str(int(int(waitTime)/4))+" seconds remaining**")
    await asyncio.sleep(int(waitTime)/4)
    await message_2.delete()
    message_1 = await ctx.fetch_message(message_1.id)
    counts = {react.emoji: react.count for react in message_1.reactions}
    winner = max(choices, key=counts.get)
    return winner

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="+", intents=intents)

@bot.command(name='cyoa')
async def cyoa(ctx, story):
    if ctx.author.id == 710139786404298822 or ctx.author.id == 710139786404298822:
        response = requests.get('https://www.inklewriter.com/stories/' + str(story) + '.json')
        data = json.loads(response.text)
        data = data['data']
        initial = data['initial']
        current = data['stitches'][initial]
        prettyData = json.dumps(data, indent = 2)
        await ctx.channel.purge()
        description = ""
        while len(current['content']) > 1:
            options = False
            for key in current['content'][1]:
                if key == "option":
                    options = True
            if options:
                option1 = current['content'][1]
                option2 = current['content'][2]
                description += "\n\n" + current['content'][0]
                choiceA = option1['option']
                choiceB = option2['option']
                winner = await voteMessage(ctx, "", description, choiceA, choiceB, responseTime)
                if winner == "🇦":
                    current = data['stitches'][option1['linkPath']]
                if winner == "🇧":
                    current = data['stitches'][option2['linkPath']]
                await ctx.channel.purge()
                description = ""
            else:
                description += "\n\n" + current['content'][0]
                current = data['stitches'][current['content'][1]['divert']]
                if current == data['stitches'][initial]:
                    description += """\n\n**You lose. Restarting in 20 seconds.**"""
                    room = discord.Embed(description=description, color=0x000000)
                    message_1 = await ctx.send(embed=room)
                    await asyncio.sleep(20)
                    description = ""
                    await ctx.channel.purge()
        description += "\n\n" + current['content'][0]
        room = discord.Embed(description=description, color=0x000000)
        message_1 = await ctx.send(embed=room)        
        description = """**You win!**"""
        room = discord.Embed(description=description, color=0x000000)
        message_1 = await ctx.send(embed=room)
        #await ctx.channel.purge()
        #await RA(ctx)
    else:
        await ctx.send("https://tenor.com/view/parks-and-rec-bobby-newport-nice-try-laughs-laughing-gif-21862350")

@bot.command(name='mission3red')
async def mission3red(ctx):
    if ctx.author.id == 710139786404298822 or ctx.author.id == 710139786404298822:
        response = requests.get('https://www.inklewriter.com/stories/149803.json')
        data = json.loads(response.text)
        data = data['data']
        initial = data['initial']
        current = data['stitches'][initial]
        prettyData = json.dumps(data, indent = 2)
        await ctx.channel.purge()
        description = ""
        while len(current['content']) > 1:
            options = False
            for key in current['content'][1]:
                if key == "option":
                    options = True
            if options:
                option1 = current['content'][1]
                option2 = current['content'][2]
                description += "\n\n" + current['content'][0]
                choiceA = option1['option']
                choiceB = option2['option']
                winner = await voteMessage(ctx, "", description, choiceA, choiceB, responseTime)
                if winner == "🇦":
                    current = data['stitches'][option1['linkPath']]
                if winner == "🇧":
                    current = data['stitches'][option2['linkPath']]
                await ctx.channel.purge()
                description = ""
            else:
                description += "\n\n" + current['content'][0]
                current = data['stitches'][current['content'][1]['divert']]
                if current == data['stitches'][initial]:
                    description += """\n\n**You lose. Restarting in 20 seconds.**"""
                    room = discord.Embed(description=description, color=0x000000)
                    message_1 = await ctx.send(embed=room)
                    await asyncio.sleep(20)
                    description = ""
                    await ctx.channel.purge()
        description += "\n\n" + current['content'][0]
        room = discord.Embed(description=description, color=0x000000)
        message_1 = await ctx.send(embed=room)        
        description = """**You win! But were you faster than the other team?**"""
        room = discord.Embed(description=description, color=0x000000)
        message_1 = await ctx.send(embed=room)
        #await ctx.channel.purge()
        #await RA(ctx)
    else:
        await ctx.send("https://tenor.com/view/parks-and-rec-bobby-newport-nice-try-laughs-laughing-gif-21862350")

@bot.command(name='mission3blue')
async def mission3blue(ctx):
    if ctx.author.id == 710139786404298822 or ctx.author.id == 710139786404298822:
        response = requests.get('https://www.inklewriter.com/stories/149799.json')
        data = json.loads(response.text)
        data = data['data']
        initial = data['initial']
        current = data['stitches'][initial]
        prettyData = json.dumps(data, indent = 2)
        await ctx.channel.purge()
        description = ""
        while len(current['content']) > 1:
            options = False
            for key in current['content'][1]:
                if key == "option":
                    options = True
            if options:
                option1 = current['content'][1]
                option2 = current['content'][2]
                description += "\n\n" + current['content'][0]
                choiceA = option1['option']
                choiceB = option2['option']
                winner = await voteMessage(ctx, "", description, choiceA, choiceB, responseTime)
                if winner == "🇦":
                    current = data['stitches'][option1['linkPath']]
                if winner == "🇧":
                    current = data['stitches'][option2['linkPath']]
                await ctx.channel.purge()
                description = ""
            else:
                description += "\n\n" + current['content'][0]
                current = data['stitches'][current['content'][1]['divert']]
                if current == data['stitches'][initial]:
                    description += """\n\n**You lose. Restarting in 20 seconds.**"""
                    room = discord.Embed(description=description, color=0x000000)
                    message_1 = await ctx.send(embed=room)
                    await asyncio.sleep(20)
                    description = ""
                    await ctx.channel.purge()
        description += "\n\n" + current['content'][0]
        room = discord.Embed(description=description, color=0x000000)
        message_1 = await ctx.send(embed=room)        
        description = """**You win! But were you faster than the other team?**"""
        room = discord.Embed(description=description, color=0x000000)
        message_1 = await ctx.send(embed=room)
        #await ctx.channel.purge()
        #await RA(ctx)
    else:
        await ctx.send("https://tenor.com/view/parks-and-rec-bobby-newport-nice-try-laughs-laughing-gif-21862350")

#Defines a View class. Overrides the default View class primarily so I can override the timeout timer/reaction
class MyView(View):
    
    def __init__(self, ctx):
        super().__init__(timeout = 10)
        self.ctx = ctx

    async def on_timeout(self):
        for i in self.children:
            if isinstance(i, Button):
                i.disabled = True
        for i in self.children:
            if isinstance(i, Select):
                self.remove_item(i)
        await self.message.edit_original_message(view = self)

'''
@bot.event
async def on_ready():
    guild = bot.get_guild(869370430287384576)
    channel = discord.utils.get(guild.channels, id =959144897225580604)
    blueRole = discord.utils.get(guild.roles, id = 1065309274366021704)
    redRole = discord.utils.get(guild.roles, id = 1065309444063367310)
    copierRole = discord.utils.get(guild.roles, id = 1052614266324262912)
    whiteBeltRole = discord.utils.get(guild.roles, id = 1052614164742426645)

    title="Make Your Choice"
    description="""If you own a purple belt, you may claim you Red Pill role here.\n\nIf you own an office plant, you may claim your Blue Pill role here.\n\nIf you own both, you may claim either role, but you can only hold one role at a time.\n\nChoose wisely - the upcoming challenge will pit red pills against blue pills."""
    embed = discord.Embed(title=title, description=description, color=0x000000)
    embed.set_image(url="https://images-ext-1.discordapp.net/external/DWiws7HoIkyFopTm7rbqaDQ7VR2baKBAlSvVKbu0Fes/https/cdn-longterm.mee6.xyz/plugins/reaction_roles/images/869370430287384576/d1193a64564307c7bfa1dc4114e56df2adb1c8dc2cb4153c0969078ea2345a10.jpeg")
    msg = await channel.fetch_message(1052682241324613694)
    view = View(timeout = None)

    async def redButton_callback(interaction):
        if whiteBeltRole not in interaction.user.roles:
            await interaction.response.send_message(content = "It doesn't look like you own an Orange Belt NFT! Without that, you may not claim the Red Pill role", ephemeral = True)
        else:
            await interaction.user.add_roles(redRole)
            await interaction.user.remove_roles(blueRole)
            await interaction.response.send_message(content = "Success, you have been given the Red Pill role", ephemeral = True)

    async def blueButton_callback(interaction):
        if copierRole not in interaction.user.roles:
            await interaction.response.send_message(content = "It doesn't look like you own a Supply Closet Key NFT! Without that, you may not claim the Blue Pill role", ephemeral = True)
        else:
            await interaction.user.add_roles(blueRole)
            await interaction.user.remove_roles(redRole)
            await interaction.response.send_message(content = "Success, you have been given the Blue Pill role", ephemeral = True)            

    redButton = Button(label="Red Pill", style = discord.ButtonStyle.blurple, custom_id="red")
    redButton.callback = redButton_callback
    blueButton = Button(label="Blue Pill", style = discord.ButtonStyle.blurple, custom_id="blue")
    blueButton.callback = blueButton_callback

    view.clear_items()
    view.add_item(redButton)
    view.add_item(blueButton)

    bot.add_view(view, message_id = 1052682241324613694)
    await msg.edit(content = "", embed = embed, view = view)
'''

    
#Runs the bot using the TOKEN defined in the environmental variables.         
bot.run(TOKEN)
