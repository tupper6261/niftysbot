#Blue Pill Avatar Ticker Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.1 - April 27, 2022

import os
import random
import urllib.request
from urllib.error import HTTPError
from urllib.request import build_opener, HTTPCookieProcessor
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
TOKEN = os.environ.get('BLUE_PILL_TOKEN')
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
    while True:
        await banNiftys(guild)
        await runBlueStartup(guild, channel)
        await updateUserAvatars(guild, channel)


async def runBlueStartup(guild, channel):
    bluePalmURL = "https://explorer.palm.io/token/0x423E540Cb46Db0e4df1Ac96bcBdDf78a804647d8/inventory"
    try:
        xBlue = urllib.request.urlopen(bluePalmURL)
    except:
        await channel.send("There was an error opening the blue pill contract webpage on the Palm blockchain explorer. I will try again in an hour.")
    else:
        xBlue = str(xBlue.read())
        firstMatrixBlue = xBlue.find("MATRIXBLUE")
        secondMatrixBlue = xBlue.find("MATRIXBLUE",firstMatrixBlue+5)
        thirdMatrixBlue = xBlue.find("MATRIXBLUE",secondMatrixBlue+5)
        name=xBlue[thirdMatrixBlue-9:thirdMatrixBlue-3] + " Blue Pills"
        try:
            await guild.me.edit(nick=name)
        except:
            await channel.send("There was an error updating my nickname.")
        else:
            await asyncio.sleep(2)

async def updateUserAvatars(guild, channel):    
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
    gotUnopenedHolderRole = guild.get_role(1062562145235120191)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from niftysAccounts"
    cur.execute(command)
    listOfUsers = cur.fetchall()
    cur.close()
    conn.close()
    y = 0
    for i in listOfUsers:
        purpleCapHolder = False
        matrixHolder = False
        spaceJamHolder = False
        tweetyHolder = False
        sylvesterHolder = False
        bugsHolder = False
        bulletTrainHolder = False
        workingPhoneHolder = False
        whiteBeltHolder = False
        photocopierPassHolder = False
        gotHolder = False
        gotUnopenedHolder = False
        niftysAccount = i[0]
        discordID = int(i[4])
        site = "https://niftys.com/api/user/" + niftysAccount + "/nfts/collected?skip=0&take=50"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        skip = 0
        more = True
        listOfAvatars = []
        while more:
            await asyncio.sleep(2)
            opener = build_opener(HTTPCookieProcessor())
            try:
                fp = urllib.request.Request(site, headers = hdr)
            except:
                await channel.send("There was an error trying to load " + site)
                more = False
            else:
                try:
                    fp = opener.open(fp)
                except HTTPError as e:
                    content = e.read()
                else:
                    mybytes = fp.read()
                    mystr = mybytes.decode("utf8")
                    fp.close()
                    data = json.loads(mystr)
                    if data['nfts'] == []:
                        more = False
                    else:
                        for i in data['nfts']:
                            if i['contractAddress'] == "0x28e4b03bc88b59d25f3467b2252b66d4b2c43286":
                                pill = "Red"
                                listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                            elif i['contractAddress'] == "0x423e540cb46db0e4df1ac96bcbddf78a804647d8":
                                pill = "Blue"
                                listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                            elif i['contractAddress'] == "0x39ceaa47306381b6d79ad46af0f36bc5332386f2":
                                pill = "None"
                                listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                            elif i['contractAddress'] == "0x45c65dae6b82375b463183f4bc8b3c24534d583f":
                                spaceJamHolder = True
                            elif i['contractAddress'] == "0xd233cd3258bb148dff63895609296d16beca9e8b":
                                spaceJamHolder = True
                            elif i['contractAddress'] == "0x5654edeb96816d2287390418200ed58fdc20d0bd":
                                spaceJamHolder = True
                            elif i['contractAddress'] == "0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e":
                                tweetyHolder = True
                            elif i['contractAddress'] == "0x4a42fdf6f33226c03d68292de8113c96e78850ab":
                                tweetyHolder = True
                            elif i['contractAddress'] == "0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b":
                                sylvesterHolder = True
                            elif i['contractAddress'] == "0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903":
                                bugsHolder = True 
                            elif i['contractAddress'] == "0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069":
                                bulletTrainHolder = True
                            elif i['contractAddress'] == "0xf49e01cf705d5b1cd96b709c4594de9ce436f319" and i['tokenId'] == "9362513085312267681642":
                                whiteBeltHolder = True
                            elif i['contractAddress'] == "0xf49e01cf705d5b1cd96b709c4594de9ce436f319" and i['tokenId'] == "8646147303727552590442":
                                photocopierPassHolder = True
                            elif i['contractAddress'] == "0xc926101089c49c57ecc64006f47a5365dc6d9786" and i['tokenId'] == "62576289420822":
                                workingPhoneHolder = True
                            elif i['contractAddress'] == "0x354d0bc7ad5914da9431124be01927c47e01ae2d":
                                gotHolder = True
                            elif i['contractAddress'] == "0x2bd016017e1f6a7d0948334017e9037028dede98":
                                if i['attributes']['open'] == 'no':
                                    gotUnopenedHolder = True
                        skip += 50
                        site = "https://niftys.com/api/user/" + niftysAccount + "/nfts/collected?skip=" + str(skip) + "&take=50"
        #update Space Jam Holder role
        member = discord.utils.get(guild.members, id=discordID)
        if member != None:
            if spaceJamHolder:
                await member.add_roles(spaceJamHolderRole)
            else:
                await member.remove_roles(spaceJamHolderRole)
            if tweetyHolder:
                await member.add_roles(tweetyHolderRole)
            else:
                await member.remove_roles(tweetyHolderRole)
            if sylvesterHolder:
                await member.add_roles(sylvesterHolderRole)
            else:
                await member.remove_roles(sylvesterHolderRole)
            if bugsHolder:
                await member.add_roles(bugsHolderRole)
            else:
                await member.remove_roles(bugsHolderRole)
            if bulletTrainHolder:
                await member.add_roles(bulletTrainHolderRole)
            else:
                await member.remove_roles(bulletTrainHolderRole)
            if workingPhoneHolder:
                await member.add_roles(workingPhoneHolderRole)
            else:
                await member.remove_roles(workingPhoneHolderRole)
            if photocopierPassHolder:
                await member.add_roles(photocopierPassHolderRole)
            else:
                await member.remove_roles(photocopierPassHolderRole)
            if whiteBeltHolder:
                await member.add_roles(whiteBeltHolderRole)
            else:
                await member.remove_roles(whiteBeltHolderRole)
            if gotHolder:
                await member.add_roles(gotHolderRole)
            else:
                await member.remove_roles(gotHolderRole)
            if gotUnopenedHolder:
                await member.add_roles(gotUnopenedHolderRole)
            else:
                await member.remove_roles(gotUnopenedHolderRole)
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "update niftysAccounts set space_jam_holder = {0} where account_name = '{1}'".format(spaceJamHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set tweety_holder = {0} where account_name = '{1}'".format(tweetyHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set sylvester_holder = {0} where account_name = '{1}'".format(sylvesterHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set bugs_holder = {0} where account_name = '{1}'".format(bugsHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set bullet_train_holder = {0} where account_name = '{1}'".format(bulletTrainHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set white_belt_holder = {0} where account_name = '{1}'".format(whiteBeltHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set copier_pass_holder = {0} where account_name = '{1}'".format(photocopierPassHolder, niftysAccount)
        cur.execute(command)
        command = "update niftysAccounts set working_phone_holder = {0} where account_name = '{1}'".format(workingPhoneHolder, niftysAccount)
        cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()
        for m in listOfAvatars:        
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select pilled from avatars where token_id = '{0}'".format(m[0])
            cur.execute(command)
            currentPill = cur.fetchall()
            currentPill = currentPill[0]
            command = "UPDATE avatars set owner_handle = '{0}' where token_id = '{1}'".format(niftysAccount, m[0])
            cur.execute(command)
            if currentPill != "Blue" and currentPill != "Red":
                command = "UPDATE avatars set pilled = '{0}' where token_id = '{1}'".format(m[1], m[0])
                cur.execute(command)
                for attribute in m[2]:
                    tableColumn = attribute.lower()
                    i = 0
                    while i < len(tableColumn):
                        if tableColumn[i] == " " or tableColumn[i] == "-" or tableColumn[i] == ":":
                            tableColumn = tableColumn[0:i] + "_" + tableColumn[i+1:]
                        i += 1
                    i = 0
                    value = m[2][attribute]
                    x = len(value)
                    while i < x:
                        if value[i] == "'":
                            value = value[0:i] + "'" + value[i:]
                            i+=1
                        i += 1
                    command = "UPDATE avatars set {0} = '{1}' where token_id = '{2}'".format(tableColumn,value, m[0])
                    cur.execute(command)
            cur.close()
            conn.commit()
            conn.close()

async def banNiftys(guild):
    for member in guild.members:
        if member.name == "Νіfty'ѕ":
            await member.ban()

bot.run(TOKEN)
