#Red Pill Avatar Ticker Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.1 - April 27, 2022

import os
import random
import urllib.request
import time
import discord
from discord.ext import commands
from dotenv import load_dotenv
import psycopg2
import json
import requests
import datetime
import asyncio

load_dotenv()
TOKEN = os.environ.get('RED_PILL_TOKEN')
DATABASETOKEN = os.getenv('DATABASE_URL')

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_ready():
    guild = bot.get_guild(869370430287384576)
    channel = discord.utils.get(guild.channels, name='bot-inits')
    while True:
        await runRedStartup(guild, channel)
        await updateRoles(guild, channel)        

async def runRedStartup(guild, channel):
    redPalmURL = "https://explorer.palm.io/token/0x28E4b03bC88B59D25f3467B2252b66d4b2c43286/inventory"
    try:
        xRed = urllib.request.urlopen(redPalmURL)
    except:
        await channel.send("There was an error opening the red pill contract webpage on the Palm blockchain explorer. I will try again in an hour.")
    else:
        xRed = str(xRed.read())
        firstMatrixRed = xRed.find("MATRIXRED")
        secondMatrixRed = xRed.find("MATRIXRED",firstMatrixRed+5)
        thirdMatrixRed = xRed.find("MATRIXRED",secondMatrixRed+5)
        name=xRed[thirdMatrixRed-9:thirdMatrixRed-3] + " Red Pills"
        try:
            await guild.me.edit(nick=name)
        except:
            await channel.send("There was an error updating my nickname. I will try again in an hour.")
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
    workingPhoneHolderRole = guild.get_role(1052614060102930473)
    whiteBeltHolderRole = guild.get_role(1052614164742426645)
    photocopierPassHolderRole= guild.get_role(1052614266324262912)
    gotHolderRole = guild.get_role(1062491726977183836)
    splitUserList = []
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from niftysAccounts"
    cur.execute(command)
    searchResult = cur.fetchall()
    cur.close()
    conn.close()
    for user in searchResult:
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
        else:
            matrixHolder = False
        if purpleSearchResult != []:
            purpleCapHolder = True
        else:
            purpleCapHolder = False
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
        command = "select copier_pass_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        photocopierPassHolder = cur.fetchall()
        command = "select white_belt_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        whiteBeltHolder = cur.fetchall()
        command = "select working_phone_holder from niftysAccounts where discord_user_id = '{0}'".format(int(user[4]))
        cur.execute(command)
        workingPhoneHolder = cur.fetchall()
        cur.close()
        conn.close()
        spaceJamHolder = spaceJamHolder[0][0]
        tweetyHolder = tweetyHolder[0][0]
        sylvesterHolder = sylvesterHolder[0][0]
        bugsHolder = bugsHolder[0][0]
        bulletTrainHolder = bulletTrainHolder[0][0]
        workingPhoneHolder = workingPhoneHolder[0][0]
        whiteBeltHolder = whiteBeltHolder[0][0]
        photocopierPassHolder = photocopierPassHolder[0][0]
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
            if workingPhoneHolder:
                await member.add_roles(workingPhoneHolderRole)
            else:
                await member.remove_roles(workingPhoneHolderRole)
            if whiteBeltHolder:
                await member.add_roles(whiteBeltHolderRole)
            else:
                await member.remove_roles(whiteBeltHolderRole)
            if photocopierPassHolder:
                await member.add_roles(photocopierPassHolderRole)
            else:
                await member.remove_roles(photocopierPassHolderRole)
    
async def sharkWeekHolders(guild, channel):
    completedSuccessfully = True
    i = True
    burnedGlitches = 0
    glitchesLeft = 0
    sharks = {
        'megamouth': 26915478242617465688247288818336585759,
        'greenland': 159679488646183539475848961431588095765,
        'basking': 222681684434523730404528039634404014897,
        'mako': 34226120671307386742086181880697465259,
        'bull': 79470045184162462714691945503074451013,
        'wobblegong': 330127669445791036851237571924415636789,
        'tiger': 200193234185085031695279862003953578154
        }
    
    try:
        response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=1&contractAddress=0x0f762a965a085221b849e7d12d75f45b4d54adb7&take=20', headers=headers)
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
    
bot.run(TOKEN)
