#Reward Giveaway Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.1 - May 24, 2022

#Dependencies
import os
import random
import urllib.request
import time
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
from discord.commands import Option
from dotenv import load_dotenv
import psycopg2
import json
import requests
import datetime
import asyncio
from web3 import Web3
import csv

load_dotenv()
TOKEN = os.environ.get('GIVEAWAY_TOKEN')
DATABASETOKEN = os.getenv('DATABASE_URL')
PRIVATEKEY = os.environ.get('GIVEAWAY_PRIVATE_KEY')

client = discord.Client()
#Discord now makes you explicitly declare some of the permissions that your bot will need.
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
#This one initializes a bot object and tells it to look for commands that start with + (ie +thousandglitchgiveaway)
bot = commands.Bot(command_prefix="+", intents=intents)



#This method runs when the bot boots up.
@bot.event
async def on_ready():
    guild = bot.get_guild(869370430287384576)
    whiteBeltHolderRole = guild.get_role(1065309274366021704)
    photocopierPassHolderRole= guild.get_role(1065309444063367310)
    i = 0
    for member in whiteBeltHolderRole.members:
        await member.remove_roles(whiteBeltHolderRole)
        print (len(whiteBeltHolderRole.members) - i)
        i += 1
    print("finished red pill")
    i = 0
    for member in photocopierPassHolderRole.members:
        await member.remove_roles(photocopierPassHolderRole)
        print (len(photocopierPassHolderRole.members) - i)
        i += 1
    print ("finished blue pill")
 
        
    '''
    #Builds a channel object based on the channel name where we'll be posting
    
    channel = discord.utils.get(guild.channels, name='💊┃matrix-collect')
    msg = await channel.fetch_message(1069731134457520239)
    await msg.reply("I call shenanigans on your face")
    #await channel.send("")
    '''


class MyView(View):
    
    def __init__(self):
        super().__init__(timeout = 182)
        #self.ctx = ctx

    async def on_timeout(self):
        return

async def roundFunc(roundNum):
    roundNum = int(roundNum)
    #Builds a guild object based on the Nifty's server id
    guild = bot.get_guild(869370430287384576)
    #Builds a channel object based on the channel name where we'll be posting
    channel = discord.utils.get(guild.channels, name='🧟│Gaming lounge')
    #channel = discord.utils.get(guild.channels, name='🎮│gaming lounge')
    #channel = discord.utils.get(guild.channels, name='📣〡niftys-talks')
    #channel = discord.utils.get(guild.channels, name='🥕〡looney-tunes-holders')
    #channel = discord.utils.get(guild.channels, name='bot-inits')
    #setting this here so it's accessible throughout the function
    messageID = 0
    view = MyView()

    if roundNum == 1:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="Hey guys! Thanks for joining us for game night! Here's 1000 coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()

    elif roundNum == 2:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="This is fun - my first horror movie! Here's another 1000 coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()

    elif roundNum == 3:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="Here's another 1000 coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        await channel.send("https://tenor.com/view/thriller-michael-jackson-popcorn-gif-11644499")
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()

    elif roundNum == 4:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="Here's another 1000 coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        await channel.send("https://tenor.com/view/watching-popcorn-eating-scared-watch-gif-17211195")
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()
        
    elif roundNum == 5:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="Here's another 1000 coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        await channel.send("https://tenor.com/view/shock-gif-25165873")
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()

    elif roundNum == 6:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="Here's another 1000 coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        await channel.send("https://tenor.com/view/jb-fletcher-murder-murder-she-wrote-angela-lansbury-popcorn-gif-5919752")
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()

    elif roundNum == 7:
        async def claimCoinsButton_callback(interaction):
            member = interaction.user
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from coinGiveawayWinners where discord_id = {0} and round_won = {1}".format(member.id, roundNum)
            cur.execute(command)
            alreadyWon = cur.fetchall()
            if alreadyWon == []:
                command = "select * from vault where discord_user_id = {0}".format(member.id)
                cur.execute(command)
                account = cur.fetchall()
                if account == []:
                    command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(member.id, int(time.time()))
                    cur.execute(command)
                    await interaction.response.send_message("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!", ephemeral = True)
                else:
                    account = account[0]
                    newBalance = account[1] + 1000
                    command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                    cur.execute(command)
                    await interaction.response.send_message("Success! I just sent you 1000 Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
                command = "insert into coinGiveawayWinners (discord_id, round_won) values ({0}, {1})".format(member.id, roundNum)
                cur.execute(command)
            else:
                await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
            cur.close()
            conn.commit()
            conn.close()

        claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
        claimCoinsButton.callback = claimCoinsButton_callback

        expiryTime = int(time.time()) + 300

        embed = discord.Embed(description="What an iconic film! I loved it and I'm personally glad I don't have any brains to be eaten.\n\nHere's your last batch of coins. Thanks for joining us!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
        
        view.add_item(claimCoinsButton)
        view.message = await channel.send(embed = embed, view = view)
        await asyncio.sleep(300)
        await view.message.delete()
    
#Defines the startgiveaway command
@bot.command(name='startgiveaway')
async def startgiveaway(ctx, roundNum):
    if ctx.author.id == 710139786404298822:
        await ctx.message.delete()
        await roundFunc(roundNum)
    else:
        await ctx.send("Nice try. I only take orders from my creator.")

#Defines the startgiveaway command
@bot.command(name='sendphoto')
async def sendphoto(ctx, photoNum):
    if ctx.author.id == 710139786404298822:
        await ctx.message.delete()
        photoNum = int(photoNum)
        #Builds a guild object based on the Nifty's server id
        guild = bot.get_guild(869370430287384576)
        #Builds a channel object based on the channel name where we'll be posting
        channel = discord.utils.get(guild.channels, name='📣〡niftys-talks')
        if photoNum == 1:
            await channel.send("https://imgur.com/EWvK6nB")
        if photoNum == 2:
            await channel.send("https://imgur.com/8II20U0")
        if photoNum == 3:
            await channel.send("https://imgur.com/phv2RVN")
    else:
        await ctx.send("Nice try. I only take orders from my creator.")

#Defines the startgiveaway command
@bot.command(name='sendmessage')
async def sendmessage(ctx):
    guild = bot.get_guild(869370430287384576)
    #Builds a channel object based on the channel name where we'll be posting
    channel = discord.utils.get(guild.channels, name='🦈〡shark-week-chat')
    msg = await channel.fetch_message(1001300888662577192)
    await msg.reply("Bob and I go way back. He's cool with it.")
    #await channel.send("https://tenor.com/view/you-didnt-hear-this-from-me-lucifer-i-didnt-say-anything-dont-tell-anyone-netflix-gif-18409801")

#Runs the bot using the TOKEN defined in the environmental variables.         
bot.run(TOKEN)
