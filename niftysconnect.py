import os
import random
import urllib.request
from urllib.request import build_opener, HTTPCookieProcessor
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

load_dotenv()

TOKEN = os.environ.get('NIFTYS_CONNECT_TOKEN')
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
bot = commands.Bot(command_prefix="+", intents=intents)

#Defines the walletconnect command
@bot.command(name='walletconnect')
async def walletconnect(ctx, wallet):
    if ctx.channel.id != 971831743185297448:
        return
    user_message = ctx.message
    commandUser = ctx.message.author
    commandUserString = str(ctx.message.author)
    location = commandUserString.find("'")
    if location != -1:
        while location != -1:
            commandUserString = commandUserString[:location] + "'" + commandUserString[location:]
            location = commandUserString.find("'", location +2)
    wallet = wallet.lower()
    #First checks the SQL server to see if the wallet has already been entered
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from wallets where wallet = '{0}'".format(wallet)
    cur.execute(command)
    searchResult = cur.fetchall()
    #If the wallet given is not in the SQL table:
    if searchResult == []:
        if len(wallet) == 42 and wallet[:2]=="0x":
            command = "select * from wallets where discord_user_id = {0}".format(commandUser.id)
            cur.execute(command)
            currentWallets = cur.fetchall()
            if currentWallets == []:
                command = "INSERT INTO wallets (wallet, discord_user, discord_user_id) values ('{0}', '{1}', {2})".format(wallet,commandUserString, commandUser.id)
                cur.execute(command)
            else:
                command = "INSERT INTO wallets (wallet, discord_user, discord_user_id, default_wallet) values ('{0}', '{1}', {2}, 0)".format(wallet,commandUserString, commandUser.id)
                cur.execute(command)
            await user_message.delete()
            await ctx.send("Success! Wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " is now linked with your Discord profile, " + commandUser.mention)
        else:
            await ctx.send("This does not seem to be an existing wallet address. Please make sure you are providing a wallet in the format '0x0000000000000000000000000000000000000000' and try again")
    else:
        await user_message.delete()
        if str(searchResult[0][3]) == str(commandUser.id):
            await ctx.send("Wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " is already tied to Discord user <@" + str(searchResult[0][3]) + ">.")
        else:
            await ctx.send("Wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " is already tied to Discord user <@" + str(searchResult[0][3]) + ">. If you feel this is not correct, please dm <@710139786404298822> and he will help you address this.")
    cur.close()
    conn.commit()
    conn.close()
        
#Defines the niftysconnect command
@bot.command(name='niftysconnect')
async def niftysconnect(ctx, niftysAccount):
    if ctx.channel.id != 971831743185297448:
        return
    purpleCapRole = ctx.guild.get_role(958871211625021520)
    matrixHolderRole = ctx.guild.get_role(959137823317950464)
    spaceJamHolderRole = ctx.guild.get_role(979455341009985627)
    tweetyHolderRole = ctx.guild.get_role(988786072760774696)
    sylvesterHolderRole = ctx.guild.get_role(1024693150482169967)
    bugsHolderRole = ctx.guild.get_role(1024701273347465377)
    bulletTrainHolderRole = ctx.guild.get_role(1024692977261621298)
    workingPhoneHolderRole = ctx.guild.get_role(1052614060102930473)
    whiteBeltHolderRole = ctx.guild.get_role(1052614164742426645)
    photocopierPassHolderRole= ctx.guild.get_role(1052614266324262912)
    gotHolderRole = ctx.guild.get_role(1062491726977183836)
    gotUnopenedHolderRole = ctx.guild.get_role(1062562145235120191)
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
    commandUser = ctx.message.author
    commandUserString = str(ctx.message.author)
    location = commandUserString.find("'")
    if location != -1:
        while location != -1:
            commandUserString = commandUserString[:location] + "'" + commandUserString[location:]
            location = commandUserString.find("'", location +2)
    niftysAccount = niftysAccount.lower()
    #First checks the SQL server to see if the nifty's account is already in the system
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from niftysAccounts where account_name = '{0}'".format(niftysAccount)
    cur.execute(command)
    searchResult = cur.fetchall()
    cur.close()
    conn.close()
    #If the account given is not in the SQL table:
    if searchResult == []:
        waiting = True
        while waiting:
            try:
                response = requests.get('https://api.niftys.com/v1/public/accounts/' + niftysAccount, headers=niftysAPIHeaders)
            except:
                await ctx.send("There was an issue connecting to the Nifty's site. Please try again.")
                waiting = False
            else:
                try:
                    data = json.loads(response.text)
                except:
                    await ctx.send("There was an issue connecting to the Nifty's site. Please try again.")
                    waiting = False
                else:
                    if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                        if niftysAccount[0]=="@":
                            await ctx.send("Nifty's user " + niftysAccount + " does not exist. Maybe try again without the '@'?")
                            waiting = False
                        else:
                            await ctx.send("Nifty's user " + niftysAccount + " does not exist.")
                            waiting = False
                    else:
                        try:
                            accountID = data['data']['handle']
                        except:
                            ctx.send("There is currently a large load on Nifty's site. Please wait, " + commandUser + ". I will try again in ten seconds.")
                            await asyncio.sleep(10)
                        else:
                            waiting = False
                            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                            cur = conn.cursor()
                            command = "INSERT INTO niftysAccounts (account_id, account_name, discord_user, discord_user_id) values ('{0}', '{1}', '{2}', '{3}')".format(accountID,niftysAccount,commandUserString,commandUser.id)
                            cur.execute(command)
                            cur.close()
                            conn.commit()
                            conn.close()
                            await ctx.send("Discord user " + commandUser.mention + " is now tied to the " + niftysAccount + " handle on Nifty's. Updating your owned NFT's now. It may take up to 10-15 minutes for everything to update.")
                            site = "https://niftys.com/api/user/" + niftysAccount + "/nfts/collected?skip=0&take=50"
                            hdr = {'User-Agent': 'Mozilla/5.0'}
                            skip = 0
                            more = True
                            listOfAvatars = []
                            while more:
                                opener = build_opener(HTTPCookieProcessor())
                                fp = urllib.request.Request(site, headers = hdr)
                                fp = opener.open(fp)
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
                                            matrixHolder = True
                                        elif i['contractAddress'] == "0x423e540cb46db0e4df1ac96bcbddf78a804647d8":
                                            pill = "Blue"
                                            listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                                            matrixHolder = True
                                        elif i['contractAddress'] == "0x39ceaa47306381b6d79ad46af0f36bc5332386f2":
                                            pill = "None"
                                            listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                                            matrixHolder = True
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
                                        elif i['contractAddress'] =="0x354d0bc7ad5914da9431124be01927c47e01ae2d":
                                            gotHolder = True
                                        elif i['contractAddress'] == "0x2bd016017e1f6a7d0948334017e9037028dede98":
                                            if i['attributes']['open'] == 'no':
                                                gotUnopenedHolder = True
                                    skip += 50
                                    site = "https://niftys.com/api/user/" + niftysAccount + "/nfts/collected?skip=" + str(skip) + "&take=50"
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
                                command = "UPDATE avatars set owner_handle = '{0}' where token_id = '{1}'".format(niftysAccount, m[0])
                                cur.execute(command)
                                command = "UPDATE avatars set pilled = '{0}' where token_id = '{1}'".format(m[1], m[0])
                                cur.execute(command)
                                for attribute in m[2]:
                                    tableColumn = attribute.lower()
                                    if tableColumn == "headwear":
                                        if m[2][attribute] == "Purple Workers Cap" or m[2][attribute] == "Purple Worker's Cap":
                                            purpleCapHolder = True
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
        if matrixHolder:
            await commandUser.add_roles(matrixHolderRole)
        else:
            await commandUser.remove_roles(matrixHolderRole)
        if purpleCapHolder:
            await commandUser.add_roles(purpleCapRole)
        else:
            await commandUser.remove_roles(purpleCapRole)
        if spaceJamHolder:
            await commandUser.add_roles(spaceJamHolderRole)
        else:
            await commandUser.remove_roles(spaceJamHolderRole)
        if tweetyHolder:
            await commandUser.add_roles(tweetyHolderRole)
        else:
            await commandUser.remove_roles(tweetyHolderRole)
        if sylvesterHolder:
            await commandUser.add_roles(sylvesterHolderRole)
        else:
            await commandUser.remove_roles(sylvesterHolderRole)
        if bugsHolder:
            await commandUser.add_roles(bugsHolderRole)
        else:
            await commandUser.remove_roles(bugsHolderRole)
        if bulletTrainHolder:
            await commandUser.add_roles(bulletTrainHolderRole)
        else:
            await commandUser.remove_roles(bulletTrainHolderRole)
        if workingPhoneHolder:
            await commandUser.add_roles(workingPhoneHolderRole)
        else:
            await commandUser.remove_roles(workingPhoneHolderRole)
        if photocopierPassHolder:
            await commandUser.add_roles(photocopierPassHolderRole)
        else:
            await commandUser.remove_roles(photocopierPassHolderRole)
        if whiteBeltHolder:
            await commandUser.add_roles(whiteBeltHolderRole)
        else:
            await commandUser.remove_roles(whiteBeltHolderRole)
        if gotHolder:
            await commandUser.add_roles(gotHolderRole)
        else:
            await commandUser.remove_roles(gotHolderRole)
        if gotUnopenedHolder:
            await commandUser.add_roles(gotUnopenedHolderRole)
        else:
            await commandUser.remove_roles(gotUnopenedHolderRole)
    else:
        if str(commandUser.id) == str(searchResult[0][4]):
            await ctx.send("The Nifty's account " + niftysAccount + " is already tied to Discord user <@" + str(searchResult[0][4]) + ">.")
        else:
            await ctx.send("The Nifty's account " + niftysAccount + " is already tied to Discord user <@" + str(searchResult[0][4]) + ">. If you feel this is not correct, please dm <@710139786404298822> and he will help you address this.")

#Defines the niftysconnect command
@bot.command(name='refresh')
async def refresh(ctx):
    if ctx.channel.id != 971831743185297448:
        return
    purpleCapRole = ctx.guild.get_role(958871211625021520)
    matrixHolderRole = ctx.guild.get_role(959137823317950464)
    spaceJamHolderRole = ctx.guild.get_role(979455341009985627)
    tweetyHolderRole = ctx.guild.get_role(988786072760774696)
    sylvesterHolderRole = ctx.guild.get_role(1024693150482169967)
    bugsHolderRole = ctx.guild.get_role(1024701273347465377)
    bulletTrainHolderRole = ctx.guild.get_role(1024692977261621298)
    workingPhoneHolderRole = ctx.guild.get_role(1052614060102930473)
    whiteBeltHolderRole = ctx.guild.get_role(1052614164742426645)
    photocopierPassHolderRole= ctx.guild.get_role(1052614266324262912)
    gotHolderRole = ctx.guild.get_role(1062491726977183836)
    gotUnopenedHolderRole = ctx.guild.get_role(1062562145235120191)
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
    commandUser = ctx.message.author
    #First checks the SQL server to see if the nifty's account is already in the system
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select account_id from niftysAccounts where discord_user_id = '{0}'".format(commandUser.id)
    cur.execute(command)
    searchResult = cur.fetchall()
    cur.close()
    conn.close()
    #If the account given is in the SQL table:
    if searchResult != []:
        await ctx.send("Updating your owned NFT's now. It may take up to 10-15 minutes for everything to update.")
        for niftysAccount in searchResult:
            niftysAccount = niftysAccount[0]
            site = "https://niftys.com/api/user/" + niftysAccount + "/nfts/collected?skip=0&take=50"
            hdr = {'User-Agent': 'Mozilla/5.0'}
            skip = 0
            more = True
            listOfAvatars = []
            while more:
                opener = build_opener(HTTPCookieProcessor())
                fp = urllib.request.Request(site, headers = hdr)
                fp = opener.open(fp)
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
                            matrixHolder = True
                        elif i['contractAddress'] == "0x423e540cb46db0e4df1ac96bcbddf78a804647d8":
                            pill = "Blue"
                            listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                            matrixHolder = True
                        elif i['contractAddress'] == "0x39ceaa47306381b6d79ad46af0f36bc5332386f2":
                            pill = "None"
                            listOfAvatars.append([i['tokenId'],pill,i['attributes']])
                            matrixHolder = True
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
                        elif i['contractAddress'] =="0x354d0bc7ad5914da9431124be01927c47e01ae2d":
                            gotHolder = True
                        elif i['contractAddress'] == "0x2bd016017e1f6a7d0948334017e9037028dede98":
                            if i['attributes']['open'] == 'no':
                                gotUnopenedHolder = True
                    skip += 50
                    site = "https://niftys.com/api/user/" + niftysAccount + "/nfts/collected?skip=" + str(skip) + "&take=50"
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
                command = "UPDATE avatars set owner_handle = '{0}' where token_id = '{1}'".format(niftysAccount, m[0])
                cur.execute(command)
                command = "UPDATE avatars set pilled = '{0}' where token_id = '{1}'".format(m[1], m[0])
                cur.execute(command)
                for attribute in m[2]:
                    tableColumn = attribute.lower()
                    if tableColumn == "headwear":
                        if m[2][attribute] == "Purple Workers Cap" or m[2][attribute] == "Purple Worker's Cap":
                            purpleCapHolder = True
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
        if matrixHolder:
            await commandUser.add_roles(matrixHolderRole)
        else:
            await commandUser.remove_roles(matrixHolderRole)
        if purpleCapHolder:
            await commandUser.add_roles(purpleCapRole)
        else:
            await commandUser.remove_roles(purpleCapRole)
        if spaceJamHolder:
            await commandUser.add_roles(spaceJamHolderRole)
        else:
            await commandUser.remove_roles(spaceJamHolderRole)
        if tweetyHolder:
            await commandUser.add_roles(tweetyHolderRole)
        else:
            await commandUser.remove_roles(tweetyHolderRole)
        if sylvesterHolder:
            await commandUser.add_roles(sylvesterHolderRole)
        else:
            await commandUser.remove_roles(sylvesterHolderRole)
        if bugsHolder:
            await commandUser.add_roles(bugsHolderRole)
        else:
            await commandUser.remove_roles(bugsHolderRole)
        if bulletTrainHolder:
            await commandUser.add_roles(bulletTrainHolderRole)
        else:
            await commandUser.remove_roles(bulletTrainHolderRole)
        if workingPhoneHolder:
            await commandUser.add_roles(workingPhoneHolderRole)
        else:
            await commandUser.remove_roles(workingPhoneHolderRole)
        if photocopierPassHolder:
            await commandUser.add_roles(photocopierPassHolderRole)
        else:
            await commandUser.remove_roles(photocopierPassHolderRole)
        if whiteBeltHolder:
            await commandUser.add_roles(whiteBeltHolderRole)
        else:
            await commandUser.remove_roles(whiteBeltHolderRole)
        if gotHolder:
            await commandUser.add_roles(gotHolderRole)
        else:
            await commandUser.remove_roles(gotHolderRole)
        if gotUnopenedHolder:
            await commandUser.add_roles(gotUnopenedHolderRole)
        else:
            await commandUser.remove_roles(gotUnopenedHolderRole)
    else:
        await ctx.send("It doesn't look like you've linked your Nifty's account using the +niftysconnect command yet! Please see <#971831707735056394> for more information.")

#Defines the niftyconnect command (because people make that typo a lot)
@bot.command(name='niftyconnect')
async def niftyconnect(ctx, niftysAccount):
    if ctx.channel.id != 971831743185297448:
        return
    await niftysconnect(ctx, niftysAccount)

class MyView(View):
    
    def __init__(self, ctx):
        super().__init__(timeout = 10)
        self.ctx = ctx

    async def on_timeout(self):
        #self.clear_items()
        for i in self.children:
            if isinstance(i, Button):
                i.disabled = True
        for i in self.children:
            if isinstance(i, Select):
                self.remove_item(i)
        await self.message.edit(view = self)

async def myConnectionsHome(view, commandUser):
    view.clear_items()
    niftysAccountsButton = Button(label="Your Nifty's Accounts", style = discord.ButtonStyle.blurple)
    walletsButton = Button(label="Your Wallets", style = discord.ButtonStyle.blurple)
    
    async def niftysAccountsButton_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:   
            await interaction.response.defer()
            await niftysAccountsMenu(view, commandUser)
        
    async def walletsButton_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            await interaction.response.defer()
            await walletMenu(view, commandUser)

    niftysAccountsButton.callback = niftysAccountsButton_callback
    walletsButton.callback = walletsButton_callback

    view.add_item(niftysAccountsButton)
    view.add_item(walletsButton)

    await view.message.edit(content = str(commandUser) + "'s connections:", view = view)

async def niftysAccountsMenu(view, commandUser):
    view.clear_items()
    await view.message.edit(content = "Your Linked Nifty's Accounts", view = view)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from niftysAccounts where discord_user_id = '{0}'".format(str(commandUser.id))
    cur.execute(command)
    handles = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()

    async def myConnectionsHomeButton_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            await interaction.response.defer()
            await myConnectionsHome(view, commandUser)

    async def select_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            select.placeholder=select.values[0]
            view.clear_items()
            view.add_item(select)
            view.add_item(offerPingsButton)
            view.add_item(unlinkButton)
            view.add_item(myConnectionsHomeButton)
            await interaction.response.edit_message(view = view)

    async def offer_pings_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            handle = select.values[0]

            async def yesButton_callback(interaction):
                if commandUser != interaction.user:
                    await interaction.response.send_message("This is not your menu.", ephemeral = True)
                else:
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update niftysAccounts set offer_updates = 1 where discord_user_id = '{0}' and account_name = '{1}'".format(str(commandUser.id), handle)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    view.clear_items()
                    await interaction.response.edit_message(content = "You will now begin receiving notifications when offers are placed on NFT's owned by the " + handle + " Nifty's account.", view = view)

            async def noButton_callback(interaction):
                if commandUser != interaction.user:
                    await interaction.response.send_message("This is not your menu.", ephemeral = True)
                else:
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update niftysAccounts set offer_updates = 0 where discord_user_id = '{0}' and account_name = '{1}'".format(str(commandUser.id), handle)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    view.clear_items()
                    await interaction.response.edit_message(content = "You will no longer receive notifications when offers are placed on NFT's owned by the " + handle + " Nifty's account.", view = view)

            yesButton = Button(label="Yes", style = discord.ButtonStyle.blurple)
            yesButton.callback = yesButton_callback
            noButton = Button(label="No", style = discord.ButtonStyle.blurple)
            noButton.callback = noButton_callback

            view.clear_items()
            view.add_item(yesButton)
            view.add_item(noButton)
            await interaction.response.edit_message(content = "Would you like to receive notifications when offers are placed on NFT's owned by the " + handle + " Nifty's account?", view = view)
            
    async def unlink_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            handle = select.values[0]

            async def yesButton_callback(interaction):
                if commandUser != interaction.user:
                    await interaction.response.send_message("This is not your menu.", ephemeral = True)
                else:
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "delete from niftysAccounts where discord_user_id = '{0}' and account_name = '{1}'".format(str(commandUser.id), handle)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    view.clear_items()
                    await interaction.response.edit_message(content = "Niftys handle " + handle + " has been successfully unlinked from your Discord account.", view = view)

            async def noButton_callback(interaction):
                if commandUser != interaction.user:
                    await interaction.response.send_message("This is not your menu.", ephemeral = True)
                else:
                    await interaction.response.defer()
                    await niftysAccountsMenu(view, commandUser)

            yesButton = Button(label="Yes", style = discord.ButtonStyle.blurple)
            yesButton.callback = yesButton_callback
            noButton = Button(label="No", style = discord.ButtonStyle.blurple)
            noButton.callback = noButton_callback

            view.clear_items()
            view.add_item(yesButton)
            view.add_item(noButton)
            await interaction.response.edit_message(content = "Are you sure you want to unlink the Nifty's handle " + handle + " from your Discord account?", view = view)

    myConnectionsHomeButton = Button(label="Main Menu", style = discord.ButtonStyle.blurple)
    myConnectionsHomeButton.callback = myConnectionsHomeButton_callback
    unlinkButton = Button(label="Unlink this Handle", style = discord.ButtonStyle.blurple)
    unlinkButton.callback = unlink_button_callback
    offerPingsButton = Button(label="Offer Notifications", style = discord.ButtonStyle.blurple)
    offerPingsButton.callback = offer_pings_button_callback
    
    if handles == []:
        await view.message.edit(content = "There are currently no Nifty's handles associated with Discord user <@" + str(commandUser.id) +">. Please use the +niftysconnect command to link your Nifty's handle(s) to your Discord account!", view = view)
    else:
        options = []
        for i in handles:
            options.append(discord.SelectOption(label=i[1]))
        select = Select(row = 0,
            placeholder = "Choose a Nifty's Handle!",
            options=options)
        select.callback = select_callback
        view.add_item(select)
    
    view.add_item(myConnectionsHomeButton)
    await view.message.edit(view = view)

async def walletMenu(view, commandUser):
    view.clear_items()
    await view.message.edit(content = "Your Linked Wallets", view = view)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from wallets where discord_user_id = {0}".format(commandUser.id)
    cur.execute(command)
    wallets = cur.fetchall()
    cur.close()
    conn.close()

    async def myConnectionsHomeButton_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            await interaction.response.defer()
            await myConnectionsHome(view, commandUser)

    async def select_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            select.placeholder=select.values[0]
            view.clear_items()
            view.add_item(select)
            view.add_item(defaultButton)
            view.add_item(unlinkButton)
            view.add_item(myConnectionsHomeButton)
            await interaction.response.edit_message(view = view)
            
    async def default_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            wallet = select.values[0]
            wallet = wallet[:42]
            default = select.values[0][len(select.values[0])-7:]
            if default == "Default":
                default = True
                view.clear_items()
                await interaction.response.edit_message(content = "Wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " is already your default wallet!", view = view)
            else:
                default = False
                conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                cur = conn.cursor()
                command = "select * from wallets where discord_user_id = {0} and default_wallet = 1".format(commandUser.id)
                cur.execute(command)
                currentDefault = cur.fetchall()
                command = "update wallets set default_wallet = 0 where wallet = '{0}'".format(currentDefault[0][0])
                cur.execute(command)
                command = "update wallets set default_wallet = 1 where wallet = '{0}'".format(wallet)
                cur.execute(command)
                cur.close()
                conn.commit()
                conn.close()
                view.clear_items()
                await interaction.response.edit_message(content = "Wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " is now your default wallet!", view = view)

    async def unlink_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            wallet = select.values[0]
            wallet = wallet[:42]
            default = select.values[0][len(select.values[0])-7:]
            if default == "Default":
                default = True
            else:
                default = False

            async def yesButton_callback(interaction):
                conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                cur = conn.cursor()
                command = "delete from wallets where discord_user_id = {0} and wallet = '{1}'".format(commandUser.id, wallet)
                cur.execute(command)
                cur.close()
                conn.commit()
                conn.close()
                if default:
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select * from wallets where discord_user_id = {0}".format(commandUser.id)
                    cur.execute(command)
                    wallets = cur.fetchall()
                    if wallets != []:
                        command = "update wallets set default_wallet = 1 where wallet = '{0}'".format(wallets[0][0])
                        cur.execute(command)
                        cur.close()
                        conn.commit()
                        conn.close()
                view.clear_items()
                await interaction.response.edit_message(content = "Wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " has been successfully unlinked from your Discord account.", view = view)

            async def noButton_callback(interaction):
                await interaction.response.defer()
                await walletMenu(view, commandUser)

            yesButton = Button(label="Yes", style = discord.ButtonStyle.blurple)
            yesButton.callback = yesButton_callback
            noButton = Button(label="No", style = discord.ButtonStyle.blurple)
            noButton.callback = noButton_callback

            view.clear_items()
            view.add_item(yesButton)
            view.add_item(noButton)
            await interaction.response.edit_message(content = "Are you sure you want to unlink wallet " + wallet[:6] + "..." + wallet[len(wallet)-6:] + " from your Discord account?", view = view)

    myConnectionsHomeButton = Button(label="Main Menu", style = discord.ButtonStyle.blurple)
    myConnectionsHomeButton.callback = myConnectionsHomeButton_callback
    unlinkButton = Button(label="Unlink this Wallet", style = discord.ButtonStyle.blurple)
    unlinkButton.callback = unlink_button_callback
    defaultButton = Button(label="Make Default", style = discord.ButtonStyle.blurple)
    defaultButton.callback = default_button_callback

    if wallets == []:
        await view.message.edit(content = "There are currently no wallets associated with Discord user <@" + str(commandUser.id) +">. Please use the +walletconnect command to link your wallet(s) to your Discord account!", view = view)
    else:
        options = []
        for i in wallets:
            wallet = i[0]
            if i[2] == 1:
                options.append(discord.SelectOption(label= wallet + " - Default"))
            else:
                options.append(discord.SelectOption(label=wallet))
        select = Select(row = 0,
            placeholder = "Choose a Wallet!",
            options=options)
        select.callback = select_callback
        view.add_item(select)
    
        view.add_item(myConnectionsHomeButton)
        await view.message.edit(view = view)
        
        await view.message.edit(content = "Your Linked Wallets", view = view)
    
    

#Defines the niftysconnect command
@bot.command(name='myconnections')
async def myconnections(ctx):
    if ctx.channel.id != 971831743185297448:
        return
    commandUser = ctx.message.author
    view = MyView(ctx)
    view.message = await ctx.send(str(commandUser) + "'s connections:", view = view)
    await myConnectionsHome(view, commandUser)
    

#Runs the bot using the TOKEN defined in the environmental variables.         
bot.run(TOKEN)
