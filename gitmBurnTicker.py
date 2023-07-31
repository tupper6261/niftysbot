#GITM Ticker Discord Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.1 - April 27, 2022

import os
import json
import requests
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import psycopg2

load_dotenv()

TOKEN = os.environ.get('GLITCH_TOKEN')
DATABASETOKEN = os.getenv('DATABASE_URL')
niftysAuthorization = os.getenv('NIFTYS_BEARER_TOKEN')
niftysAuthKeyID = os.getenv('NIFTYS_AUTH_KEY')

niftysAPIHeaders = {
    'accept': 'application/json',
    'Authorization': niftysAuthorization,
    'auth-key-id': niftysAuthKeyID,
}

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():
    guild = bot.get_guild(869370430287384576)
    channel = discord.utils.get(guild.channels, name='bot-inits')
    #while True:
        #await runGlitchStartup(guild, channel)
        #await updateRoles(guild, channel)

async def runGlitchStartup(guild, channel):
    completedSuccessfully = True
    i = True
    burnedGlitches = 0
    glitchesLeft = 0
    try:
        response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=1&contractAddress=0x797735ff36e3a602dbb54510263cfb42633f2486&take=20', headers=headers)
    except:
        await channel.send("There was an error calling the Nifty's Connect API. I will try again in eleven minutes.")
    else:
        try:
            data = json.loads(response.text)
        except:
            await channel.send("There was an error parsing JSON data. I will try again in eleven minutes.")
        else:
            try:
                error = data['code']
            except:
                for item in data['data']:
                    if item['wallet']['address'] == "0x0000000000000000000000000000000000000000":
                        burnedGlitches = item['quantity']
                    if item['wallet']['address'] == "0x8f8519f23249fce2c0aa7961b6d8aa67dae7ec75":
                        glitchesLeft += int(item['quantity'])
                    if item['wallet']['address'] == "0xdcae9202e61b4db38a461836ee1311d923f7a617":
                        glitchesLeft += int(item['quantity'])
            else:
                await channel.send("Rate limit on Nifty's Connect API exceeded. I will try again in eleven minutes.")
                completedSuccessfully = False
            name = str(burnedGlitches)+ " GITM Burned"
            '''
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "update discordShop set inventory = {0} where item_id = 1".format(glitchesLeft)
            cur.execute(command)
            cur.close()
            conn.commit()
            conn.close()
            '''
            if completedSuccessfully:
                try:
                    await guild.me.edit(nick=name)
                except:
                    await channel.send("There was an error updating my nickname. I will try again in eleven minutes.")
                else:
                    await asyncio.sleep(1)

async def updateRoles(guild, channel):
    purpleCapRole = guild.get_role(958871211625021520)
    matrixHolderRole = guild.get_role(959137823317950464)
    spaceJamHolderRole = guild.get_role(979455341009985627)
    tweetyHolderRole = guild.get_role(988786072760774696)
    sylvesterHolderRole = guild.get_role(1024693150482169967)
    bugsHolderRole = guild.get_role(1024701273347465377)
    bulletTrainHolderRole = guild.get_role(1024692977261621298)
    splitUserList = []
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from niftysAccounts"
    cur.execute(command)
    searchResult = cur.fetchall()
    cur.close()
    conn.close()
    m = len(searchResult)
    n = 1
    for user in searchResult:
        #print (str(n)+"/"+str(m))
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "select * from avatars where owner_handle = '{0}'".format(user[0])
        cur.execute(command)
        matrixSearchResult = cur.fetchall()
        command = "select * from avatars where owner_handle = '{0}' and headwear = 'Purple Worker''s Cap'".format(user[0])
        cur.execute(command)
        purpleSearchResult = cur.fetchall()
        if purpleSearchResult == []:
            command = "select * from avatars where owner_handle = '{0}' and headwear = 'Purple Workers Cap'".format(user[0])
            cur.execute(command)
            purpleSearchResult = cur.fetchall()
        if matrixSearchResult != []:
            matrixHolder = True
        if purpleSearchResult != []:
            purpleCapHolder = True
        command = "select space_jam_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        spaceJamHolder = cur.fetchall()
        command = "select tweety_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        tweetyHolder = cur.fetchall()
        command = "select sylvester_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        sylvesterHolder = cur.fetchall()
        command = "select bugs_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        bugsHolder = cur.fetchall()
        command = "select bullet_train_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        bulletTrainHolder = cur.fetchall()
        cur.close()
        conn.close()
        spaceJamHolder = spaceJamHolder[0][0]
        tweetyHolder = tweetyHolder[0][0]
        sylvesterHolder = sylvesterHolder[0][0]
        bugsHolder = bugsHolder[0][0]
        bulletTrainHolder = bulletTrainHolder[0][0]
        member = discord.utils.get(guild.members, id=int(user[4]))
        if member != None:
            if matrixHolder:
                await member.add_roles(matrixHolderRole)
            else:
                await member.remove_roles(matrixHolderRole)
            if purpleCapHolder:
                await member.add_roles(purpleCapRole)
            else:
                await member.remove_roles(purpleCapRole)
            if spaceJamHolder:
                await member.add_roles(spaceJamHolderRole)
            else:
                await member.remove_roles(spaceJamHolderRole)
            if tweetyHolder:
                await member.add_roles(tweetyHolderRole)
            else:
                await member.remove_roles(tweetyHolderRole)
            if bugsHolder:
                await member.add_roles(bugsHolderRole)
            else:
                await member.remove_roles(bugsHolderRole)
            if sylvesterHolder:
                await member.add_roles(sylvesterHolderRole)
            else:
                await member.remove_roles(sylvesterHolderRole)
            if bulletTrainHolder:
                await member.add_roles(bulletTrainHolderRole)
            else:
                await member.remove_roles(bulletTrainHolderRole)
        n += 1


@bot.command(name='runGlitch')
async def runGlitch(ctx):
    while True:
        completedSuccessfully = True
        i = True
        burnedGlitches = 0
        try:
            response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=1&contractAddress=0x797735ff36e3a602dbb54510263cfb42633f2486&take=20', headers=headers)
        except:
            await ctx.send("There was an error calling the Nifty's Connect API. I will try again in eleven minutes.")
        else:
            try:
                data = json.loads(response.text)
            except:
                await ctx.send("There was an error parsing JSON data. I will try again in eleven minutes.")
            else:
                while i:
                    for item in data['data']:
                        if item['wallet']['address'] == "0x0000000000000000000000000000000000000000":
                            burnedGlitches = item['quantity']
                            i = False
                        if item['quantity'] == "1":
                            i = False
                    if i:
                        await asyncio.sleep(3)
                        try:
                            response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=1&contractAddress=0x797735ff36e3a602dbb54510263cfb42633f2486&take=20&paginationCursor='+str(data['paginationCursor']), headers=headers)
                        except:
                            await ctx.send("There was an error calling the Nifty's Connect API. I will try again in eleven minutes.")
                            i = False
                            completedSuccessfully = False
                        else:
                            try:
                                data = json.loads(response.text)
                            except:
                                await ctx.send("There was an error parsing JSON data. I will try again in eleven minutes.")
                                i = False
                                completedSuccessfully = False
                            else:
                                await asyncio.sleep(1)
                name = str(burnedGlitches)+ " GITM Burned"
                if completedSuccessfully:
                    try:
                        await ctx.guild.me.edit(nick=name)
                    except:
                        await ctx.send("There was an error updating my nickname. I will try again in eleven minutes.")
                    else:
                        await ctx.send("GITM Burn count updated successfully. I will check again in eleven minutes.")
        await asyncio.sleep(660)

@bot.event
async def on_message(message):
    channel = str(message.channel)
    author = str(message.author)
    socialChannels = ["niftys-twitter", "niftys-instagram", "matrix-twitter", "matrix-instagram"]
    if channel == "📥〡suggestion-box":
        messageTitle = ""
        messageContent = ""
        messageURL = ""
        if len(message.embeds) != 0:
            messageTitle = str(message.embeds[0].title)
            if messageTitle == "Embed.Empty":
                messageTitle = ""
            messageContent = str(message.embeds[0].description)
            if messageContent == "Embed.Empty":
                messageContent = ""
            messageURL = str(message.embeds[0].url)
            if messageURL == "Embed.Empty":
                messageURL = ""

        payload = {"blocks":[]}
        authorString = "Author: " + author
        payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text":"*Source: Discord*"}})
        payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text":authorString}})
        if str(message.content) != "Embed.Empty":
            payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text":message.content}})
        if messageTitle!="":
            payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text":messageTitle}})
        if messageContent!="":
            payload['blocks'].append({"type": "section","text": {"type": "mrkdwn","text": messageContent}})
        if messageURL!="":
            payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text": messageURL}})

        url = 'https://hooks.slack.com/services/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'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers)
    '''
    if channel in socialChannels:
        messageTitle = ""
        messageContent = ""
        messageURL = ""
        if len(message.embeds) != 0:
            messageTitle = str(message.embeds[0].title)
            if messageTitle == "Embed.Empty":
                messageTitle = ""
            messageContent = str(message.embeds[0].description)
            if messageContent == "Embed.Empty":
                messageContent = ""
            messageURL = str(message.embeds[0].url)
            if messageURL == "Embed.Empty":
                messageURL = ""

        payload = {"blocks":[]}
        if str(message.content) != "Embed.Empty":
            payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text":message.content}})
        if messageTitle!="":
            payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text":messageTitle}})
        if messageContent!="":
            payload['blocks'].append({"type": "section","text": {"type": "mrkdwn","text": messageContent}})
        if messageURL!="":
            payload['blocks'].append({"type":"section","text":{"type": "mrkdwn","text": messageURL}})

        url = 'https://hooks.slack.com/services/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'
        headers = {'content-type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers)
    '''
    
                  

bot.run(TOKEN)
