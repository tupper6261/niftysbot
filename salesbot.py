#Nifty's Sales Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.0 - June 10, 2022

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

#Grab my oauth tokens
TOKEN = os.getenv('SALES_BOT_TOKEN')
DATABASETOKEN = os.getenv('DATABASE_URL')

#Set my Nifty's API call headers
niftysAuthorization = os.getenv('NIFTYS_BEARER_TOKEN')
niftysAuthKeyID = os.getenv('NIFTYS_AUTH_KEY')

niftysAPIHeaders = {
    'accept': 'application/json',
    'Authorization': niftysAuthorization,
    'auth-key-id': niftysAuthKeyID,
}

#List of 721 contracts
contracts = ['0x39ceaa47306381b6d79ad46af0f36bc5332386f2','0x423e540cb46db0e4df1ac96bcbddf78a804647d8','0x28e4b03bc88b59d25f3467b2252b66d4b2c43286',
             '0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e', '0x4a42fdf6f33226c03d68292de8113c96e78850ab', '0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b',
             '0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903', '0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069', '0x048035859089a9b13a3f1cc686a5f19f6375e073',
             '0x2bd016017e1f6a7d0948334017e9037028dede98', '0x354d0bc7ad5914da9431124be01927c47e01ae2d']
contractNames = ['unpilled','blue','red',
                 'tweety', 'tweetyeth', 'sylvester',
                 'bugs', 'bullet train', 'matrix rewards',
                 'hero box', 'north series 1 avatar']

client = discord.Client()
#Discord requires to specify specific intents for bots. The following three lines essentially say that my bot could potentially require all bot features. 
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
#This initializes a bot 
bot = commands.Bot(intents=intents)

#This method runs when the bot boots up.
@bot.event
async def on_ready():
    while True:
        await gotMints()
        await btMints()
        await tweetyEthMints()
        await tweetyPalmMints()
        await sylvesterMints()
        await bugsMints()
        await updateSales()
        await updateOffers()

async def updateSales():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    #Builds a channel object based on the sales channel in which we want to post sales
    ctx = discord.utils.get(guild.channels, id = 984916401187848193)

    #For each contract in the list of 721's
    for contract in contracts:
        #Pulls 20 completed offers for that contract
        try:
            response = requests.get('https://api.niftys.com/v1/public/offers?contractAddress=' + contract + '&orderByDirection=desc&status=COMPLETED&take=20', headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            #Convert the JSON into a Python dictionary
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                #Keeps looping through until the flag is set
                finished = False
                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    finished = True
                while finished == False:
                    if data != {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        #Grab the pagination cursor before we dive into the individual offers
                        paginationCursor = data['paginationCursor']
                        #For each offer in the batch of 20 we just grabbed
                        for currentOffer in data['data']:
                            #Put the relevant JSON data into variables to make life easier and/or format correctly
                            offerPrice = currentOffer['price']
                            if contract in ['0x4a42fdf6f33226c03d68292de8113c96e78850ab', '0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b',
                                            '0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903', '0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069', '0x048035859089a9b13a3f1cc686a5f19f6375e073',
                                            '0x2bd016017e1f6a7d0948334017e9037028dede98', '0x354d0bc7ad5914da9431124be01927c47e01ae2d']:
                                offerPrice = round((float(offerPrice)/1000000),2)
                            else:
                                offerPrice = round((float(offerPrice)/1000000000000000000),2)
                            tokenId = currentOffer['tokenId']
                            contractAddress = currentOffer['contractAddress']
                            createdAt = currentOffer['createdAt']
                            date_str_no_z = createdAt[:-1]# remove last z
                            #This converts the timestamp string into a unix timestamp
                            dt_obj = datetime.datetime.strptime(date_str_no_z, "%Y-%m-%dT%H:%M:%S.%f")
                            unix_time = dt_obj.timestamp()
                            #If this offer is more than 31 days (2678400 seconds) old, we're gonna stop looking for offers
                            if int(unix_time) + 2678400 < int(time.time()):
                                finished = True
                            #Check to see if the current offer has already been found and communicated
                            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                            cur = conn.cursor()
                            command = "select * from completedSales where offer_id = '{0}'".format(currentOffer['id'])
                            cur.execute(command)
                            searchResult = cur.fetchall()
                            #If it hasn't already been posted:
                            if searchResult == []:
                                #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                await asyncio.sleep(2)
                                #Grab the pill info and current owner of this avatar
                                response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+tokenId+'&contractAddress='+contractAddress, headers=headers)
                                #Convert the JSON into a Python dictionary
                                data = json.loads(response.text)
                                #Pilling events show up as completed offers, so if the current owner is null, we ignore this one
                                if data != {'data': [], 'total': 0, 'paginationCursor': None}:
                                    #First checks to see if this is a Palm Tweety
                                    if contractAddress == contracts[3]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/PALM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #Then checks to see if this is an Eth Tweety
                                    elif contractAddress == contracts[4]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #Then checks to see if this is a Sylvester
                                    elif contractAddress == contracts[5]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #Then checks to see if this is a Bugs
                                    elif contractAddress == contracts[6]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                        
                                    #Then checks to see if this is a bullet train
                                    elif contractAddress == contracts[7]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #Then checks to see if this is a matrix reward
                                    elif contractAddress == contracts[8]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        if int(tokenId)<26:
                                            tweetyNumber = "The Nebuchadnezzar"
                                        else:
                                            tweetyNumber = "The Sentinel"
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #Then checks to see if this is a Game of Thrones The North Series 1 Hero Box
                                    elif contractAddress == contracts[9]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #Then checks to see if this is a Game of Thrones The North Avatar
                                    elif contractAddress == contracts[10]:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            return
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                return
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    return
                                                else:
                                                    tweetyNumber = data['name']
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                    '''
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = tweetyNumber
                                        #Sets the message content
                                        embed.description = tweetyNumber + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                    #It must be a Matrix avatar
                                    else:
                                        #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                        await asyncio.sleep(2)
                                        try:
                                            #Grab the pill info and current owner of this avatar
                                            response = requests.get('https://api.niftys.com/v1/public/metadata/PALM/'+contractAddress+'/'+tokenId, headers=headers)
                                        except Exception as e:
                                            await errors.send(e)
                                            avatarImageURL = ""
                                        else:
                                            try:
                                                #Convert the JSON into a Python dictionary
                                                data = json.loads(response.text)
                                            except Exception as e:
                                                await errors.send(e)
                                                avatarImageURL = ""
                                            else:
                                                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                    avatarImageURL = ""
                                                else:
                                                    avatarImageURL = data['image']
                                                    '''
                                                    dimAdjust = avatarImageURL.find("/v3-prod")
                                                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/420x630" + avatarImageURL[dimAdjust:]
                                                    '''
                                        #Sets a string variable with the pill status to be used later
                                        if contractAddress == contracts[0]:
                                            pilled = "Unpilled"
                                        elif contractAddress == contracts[1]:
                                            pilled = "Blue-pilled"
                                        elif contractAddress == contracts[2]:
                                            pilled = "Red-pilled"
                                        avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                        #Builds a Discord embed object for our message and sets the bar color
                                        embed = discord.Embed(color=0x000000)
                                        #Sets the thumbnail image
                                        embed.set_thumbnail(url=avatarImageURL)
                                        #Sets the title
                                        embed.title = "Matrix Avatar "+tokenId
                                        #Sets the message content
                                        embed.description = pilled + " avatar " + tokenId + " sold for $" + str(offerPrice) + ".\n\n"+avatarURL
                                        #Sends the message
                                        await ctx.send(embed=embed)
                                        #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                        command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                        cur.execute(command)
                                else:
                                    #add this sale into the database of sales we've already posted with a 64 day (5529600) expiration date so I can keep the database clean
                                    command = "insert into completedSales (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+5529600)
                                    cur.execute(command)
                            cur.close()
                            conn.commit()
                            conn.close()
                        if paginationCursor == None:
                            finished = True
                        else:
                            #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                            await asyncio.sleep(2)
                            #Pulls a new batch of 20 completed offers
                            try:
                                response = requests.get('https://api.niftys.com/v1/public/offers?contractAddress=' + contract + '&orderByDirection=desc&status=COMPLETED&take=20&paginationCursor='+paginationCursor, headers=headers)
                            except Exception as e:
                                await errors.send(e)
                            else:
                                #Convert the JSON into a Python dictionary
                                try:
                                    data = json.loads(response.text)
                                except Exception as e:
                                    await errors.send(e)
                                else:
                                    await asyncio.sleep(1)
                    else:
                        finished = True

async def tweetyPalmMints():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    tweetyMintChannel = discord.utils.get(guild.channels, id = 991063007377391776)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select latest_tweety_mint from serverVariables where row = '1'"
    cur.execute(command)
    avatarnumber = cur.fetchall()
    cur.close()
    conn.close()
    avatarnumber = avatarnumber[0][0]
    newMints = True
    while newMints:
        await asyncio.sleep(2)
        try:
            response = requests.get('https://api.niftys.com/v1/public/metadata/PALM/0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e/' + str(avatarnumber), headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
                    newMints = False
                elif data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Metadata not found.'}:
                    newMints = False
                elif data['attributes'] == []:
                    newMints = False
                else:
                    #Grab the avatar's image URL before we dive into the attribute data
                    avatarImageURL = data['image']
                    '''
                    dimAdjust = avatarImageURL.find("/v3-prod")
                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                    '''
                    avatarURL = "https://niftys.com/nft/0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e/"+str(avatarnumber)
                    avatar_name = data['name']
                    avatar_niftys_owner = "Retrieving..."
                    avatar_discord_owner = "Retrieving..."
                    avatar_eyes = ""
                    avatar_mouth = ""
                    avatar_facial_decoration = ""
                    avatar_shirt = ""
                    avatar_headband = ""
                    avatar_body = ""
                    avatar_neckwear = ""
                    avatar_environment = ""
                    avatar_handheld_prop = ""
                    avatar_looney_edition = ""
                    for attribute in data['attributes']:
                        if attribute['trait_type'] == 'Headwear':
                            avatar_headband = attribute['value']
                        if attribute['trait_type'] == 'Eyes':
                            avatar_eyes = attribute['value']
                        if attribute['trait_type'] == 'Mouth':
                            avatar_mouth = attribute['value']
                        if attribute['trait_type'] == 'Facial Decoration':
                            avatar_facial_decoration = attribute['value']
                        if attribute['trait_type'] == 'Body':
                            avatar_body = attribute['value']
                        if attribute['trait_type'] == 'Shirt':
                            avatar_shirt = attribute['value']
                        if attribute['trait_type'] == 'Neckwear':
                            avatar_neckwear = attribute['value']
                        if attribute['trait_type'] == 'Handheld Prop':
                            avatar_handheld_prop = attribute['value']
                        if attribute['trait_type'] == 'Environment':
                            avatar_environment = attribute['value']
                        if attribute['trait_type'] == 'Looney Edition':
                            avatar_looney_edition = attribute['value']
                    embed = discord.Embed(color=0xfffaa5)
                    embed.title = avatar_name + " (Token ID " + str(avatarnumber) + ")"
                    embed.set_thumbnail(url=avatarImageURL)
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    message = await tweetyMintChannel.send(embed = embed)
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update serverVariables set latest_tweety_mint = {0} where row = '1'".format(avatarnumber + 1)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    #Get Niftys owner
                    await asyncio.sleep(2)
                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+str(avatarnumber)+'&contractAddress=0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e', headers=headers)
                    data = json.loads(response.text)
                    if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data == {'data': [], 'total': 0, 'paginationCursor': None}:
                        avatar_niftys_owner = "unknown"
                    elif data['data'][0]['wallet']['account'] == None:
                        avatar_niftys_owner = "unknown"
                    else:
                        avatar_niftys_owner = data['data'][0]['wallet']['account']['handle']
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    await message.edit(embed = embed)
                    #Get discord owner
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_niftys_owner)
                    cur.execute(command)
                    avatar_discord_owner = cur.fetchall()
                    cur.close()
                    conn.close()
                    if avatar_discord_owner == []:
                        avatar_discord_owner = "unknown"
                    else:
                        avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    await message.edit(embed = embed)
                    avatarnumber += 1

async def tweetyEthMints():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    tweetyMintChannel = discord.utils.get(guild.channels, id = 991063007377391776)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select latest_tweety_mint from serverVariables where row = '1'"
    cur.execute(command)
    avatarnumber = cur.fetchall()
    cur.close()
    conn.close()
    avatarnumber = avatarnumber[0][0]
    newMints = True
    while newMints:
        await asyncio.sleep(2)
        try:
            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0x4a42fdf6f33226c03d68292de8113c96e78850ab/' + str(avatarnumber), headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
                    newMints = False
                elif data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Metadata not found.'}:
                    newMints = False
                elif data['attributes'] == []:
                    newMints = False
                else:
                    #Grab the avatar's image URL before we dive into the attribute data
                    avatarImageURL = data['image']
                    '''
                    dimAdjust = avatarImageURL.find("/v3-prod")
                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                    '''
                    avatarURL = "https://niftys.com/nft/0x4a42fdf6f33226c03d68292de8113c96e78850ab/"+str(avatarnumber)
                    avatar_name = data['name']
                    avatar_niftys_owner = "Retrieving..."
                    avatar_discord_owner = "Retrieving..."
                    avatar_eyes = ""
                    avatar_mouth = ""
                    avatar_facial_decoration = ""
                    avatar_shirt = ""
                    avatar_headband = ""
                    avatar_body = ""
                    avatar_neckwear = ""
                    avatar_environment = ""
                    avatar_handheld_prop = ""
                    avatar_looney_edition = ""
                    for attribute in data['attributes']:
                        if attribute['trait_type'] == 'Headwear':
                            avatar_headband = attribute['value']
                        if attribute['trait_type'] == 'Eyes':
                            avatar_eyes = attribute['value']
                        if attribute['trait_type'] == 'Mouth':
                            avatar_mouth = attribute['value']
                        if attribute['trait_type'] == 'Facial Decoration':
                            avatar_facial_decoration = attribute['value']
                        if attribute['trait_type'] == 'Body':
                            avatar_body = attribute['value']
                        if attribute['trait_type'] == 'Shirt':
                            avatar_shirt = attribute['value']
                        if attribute['trait_type'] == 'Neckwear':
                            avatar_neckwear = attribute['value']
                        if attribute['trait_type'] == 'Handheld Prop':
                            avatar_handheld_prop = attribute['value']
                        if attribute['trait_type'] == 'Environment':
                            avatar_environment = attribute['value']
                        if attribute['trait_type'] == 'Looney Edition':
                            avatar_looney_edition = attribute['value']
                    embed = discord.Embed(color=0xfffaa5)
                    embed.title = avatar_name + " (Token ID " + str(avatarnumber) + ")"
                    embed.set_thumbnail(url=avatarImageURL)
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    message = await tweetyMintChannel.send(embed = embed)
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update serverVariables set latest_tweety_mint = {0} where row = '1'".format(avatarnumber + 1)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    #Get Niftys owner
                    await asyncio.sleep(2)
                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+str(avatarnumber)+'&contractAddress=0x72d5d86e802129c2a01a875db74d37b1410f4d8d', headers=headers)
                    data = json.loads(response.text)
                    if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data['data'][0]['wallet']['account'] == None:
                        avatar_niftys_owner = "unknown"
                    else:
                        avatar_niftys_owner = data['data'][0]['wallet']['account']['handle']
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    await message.edit(embed = embed)
                    #Get discord owner
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_niftys_owner)
                    cur.execute(command)
                    avatar_discord_owner = cur.fetchall()
                    cur.close()
                    conn.close()
                    if avatar_discord_owner == []:
                        avatar_discord_owner = "unknown"
                    else:
                        avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    await message.edit(embed = embed)
                    avatarnumber += 1

async def sylvesterMints():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    tweetyMintChannel = discord.utils.get(guild.channels, id = 991063007377391776)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select latest_sylvester_mint from serverVariables where row = '1'"
    cur.execute(command)
    avatarnumber = cur.fetchall()
    cur.close()
    conn.close()
    avatarnumber = avatarnumber[0][0]
    newMints = True
    while newMints:
        await asyncio.sleep(2)
        try:
            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b/' + str(avatarnumber), headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
                    newMints = False
                elif data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Metadata not found.'}:
                    newMints = False
                elif data['attributes'] == []:
                    newMints = False
                else:
                    #Grab the avatar's image URL before we dive into the attribute data
                    avatarImageURL = data['image']
                    '''
                    dimAdjust = avatarImageURL.find("/v3-prod")
                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                    '''
                    avatarURL = "https://niftys.com/nft/0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b/"+str(avatarnumber)
                    avatar_name = data['name']
                    avatar_niftys_owner = "Retrieving..."
                    avatar_discord_owner = "Retrieving..."
                    avatar_eyes = ""
                    avatar_mouth = ""
                    avatar_facial_decoration = ""
                    avatar_shirt = ""
                    avatar_headband = ""
                    avatar_body = ""
                    avatar_neckwear = ""
                    avatar_environment = ""
                    avatar_handheld_prop = ""
                    avatar_looney_edition = ""
                    for attribute in data['attributes']:
                        if attribute['trait_type'] == 'Headwear':
                            avatar_headband = attribute['value']
                        if attribute['trait_type'] == 'Eyes':
                            avatar_eyes = attribute['value']
                        if attribute['trait_type'] == 'Mouth':
                            avatar_mouth = attribute['value']
                        if attribute['trait_type'] == 'Facial Decoration':
                            avatar_facial_decoration = attribute['value']
                        if attribute['trait_type'] == 'Body':
                            avatar_body = attribute['value']
                        if attribute['trait_type'] == 'Shirt':
                            avatar_shirt = attribute['value']
                        if attribute['trait_type'] == 'Neckwear':
                            avatar_neckwear = attribute['value']
                        if attribute['trait_type'] == 'Handheld Prop':
                            avatar_handheld_prop = attribute['value']
                        if attribute['trait_type'] == 'Environment':
                            avatar_environment = attribute['value']
                        if attribute['trait_type'] == 'Looney Edition':
                            avatar_looney_edition = attribute['value']
                    embed = discord.Embed(color=0xfffaa5)
                    embed.title = avatar_name
                    embed.set_thumbnail(url=avatarImageURL)
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update serverVariables set latest_sylvester_mint = {0} where row = '1'".format(avatarnumber + 1)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    message = await tweetyMintChannel.send(embed = embed)
                    
                    #Get Niftys owner
                    await asyncio.sleep(2)
                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+str(avatarnumber)+'&contractAddress=0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b', headers=headers)
                    data = json.loads(response.text)
                    if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data['data'][0]['wallet']['account'] == None:
                        avatar_niftys_owner = "unknown"
                    else:
                        avatar_niftys_owner = data['data'][0]['wallet']['account']['handle']
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    await message.edit(embed = embed)
                    #Get discord owner
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_niftys_owner)
                    cur.execute(command)
                    avatar_discord_owner = cur.fetchall()
                    cur.close()
                    conn.close()
                    if avatar_discord_owner == []:
                        avatar_discord_owner = "unknown"
                    else:
                        avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"
                    if avatar_looney_edition == "":
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
                    else:
                        embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
                    await message.edit(embed = embed)
                    avatarnumber += 1

async def bugsMints():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    tweetyMintChannel = discord.utils.get(guild.channels, id = 991063007377391776)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select latest_bugs_mint from serverVariables where row = '1'"
    cur.execute(command)
    avatarnumber = cur.fetchall()
    cur.close()
    conn.close()
    avatarnumber = avatarnumber[0][0]
    newMints = True
    while newMints:
        await asyncio.sleep(2)
        try:
            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903/' + str(avatarnumber), headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
                    newMints = False
                elif data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Metadata not found.'}:
                    newMints = False
                elif data['attributes'] == []:
                    newMints = False
                else:
                    #Grab the avatar's image URL before we dive into the attribute data
                    avatarImageURL = data['image']
                    '''
                    dimAdjust = avatarImageURL.find("/v3-prod")
                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                    '''
                    avatarURL = "https://niftys.com/nft/0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903/"+str(avatarnumber)
                    avatar_name = data['name']
                    avatar_niftys_owner = "Retrieving..."
                    avatar_discord_owner = "Retrieving..."
                    
                    embed = discord.Embed(color=0xfffaa5)
                    embed.title = avatar_name
                    embed.set_thumbnail(url=avatarImageURL)

                    embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n{2}".format(avatar_niftys_owner, avatar_discord_owner, avatarURL)
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update serverVariables set latest_bugs_mint = {0} where row = '1'".format(avatarnumber + 1)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    message = await tweetyMintChannel.send(embed = embed)
                    
                    #Get Niftys owner
                    await asyncio.sleep(2)
                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+str(avatarnumber)+'&contractAddress=0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903', headers=headers)
                    data = json.loads(response.text)
                    if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data == {'data': [], 'total': 0, 'paginationCursor': None}:
                        avatar_niftys_owner = "unknown"
                    elif data['data'][0]['wallet']['account'] == None:
                        avatar_niftys_owner = "unknown"
                    else:
                        avatar_niftys_owner = data['data'][0]['wallet']['account']['handle']

                    embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n{2}".format(avatar_niftys_owner, avatar_discord_owner, avatarURL)
                    await message.edit(embed = embed)
                    #Get discord owner
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_niftys_owner)
                    cur.execute(command)
                    avatar_discord_owner = cur.fetchall()
                    cur.close()
                    conn.close()
                    if avatar_discord_owner == []:
                        avatar_discord_owner = "unknown"
                    else:
                        avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"

                    embed.description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n{2}".format(avatar_niftys_owner, avatar_discord_owner, avatarURL)
                    await message.edit(embed = embed)
                    avatarnumber += 1

async def btMints():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    tweetyMintChannel = discord.utils.get(guild.channels, id = 1025133902404268132)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select latest_bt_mint from serverVariables where row = '1'"
    cur.execute(command)
    avatarnumber = cur.fetchall()
    cur.close()
    conn.close()
    avatarnumber = avatarnumber[0][0]
    newMints = True
    while newMints:
        await asyncio.sleep(2)
        try:
            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069/' + str(avatarnumber), headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
                    newMints = False
                elif data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Metadata not found.'}:
                    newMints = False
                elif data['attributes'] == []:
                    newMints = False
                else:
                    #Grab the avatar's image URL before we dive into the attribute data
                    avatarImageURL = data['image']
                    '''
                    dimAdjust = avatarImageURL.find("/v3-prod")
                    avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                    '''
                    avatarURL = "https://niftys.com/nft/0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069/"+str(avatarnumber)
                    avatar_name = data['name']
                    avatar_niftys_owner = "Retrieving..."
                    avatar_discord_owner = "Retrieving..."
                            
                    description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
                    for attribute in data['attributes']:
                        if attribute['value'] != 'None':
                            description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
                    description += "\n{0}".format(avatarURL)

                    embed = discord.Embed(color=0x000000)
                    embed.title = avatar_name
                    embed.set_thumbnail(url=avatarImageURL)
                    embed.description = description
                    
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update serverVariables set latest_bt_mint = {0} where row = '1'".format(avatarnumber + 1)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    
                    message = await tweetyMintChannel.send(embed = embed)
                    
                    #Get Niftys owner
                    await asyncio.sleep(2)
                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=' + str(avatarnumber) + '&contractAddress=0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069', headers=headers)
                    data2 = json.loads(response.text)
                    if data2 == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data2 == {'kind': 'INTERNAL_SERVER_ERR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data2 == {'data': [], 'total': 0, 'paginationCursor': None}:
                        avatar_niftys_owner = "unknown"
                    elif data2['data'][0]['wallet']['account'] == None:
                        avatar_niftys_owner = "unknown"
                    else:
                        avatar_niftys_owner = data2['data'][0]['wallet']['account']['handle']
                        
                    description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
                    for attribute in data['attributes']:
                        if attribute['value'] != 'None':
                            description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
                    description += "\n{0}".format(avatarURL)

                    embed.description = description
                    await message.edit(embed = embed)
                    
                    #Get discord owner
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_niftys_owner)
                    cur.execute(command)
                    avatar_discord_owner = cur.fetchall()
                    cur.close()
                    conn.close()
                    if avatar_discord_owner == []:
                        avatar_discord_owner = "unknown"
                    else:
                        avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"
                        
                    description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
                    for attribute in data['attributes']:
                        if attribute['value'] != 'None':
                            description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
                    description += "\n{0}".format(avatarURL)

                    embed.description = description
                    await message.edit(embed = embed)
                    avatarnumber += 1

async def gotMints():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    tweetyMintChannel = discord.utils.get(guild.channels, id = 1068281207625887744)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select latest_got_mint from serverVariables where row = '1'"
    cur.execute(command)
    avatarnumber = cur.fetchall()
    cur.close()
    conn.close()
    avatarnumber = avatarnumber[0][0]
    newMints = True
    while newMints:
        await asyncio.sleep(2)
        try:
            response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0x354d0bc7ad5914da9431124be01927c47e01ae2d/' + str(avatarnumber), headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
                    newMints = False
                elif data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    newMints = False
                elif data == {'code': 'NOT_FOUND', 'error': 'Metadata not found.'}:
                    newMints = False
                elif data['attributes'] == []:
                    newMints = False
                else:
                    #Grab the avatar's image URL before we dive into the attribute data
                    avatarImageURL = data['image']
                    avatarURL = "https://niftys.com/nft/0x354d0bc7ad5914da9431124be01927c47e01ae2d/"+str(avatarnumber)
                    avatar_name = data['name']
                    avatar_niftys_owner = "Retrieving..."
                    avatar_discord_owner = "Retrieving..."
                            
                    description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
                    for attribute in data['attributes']:
                        if attribute['value'] != 'None':
                            description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
                    description += "\n{0}".format(avatarURL)

                    embed = discord.Embed(color=0x000000)
                    embed.title = avatar_name
                    embed.set_thumbnail(url=avatarImageURL)
                    embed.description = description
                    
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "update serverVariables set latest_got_mint = {0} where row = '1'".format(avatarnumber + 1)
                    cur.execute(command)
                    cur.close()
                    conn.commit()
                    conn.close()
                    
                    message = await tweetyMintChannel.send(embed = embed)
                    
                    #Get Niftys owner
                    await asyncio.sleep(2)
                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=' + str(avatarnumber) + '&contractAddress=0x354d0bc7ad5914da9431124be01927c47e01ae2d', headers=headers)
                    data2 = json.loads(response.text)
                    if data2 == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data2 == {'kind': 'INTERNAL_SERVER_ERR', 'error': 'An unexpected error occurred'}:
                        avatar_niftys_owner = "unknown"
                    elif data2 == {'data': [], 'total': 0, 'paginationCursor': None}:
                        avatar_niftys_owner = "unknown"
                    elif data2['data'][0]['wallet']['account'] == None:
                        avatar_niftys_owner = "unknown"
                    else:
                        avatar_niftys_owner = data2['data'][0]['wallet']['account']['handle']
                        
                    description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
                    for attribute in data['attributes']:
                        if attribute['value'] != 'None':
                            description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
                    description += "\n{0}".format(avatarURL)

                    embed.description = description
                    await message.edit(embed = embed)
                    
                    #Get discord owner
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_niftys_owner)
                    cur.execute(command)
                    avatar_discord_owner = cur.fetchall()
                    cur.close()
                    conn.close()
                    if avatar_discord_owner == []:
                        avatar_discord_owner = "unknown"
                    else:
                        avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"
                        
                    description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
                    for attribute in data['attributes']:
                        if attribute['value'] != 'None':
                            description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
                    description += "\n{0}".format(avatarURL)

                    embed.description = description
                    await message.edit(embed = embed)
                    avatarnumber += 1
                    
async def updateOffers():
    #Creates a guild object (guild is Discord's official name for servers) based on the Nifty's server
    guild = bot.get_guild(869370430287384576)
    errors = discord.utils.get(guild.channels, name='bot-inits')
    ctx = discord.utils.get(guild.channels, id = 996063815798099998)

    #For each contract in the list of 721's
    for contract in contracts:
        #Pulls 20 open offers for that contract
        try:
            response = requests.get('https://api.niftys.com/v1/public/offers?contractAddress=' + contract + '&orderByDirection=desc&status=CREATED&party=buyer&take=20', headers=headers)
        except Exception as e:
            await errors.send(e)
        else:
            #Convert the JSON into a Python dictionary
            try:
                data = json.loads(response.text)
            except Exception as e:
                await errors.send(e)
            else:
                #Keeps looping through until the flag is set
                finished = False
                if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                    finished = True
                while finished == False:
                    #Grab the pagination cursor before we dive into the individual offers
                    if data != {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                        paginationCursor = data['paginationCursor']
                        #For each offer in the batch of 20 we just grabbed
                        for currentOffer in data['data']:
                            #Put the relevant JSON data into variables to make life easier and/or format correctly
                            offerPrice = currentOffer['price']
                            if contract in ['0x4a42fdf6f33226c03d68292de8113c96e78850ab', '0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b',
                                            '0x9a9ebf0bbf8bd027e0fba055a52d4ae7d1f52903', '0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069', '0x048035859089a9b13a3f1cc686a5f19f6375e073',
                                            '0x2bd016017e1f6a7d0948334017e9037028dede98', '0x354d0bc7ad5914da9431124be01927c47e01ae2d']:
                                offerPrice = round((float(offerPrice)/1000000),2)
                            else:
                                offerPrice = round((float(offerPrice)/1000000000000000000),2)
                            tokenId = currentOffer['tokenId']
                            contractAddress = currentOffer['contractAddress']
                            createdAt = currentOffer['createdAt']
                            date_str_no_z = createdAt[:-1]# remove last z
                            #This converts the timestamp string into a unix timestamp
                            dt_obj = datetime.datetime.strptime(date_str_no_z, "%Y-%m-%dT%H:%M:%S.%f")
                            unix_time = dt_obj.timestamp()
                            #If this offer is more than 31 days (2678400 seconds) old, we're gonna stop looking for offers
                            if int(unix_time) + 2678400 < int(time.time()):
                                finished = True
                            #Check to see if the current offer has already been found and communicated
                            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                            cur = conn.cursor()
                            command = "select * from offers where offer_id = '{0}'".format(currentOffer['id'])
                            cur.execute(command)
                            searchResult = cur.fetchall()
                            #If it hasn't already been posted:
                            if searchResult == []:
                                #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                await asyncio.sleep(2)
                                try:
                                    #Grab the pill info and current owner of this avatar
                                    response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+tokenId+'&contractAddress='+contractAddress, headers=headers)
                                except Exception as e:
                                    await errors.send(e)
                                    ownerId = "*(unable to load)*"
                                else:
                                    try:
                                        #Convert the JSON into a Python dictionary
                                        data = json.loads(response.text)
                                    except Exception as e:
                                        await errors.send(e)
                                        ownerId = "*(unable to load)*"
                                    else:
                                        if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                            ownerId = "*(unable to load)*"
                                        elif data['data'][0]['wallet']['account'] == None: 
                                            ownerId = "*(unable to load)*"
                                        else:
                                            ownerId = data['data'][0]['wallet']['account']['handle']
                                #First checks to see if this is a Palm Tweety
                                if contractAddress == contracts[3]:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/PALM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        tweetyNumber = ""
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            tweetyNumber = ""
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                tweetyNumber = ""
                                                avatarImageURL = ""
                                            else:
                                                tweetyNumber = data['name']
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                '''
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = tweetyNumber
                                    #Sets the message content
                                    description = tweetyNumber + " (Token ID " +tokenId + "), owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                                #Then checks to see if this is an Eth Tweety
                                elif contractAddress == contracts[4]:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        tweetyNumber = ""
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            tweetyNumber = ""
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                tweetyNumber = ""
                                                avatarImageURL = ""
                                            else:
                                                tweetyNumber = data['name']
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                '''
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = tweetyNumber
                                    #Sets the message content
                                    description = tweetyNumber + " (Token ID " +tokenId + "), owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                                #Then checks to see if this is a sylvester
                                elif contractAddress == contracts[5]:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        tweetyNumber = ""
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            tweetyNumber = ""
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                tweetyNumber = ""
                                                avatarImageURL = ""
                                            else:
                                                tweetyNumber = data['name']
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                '''
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = tweetyNumber
                                    #Sets the message content
                                    description = tweetyNumber + ", owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                                #Then checks to see if this is a bugs
                                elif contractAddress == contracts[6]:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        tweetyNumber = ""
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            tweetyNumber = ""
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                tweetyNumber = ""
                                                avatarImageURL = ""
                                            else:
                                                tweetyNumber = data['name']
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                '''
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = tweetyNumber
                                    #Sets the message content
                                    description = tweetyNumber + ", owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                                #Then checks to see if this is a bullet train or GoT
                                elif contractAddress == contracts[7] or contractAddress == contracts[9] or contractAddress == contracts[10]:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        tweetyNumber = ""
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            tweetyNumber = ""
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                tweetyNumber = ""
                                                avatarImageURL = ""
                                            else:
                                                tweetyNumber = data['name']
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                '''
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = tweetyNumber
                                    #Sets the message content
                                    description = tweetyNumber + ", owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                                #Then checks to see if this is a matrix reward
                                elif contractAddress == contracts[8]:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    if int(tokenId)<26:
                                        tweetyNumber = "The Nebuchadnezzar"
                                    else:
                                        tweetyNumber = "The Sentinel"
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                avatarImageURL = ""
                                            else:
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/400x400" + avatarImageURL[dimAdjust:]
                                                '''
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = tweetyNumber
                                    #Sets the message content
                                    description = tweetyNumber + ", owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                                #It must be a Matrix avatar
                                else:
                                    #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                                    await asyncio.sleep(2)
                                    try:
                                        #Grab the pill info and current owner of this avatar
                                        response = requests.get('https://api.niftys.com/v1/public/metadata/PALM/'+contractAddress+'/'+tokenId, headers=headers)
                                    except Exception as e:
                                        await errors.send(e)
                                        avatarImageURL = ""
                                    else:
                                        try:
                                            #Convert the JSON into a Python dictionary
                                            data = json.loads(response.text)
                                        except Exception as e:
                                            await errors.send(e)
                                            avatarImageURL = ""
                                        else:
                                            if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                                                avatarImageURL = ""
                                            else:
                                                avatarImageURL = data['image']
                                                '''
                                                dimAdjust = avatarImageURL.find("/v3-prod")
                                                avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/420x630" + avatarImageURL[dimAdjust:]
                                                '''
                                    #Sets a string variable with the pill status to be used later
                                    if contractAddress == contracts[0]:
                                        pilled = "Unpilled"
                                    elif contractAddress == contracts[1]:
                                        pilled = "Blue-pilled"
                                    elif contractAddress == contracts[2]:
                                        pilled = "Red-pilled"
                                    avatarURL = "https://niftys.com/nft/"+contractAddress+"/"+tokenId
                                    #Builds a Discord embed object for our message and sets the bar color
                                    embed = discord.Embed(color=0x000000)
                                    #Sets the thumbnail image
                                    embed.set_thumbnail(url=avatarImageURL)
                                    #Sets the title
                                    embed.title = "Matrix Avatar "+tokenId
                                    #Sets the message content
                                    description = pilled + " avatar " + tokenId + ", owned by " + ownerId + ", received a $" + str(offerPrice) + " offer on <t:"+str(int(unix_time))+":f>.\n\n"+avatarURL
                                    #See if the owner has linked their Discord account and wants to be pinged
                                    command = "select * from niftysAccounts where account_id = '{0}' and offer_updates = 1".format(ownerId)
                                    cur.execute(command)
                                    searchResult = cur.fetchall()
                                    if searchResult != []:
                                        description = description + "\n\nThis NFT belongs to you, <@" + str(searchResult[0][4]) + ">!"
                                    #Sets the message content
                                    embed.description = description
                                    #Sends the message
                                    await ctx.send(embed=embed)
                                    #add this sale into the database of sales we've already posted with a 1 day (86400) expiration date so I can keep the database clean
                                    command = "insert into offers (offer_id, expires) values ('{0}',{1})".format(currentOffer['id'], int(time.time())+86400)
                                    cur.execute(command)
                            #If it has already been posted, we're done going through this contract
                            else:
                                finished = True
                            cur.close()
                            conn.commit()
                            conn.close()
                        if paginationCursor == None:
                            finished = True
                        else:
                            #Pause for 2 seconds to adhere to the Nifty's API rate limit 
                            await asyncio.sleep(2)
                            #Pulls a new batch of 20 completed offers
                            try:
                                response = requests.get('https://api.niftys.com/v1/public/offers?contractAddress=' + contract + '&orderByDirection=desc&status=CREATED&party=buyer&take=20&paginationCursor='+paginationCursor, headers=headers)
                            except Exception as e:
                                await errors.send(e)
                            else:
                                #Convert the JSON into a Python dictionary
                                try:
                                    data = json.loads(response.text)
                                except Exception as e:
                                    await errors.send(e)
                                else:
                                    await asyncio.sleep(1)
                    else:
                        finished = True
    
    
#Runs the bot using the TOKEN defined in the environmental variables.         
bot.run(TOKEN)
