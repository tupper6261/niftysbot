#Nifty's Bot. Copyright Timothy Marshall Upper, 2022. All Rights Reserved.
#Version 1.0 - June 7, 2022

# bot.py
from __future__ import print_function
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

load_dotenv()

TOKEN = os.getenv('NIFTYS_BOT_TOKEN')
DATABASETOKEN = os.getenv('DATABASE_URL')
DISTRO_PRIVATE_KEY = os.getenv('DISTRO_PRIVATE_KEY')
niftysAuthorization = os.getenv('NIFTYS_BEARER_TOKEN')
niftysAuthKeyID = os.getenv('NIFTYS_AUTH_KEY')

niftysAPIHeaders = {
    'accept': 'application/json',
    'Authorization': niftysAuthorization,
    'auth-key-id': niftysAuthKeyID,
}


async def sendGITM(wallet, numPrizes):
    # enter your private key.  Be careful with your private key
    private_key = DISTRO_PRIVATE_KEY

    # add your blockchain connection information
    infura_url = 'https://mainnet.palm.niftys.com:8545/'
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # enter the account that the crypto is being sent from
    from_address = web3.toChecksumAddress("0xdcAe9202e61b4Db38a461836EE1311d923F7A617")

    true = True
    false = False
    glitchContract = web3.toChecksumAddress("0x797735ff36e3a602dbb54510263cfb42633f2486")
    glitchABI = ([{"type":"constructor","stateMutability":"nonpayable","inputs":[]},{"type":"event","name":"ApprovalForAll","inputs":[{"type":"address","name":"account","internalType":"address","indexed":true},{"type":"address","name":"operator","internalType":"address","indexed":true},{"type":"bool","name":"approved","internalType":"bool","indexed":false}],"anonymous":false},{"type":"event","name":"Paused","inputs":[{"type":"address","name":"account","internalType":"address","indexed":false}],"anonymous":false},{"type":"event","name":"RoleAdminChanged","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32","indexed":true},{"type":"bytes32","name":"previousAdminRole","internalType":"bytes32","indexed":true},{"type":"bytes32","name":"newAdminRole","internalType":"bytes32","indexed":true}],"anonymous":false},{"type":"event","name":"RoleGranted","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32","indexed":true},{"type":"address","name":"account","internalType":"address","indexed":true},{"type":"address","name":"sender","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"RoleRevoked","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32","indexed":true},{"type":"address","name":"account","internalType":"address","indexed":true},{"type":"address","name":"sender","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"RoyaltyFeeChanged","inputs":[{"type":"uint24","name":"previousFee","internalType":"uint24","indexed":false},{"type":"uint24","name":"newFee","internalType":"uint24","indexed":false}],"anonymous":false},{"type":"event","name":"RoyaltyWalletChanged","inputs":[{"type":"address","name":"previousWallet","internalType":"address","indexed":true},{"type":"address","name":"newWallet","internalType":"address","indexed":true}],"anonymous":false},{"type":"event","name":"TransferBatch","inputs":[{"type":"address","name":"operator","internalType":"address","indexed":true},{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256[]","name":"ids","internalType":"uint256[]","indexed":false},{"type":"uint256[]","name":"values","internalType":"uint256[]","indexed":false}],"anonymous":false},{"type":"event","name":"TransferSingle","inputs":[{"type":"address","name":"operator","internalType":"address","indexed":true},{"type":"address","name":"from","internalType":"address","indexed":true},{"type":"address","name":"to","internalType":"address","indexed":true},{"type":"uint256","name":"id","internalType":"uint256","indexed":false},{"type":"uint256","name":"value","internalType":"uint256","indexed":false}],"anonymous":false},{"type":"event","name":"URI","inputs":[{"type":"string","name":"value","internalType":"string","indexed":false},{"type":"uint256","name":"id","internalType":"uint256","indexed":true}],"anonymous":false},{"type":"event","name":"URIChanged","inputs":[{"type":"string","name":"newURI","internalType":"string","indexed":false}],"anonymous":false},{"type":"event","name":"Unpaused","inputs":[{"type":"address","name":"account","internalType":"address","indexed":false}],"anonymous":false},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"ADMIN","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"DEFAULT_ADMIN_ROLE","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"ROYALTY_FEE_DENOMINATOR","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"SIGNER","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"},{"type":"uint256","name":"id","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"","internalType":"uint256[]"}],"name":"balanceOfBatch","inputs":[{"type":"address[]","name":"accounts","internalType":"address[]"},{"type":"uint256[]","name":"ids","internalType":"uint256[]"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"burn","inputs":[{"type":"address","name":"account","internalType":"address"},{"type":"uint256","name":"id","internalType":"uint256"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"burnBatch","inputs":[{"type":"address","name":"account","internalType":"address"},{"type":"uint256[]","name":"ids","internalType":"uint256[]"},{"type":"uint256[]","name":"values","internalType":"uint256[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"contractURI","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"getRoleAdmin","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"grantRole","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32"},{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"hasRole","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32"},{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"isApprovedForAll","inputs":[{"type":"address","name":"account","internalType":"address"},{"type":"address","name":"operator","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mint","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"id","internalType":"uint256"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"mintBatch","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256[]","name":"ids","internalType":"uint256[]"},{"type":"uint256[]","name":"values","internalType":"uint256[]"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"minted","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"pause","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"paused","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"renounceRole","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32"},{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"revokeRole","inputs":[{"type":"bytes32","name":"role","internalType":"bytes32"},{"type":"address","name":"account","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint24","name":"","internalType":"uint24"}],"name":"royaltyFee","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"receiver","internalType":"address"},{"type":"uint256","name":"royaltyAmount","internalType":"uint256"}],"name":"royaltyInfo","inputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"value","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"royaltyWallet","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"safeBatchTransferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256[]","name":"ids","internalType":"uint256[]"},{"type":"uint256[]","name":"amounts","internalType":"uint256[]"},{"type":"bytes","name":"data","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"safeTransferFrom","inputs":[{"type":"address","name":"from","internalType":"address"},{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"id","internalType":"uint256"},{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"bytes","name":"data","internalType":"bytes"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setApprovalForAll","inputs":[{"type":"address","name":"operator","internalType":"address"},{"type":"bool","name":"approved","internalType":"bool"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setContractURI","inputs":[{"type":"string","name":"_contractURI","internalType":"string"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setRoyaltyFee","inputs":[{"type":"uint24","name":"_royaltyFee","internalType":"uint24"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setRoyaltyWallet","inputs":[{"type":"address","name":"_royaltyWallet","internalType":"address"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"setURI","inputs":[{"type":"string","name":"_uri","internalType":"string"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"supportsInterface","inputs":[{"type":"bytes4","name":"interfaceId","internalType":"bytes4"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"unpause","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"","internalType":"string"}],"name":"uri","inputs":[{"type":"uint256","name":"tokenid","internalType":"uint256"}]}])

    # enter a list of accounts that the crypto is being sent to
    to_address = web3.toChecksumAddress(wallet)

    i = 0
    while i < numPrizes:
        nonce = web3.eth.getTransactionCount(from_address)

        data = bytes(0)

        prizeContract = web3.eth.contract(address = glitchContract, abi = glitchABI)

        tx = prizeContract.functions.safeTransferFrom(from_address, to_address, 1, 1, data).buildTransaction(
            {
                    'from': from_address,
                    'nonce': nonce,
                    'gas': 300000,
                    'gasPrice': web3.toWei('.000021', 'gwei')
            }
        )

        # sign the transaction
        # wait 5 seconds before processing the next transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        try:
            tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        except Exception as e:
            time.sleep(5)
            sendGITM(wallet, 1)
            i += 1
        else:
            try:
                transaction = web3.toHex(tx_hash)
            except Exception as e:
                time.sleep(5)
                i+=1
            else:
                time.sleep(5)
                i+=1
               
async def mint721(contractAddress, network, toAddress, amount):
    headers = {
        'accept': 'application/json',
        'Authorization': niftysAuthorization,
        'auth-key-id': niftysAuthKeyID,
    }
    mintPayload = {
      "contractAddress": contractAddress,
      "network": network,
      "toAddress": toAddress,
      "amount": amount
    }
    response = requests.post('https://api.niftys.com/v1/public/mint-items', headers=headers, json = mintPayload)
    while str(response) != "<Response [200]>":
        response = requests.post('https://api.niftys.com/v1/public/mint-items', headers=headers, json = mintPayload)
        print (response)
        data = json.loads(response.text)
        print (data)
        
        
async def mint1155(contractAddress, tokenID, network, toAddress, amount):
    headers = {
        'accept': 'application/json',
        'Authorization': niftysAuthorization,
        'auth-key-id': niftysAuthKeyID,
    }
    mintPayload = {
      "tokenId": tokenID,
      "contractAddress": contractAddress,
      "network": network,
      "toAddress": toAddress,
      "amount": amount
    }
    response = requests.post('https://api.niftys.com/v1/public/mint-items', headers=headers, json = mintPayload)
    while str(response) != "<Response [200]>":
        response = requests.post('https://api.niftys.com/v1/public/mint-items', headers=headers, json = mintPayload)
        print (response)
        data = json.loads(response.text)
        print (data)

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="+", intents=intents)

#Defines a View class. Overrides the default View class primarily so I can override the timeout timer/reaction
class MyView(View):
    
    def __init__(self, ctx, timeout = 10):
        super().__init__(timeout = timeout)
        self.ctx = ctx

    async def on_timeout(self):
        for i in self.children:
            if isinstance(i, Button):
                i.disabled = True
        for i in self.children:
            if isinstance(i, Select):
                self.remove_item(i)
        await self.message.edit_original_message(view = self)

async def coingiveawaymessage(ctx, amount, timelimit):
    #setting this here so it's accessible throughout the function
    messageID = 0
    timeSeconds = timelimit * 60
    view = MyView(ctx, timeSeconds+10)
    claimed = []
    
    async def claimCoinsButton_callback(interaction):
        member = interaction.user
        nonlocal amount
        nonlocal claimed
        if member.id in claimed:
            await interaction.response.send_message("You've already claimed these Coins!", ephemeral = True)
        else:
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from vault where discord_user_id = {0}".format(member.id)
            cur.execute(command)
            account = cur.fetchall()
            if account == []:
                command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, {1}, {2})".format(member.id, amount + 10000, int(time.time()))
                cur.execute(command)
                await interaction.response.send_message("""Well, hello!\n\nIt's nice to meet you!
                                                        \n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.
                                                        \n\nYour first daily Coin claim is worth 10,000 Coins, and I have added {0} coins to that. That brings your current balance to {1} coins.
                                                        \n\nFeel free to check out <#984461108347797504> for more info!""".format(str(amount), str(amount+10000)), ephemeral = True)
            else:
                account = account[0]
                newBalance = account[1] + amount
                command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                cur.execute(command)
                await interaction.response.send_message("Success! I just sent you "+str(amount)+" Coins, which brings your Coin balance to " + str(newBalance) + ".", ephemeral = True)
            claimed.append(member.id)
                
            cur.close()
            conn.commit()
            conn.close()

    claimCoinsButton = Button(label="🪙 Claim Coins 🪙", style = discord.ButtonStyle.blurple)
    claimCoinsButton.callback = claimCoinsButton_callback

    expiryTime = int(time.time()) + timeSeconds

    embed = discord.Embed(description="Hey guys! Here's "+str(amount)+" coins!\n\nI'll delete this <t:" + str(expiryTime) + ":R>.", color=0x0da2ff)
    
    view.add_item(claimCoinsButton)
    view.message = await ctx.respond(embed = embed, view = view, delete_after=timeSeconds)
    await asyncio.sleep(timeSeconds)

#Defines the coingiveaway slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Start a coin giveaway")
async def coingiveawaycampaign(ctx, amount: Option(int, "How many coins do you want to give away per message?"), timelimit: Option(int, "How long do you want each message to stay up (in minutes)?"), timeinterval: Option(int, "How long between messages (in minutes)?"), messagenumber: Option(int, "How many messages should I send?")):
    guild = bot.get_guild(869370430287384576)
    #Make sure the command user has the authority to run the command
    staffRole = discord.utils.get(ctx.guild.roles, id = 911663990223024218)
    superModRole = discord.utils.get(ctx.guild.roles, id = 987041256096030790)
    #if the user isn't a supermod or a nifty's staff, don't let them start the giveaway
    if staffRole not in ctx.author.roles and superModRole not in ctx.author.roles:
        response = random.randint(1,5)
        if response == 1:
            await ctx.respond("https://tenor.com/view/nice-try-saturday-night-live-good-try-nice-attempt-nice-shot-gif-25237563")
        if response == 2:
            await ctx.respond("https://tenor.com/view/nice-try-kid-frank-gallagher-william-macy-shameless-nice-one-gif-16165992")
        if response == 3:
            await ctx.respond("https://tenor.com/view/parks-and-rec-bobby-newport-nice-try-laughs-laughing-gif-21862350")
        if response == 4:
            await ctx.respond("https://tenor.com/view/nice-try-jack-donaghy-30rock-good-try-try-again-gif-21903632")
        if response == 5:
            await ctx.respond("https://tenor.com/view/nicetry-lawyer-harveyspecter-gif-4755413")
        return

    while messagenumber > 0:
        await coingiveawaymessage(ctx, amount, timelimit)
        await asyncio.sleep(timeinterval*60)
        messagenumber -= 1

#Defines the coingiveaway slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Start a coin giveaway")
async def coingiveaway(ctx, amount: Option(int, "How many coins do you want to give away?"), timelimit: Option(int, "How long do you want the message to be up (in minutes)?")):
    guild = bot.get_guild(869370430287384576)
    #Make sure the command user has the authority to run the command
    staffRole = discord.utils.get(ctx.guild.roles, id = 911663990223024218)
    superModRole = discord.utils.get(ctx.guild.roles, id = 987041256096030790)
    #if the user isn't a supermod or a nifty's staff, don't let them start the giveaway
    if staffRole not in ctx.author.roles and superModRole not in ctx.author.roles:
        response = random.randint(1,5)
        if response == 1:
            await ctx.respond("https://tenor.com/view/nice-try-saturday-night-live-good-try-nice-attempt-nice-shot-gif-25237563")
        if response == 2:
            await ctx.respond("https://tenor.com/view/nice-try-kid-frank-gallagher-william-macy-shameless-nice-one-gif-16165992")
        if response == 3:
            await ctx.respond("https://tenor.com/view/parks-and-rec-bobby-newport-nice-try-laughs-laughing-gif-21862350")
        if response == 4:
            await ctx.respond("https://tenor.com/view/nice-try-jack-donaghy-30rock-good-try-try-again-gif-21903632")
        if response == 5:
            await ctx.respond("https://tenor.com/view/nicetry-lawyer-harveyspecter-gif-4755413")
        return

    await coingiveawaymessage(ctx, amount, timelimit)
        
    

#Defines the send coins slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Send coins to a user.")
async def phoebesendcoins(ctx, recipient: Option(discord.Member, "Who do you want to send coins to?"), coins: Option(int, "How many?")):
    guild = bot.get_guild(869370430287384576)
    #Make sure the command user has the authority to run the command
    staffRole = discord.utils.get(ctx.guild.roles, id = 911663990223024218)
    superModRole = discord.utils.get(ctx.guild.roles, id = 987041256096030790)
    #if the user isn't a supermod or a nifty's staff, don't let them start the giveaway
    if staffRole not in ctx.author.roles and superModRole not in ctx.author.roles:
        response = random.randint(1,5)
        if response == 1:
            await ctx.respond("https://tenor.com/view/nice-try-saturday-night-live-good-try-nice-attempt-nice-shot-gif-25237563")
        if response == 2:
            await ctx.respond("https://tenor.com/view/nice-try-kid-frank-gallagher-william-macy-shameless-nice-one-gif-16165992")
        if response == 3:
            await ctx.respond("https://tenor.com/view/parks-and-rec-bobby-newport-nice-try-laughs-laughing-gif-21862350")
        if response == 4:
            await ctx.respond("https://tenor.com/view/nice-try-jack-donaghy-30rock-good-try-try-again-gif-21903632")
        if response == 5:
            await ctx.respond("https://tenor.com/view/nicetry-lawyer-harveyspecter-gif-4755413")
        return
    
    guild = bot.get_guild(869370430287384576)
    channel = discord.utils.get(guild.channels, name='🪙│bank-general')
    uid = recipient.id
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select balance from vault where discord_user_id = {0}".format(uid)
    cur.execute(command)
    balance = cur.fetchall()
    if balance == []:
        command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, {1}, {2})".format(uid, coins+10000, int(time.time()))
        cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()
        await ctx.respond("<@"+str(uid)+">, you have been sent 🪙"+ str(coins) + "! I also went ahead and claimed your first daily for you, which is worth 🪙10,000. You now have a balance of 🪙" + str(coins+10000) + ".")
    else:
        balance = balance[0][0]
        balance = balance + coins
        command = "update vault set balance = {0} where discord_user_id = {1}".format(balance,uid)
        cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()
        await ctx.respond("<@"+str(uid)+">, you have been sent 🪙"+ str(coins) + "! Your balance is now 🪙"+str(balance)+".")
        
        
#Defines the gameofthrones slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Information about the Game of Thrones: Build Your Realm program.")
async def gameofthrones(ctx):
    embed = discord.Embed(color=0x000000)
    embed.title = "Build Your Realm"
    embed.description = """Some frequently asked questions about the Game of Thrones: Build Your Realm NFT Program:\n\n**1. When will the mint take place?**\nThe presale mint will be on <t:1673366400:f> and the public sale will begin at <t:1673380800:t>. Both of these times are displayed in your current time zone.\n\n**2. How much will the mint cost?**\nMint price will be $150 (or about .11 ETH).\n\n**3. Where will the mint take place?**\nThe mint will occur at https://niftys.com/c/gameofthrones/sale/the-north-series-1\n\n**4. Can I still get an allowlist spot?**\nUnfortunately, allowlist signups are currently closed.\n\n**5. What is the mint size?**\nThe mint will be made up of 5000 Hero Boxes. Each Hero Box will contain:\nOne Hero (or Legendary Hero) Avatar\nNine Resource Cards that you’ll need as you build your realm\nThree Story Cards, featuring iconic scenes, characters and locations from the show."""
    await ctx.respond(embed = embed)

'''
@bot.slash_command(guild_ids=[869370430287384576], description = "Tweety Sale Information")
async def tweetysale(ctx):
    embed = discord.Embed(color=FFEF00)
    embed.set_thumbnail(url="https://i.imgur.com/nXniSRl.png")
    embed.title = "Wondering if you're on the presale list?"
    embed.description = """Check out https://niftys.com/community/looney-tunes/sale/tweety-avatars and make sure you're logged in!"""
    await ctx.respond("https://i.imgur.com/GwdZB77.png")
    await ctx.send(embed = embed)
'''

#Defines the assassinavatars slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Look up info on an Assassin Avatar")
async def assassinavatar(ctx, avatarnumber: Option(int, "The mint number of the avatar you want to look up", required = True)):
    #Make sure the avatar is in the proper range
    if avatarnumber < 1 or avatarnumber > 10000:
        message = await ctx.respond("You must enter a number between 1 and 5000!", ephemeral= True)
    else:
        #Look up the avatar
        message = await ctx.respond("Loading Assassin Avatar " + str(avatarnumber) + ". This may take a few seconds...")
        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069/' + str(avatarnumber), headers=niftysAPIHeaders)
        data = json.loads(response.text)
        if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'} or data == {'code': 'NOT_FOUND', 'error': 'Not Found'} or data['attributes'] == []:
            await message.edit_original_message(content = "Avatar " + str(avatarnumber) + " has not been minted yet!")
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
                if attribute['value'] != "None":
                    description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
            description += "\n{0}".format(avatarURL)

            embed = discord.Embed(color=0xfffaa5)
            embed.title = avatar_name
            embed.set_thumbnail(url=avatarImageURL)
            embed.description = description
            await message.edit_original_message(content = "", embed = embed)
            
            #Get Niftys owner
            await asyncio.sleep(2)
            response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=' + str(avatarnumber) + '&contractAddress=0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069', headers=niftysAPIHeaders)
            data2 = json.loads(response.text)
            if data2 == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                avatar_niftys_owner = "unknown"
            elif data2 == {'data': [], 'total': 0, 'paginationCursor': None}:
                avatar_niftys_owner = "unknown"
            elif data2['data'][0]['wallet']['account'] == None:
                avatar_niftys_owner = "unknown"
            else:
                avatar_niftys_owner = data2['data'][0]['wallet']['account']['handle']
                
            description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
            for attribute in data['attributes']:
                if attribute['value'] != "None":
                    description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
            description += "\n{0}".format(avatarURL)

            embed.description = description
            await message.edit_original_message(embed = embed)
            
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
                
            description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
            for attribute in data['attributes']:
                if attribute['value'] != "None":
                    description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
            description += "\n{0}".format(avatarURL)

            embed.description = description
            await message.edit_original_message(embed = embed)

#Defines the sylvesteravatars slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Look up info on a Sylvester Avatar")
async def sylvesteravatar(ctx, avatarnumber: Option(int, "The mint number of the avatar you want to look up", required = True)):
    #Make sure the avatar is in the proper range
    if avatarnumber < 1 or avatarnumber > 5000:
        message = await ctx.respond("You must enter a number between 1 and 5000!", ephemeral= True)
    else:
        #Look up the avatar
        message = await ctx.respond("Loading Sylvester Avatar " + str(avatarnumber) + ". This may take a few seconds...")
        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b/' + str(avatarnumber), headers=niftysAPIHeaders)
        data = json.loads(response.text)
        if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'} or data == {'code': 'NOT_FOUND', 'error': 'Not Found'}:
            await message.edit_original_message(content = "Avatar " + str(avatarnumber) + " has not been minted yet!")
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
                    
            description = "**Owner's Nifty's Handle:** *{0}*\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
            for attribute in data['attributes']:
                description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
            description += "\n{0}".format(avatarURL)

            embed = discord.Embed(color=0xfffaa5)
            embed.title = avatar_name
            embed.set_thumbnail(url=avatarImageURL)
            embed.description = description
            await message.edit_original_message(content = "", embed = embed)
            
            #Get Niftys owner
            await asyncio.sleep(2)
            response = requests.get('https://api.niftys.com/v1/public/owners?tokenId=' + str(avatarnumber) + '&contractAddress=0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b', headers=niftysAPIHeaders)
            data2 = json.loads(response.text)
            if data2 == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
                avatar_niftys_owner = "unknown"
            elif data2 == {'data': [], 'total': 0, 'paginationCursor': None}:
                avatar_niftys_owner = "unknown"
            elif data2['data'][0]['wallet']['account'] == None:
                avatar_niftys_owner = "unknown"
            else:
                avatar_niftys_owner = data2['data'][0]['wallet']['account']['handle']
                
            description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
            for attribute in data['attributes']:
                description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
            description += "\n{0}".format(avatarURL)

            embed.description = description
            await message.edit_original_message(embed = embed)
            
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
                
            description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** {1}\n\n**Attributes:**\n".format(avatar_niftys_owner, avatar_discord_owner)
            for attribute in data['attributes']:
                description += "**{0}:** {1}\n".format(attribute['trait_type'], attribute['value'])
            description += "\n{0}".format(avatarURL)

            embed.description = description
            await message.edit_original_message(embed = embed)

#Defines the tweetyavatars slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Look up info on a Tweety Avatar")
async def tweetyavatar(ctx, avatarnumber: Option(int, "The mint number of the avatar you want to look up", required = True)):
    #Make sure the avatar is in the proper range
    if avatarnumber < 1 or avatarnumber > 5000:
        message = await ctx.respond("You must enter a number between 1 and 5000!", ephemeral= True)
    else:
        #Look up the avatar
        message = await ctx.respond("Loading Tweety Avatar " + str(avatarnumber) + ". This may take a few seconds...")
        response = requests.get('https://api.niftys.com/v1/public/metadata/ETHEREUM/0x4a42fdf6f33226c03d68292de8113c96e78850ab/' + str(avatarnumber), headers=niftysAPIHeaders)
        data = json.loads(response.text)
        if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'} or data == {'code': 'NOT_FOUND', 'error': 'Not Found'} or data['attributes']==[]:
            response = requests.get('https://api.niftys.com/v1/public/metadata/PALM/0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e/' + str(avatarnumber), headers=niftysAPIHeaders)
            data = json.loads(response.text)
        if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'} or data == {'code': 'NOT_FOUND', 'error': 'Not Found'} or data['attributes']==[]:
            await message.edit_original_message(content = "Avatar " + str(avatarnumber) + " has not been minted yet!")
            return
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
            await message.edit_original_message(content = "", embed = embed)
            #Get Niftys owner
            response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+str(avatarnumber)+'&contractAddress=0x8b0ee617084fa3cdd4fa29130bef7a5ca64c650e', headers=niftysAPIHeaders)
            data = json.loads(response.text)
            avatar_niftys_owner = data['data'][0]['wallet']['account']['handle']
            if avatar_looney_edition == "":
                embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Headwear:** {2}\n**Eyes:** {3}\n**Mouth:** {4}\n**Facial Decoration:** {5}\n**Body:** {6}\n**Shirt:** {7}\n**Neckwear:** {8}\n**Handhed Prop:** {9}\n**Environment:** {10}\n\n{11}".format(avatar_niftys_owner, avatar_discord_owner, avatar_headband, avatar_eyes, avatar_mouth, avatar_facial_decoration, avatar_body, avatar_shirt, avatar_neckwear, avatar_handheld_prop, avatar_environment, avatarURL)
            else:
                embed.description = "**Owner's Nifty's Handle:** {0}\n**Owner's Discord Username:** *{1}*\n\n**Attributes:**\n**Looney Edition:** {2}\n\n{3}".format(avatar_niftys_owner, avatar_discord_owner, avatar_looney_edition, avatarURL)
            await message.edit_original_message(content = "", embed = embed)
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
            await message.edit_original_message(content = "", embed = embed)


#Defines the matrixavatars slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Look up info on a Matrix Avatar")
async def matrixavatar(ctx, avatarnumber: Option(int, "The avatar number you want to look up", required = True)):
    #Make sure the avatar is in the proper range
    if avatarnumber < 1 or avatarnumber > 100000:
        message = await ctx.respond("You must enter a number between 1 and 100000!", ephemeral= True)
    else:
        #Because of Nifty's rate limiting, it could take a bit to respond...
        message = await ctx.respond("Looking up Matrix Avatar " + str(avatarnumber) + ". This may take a few seconds...")
        #Sets up all the avatar variables to be filled in later:
        avatar_owner = "loading..."
        avatar_discord_owner = "loading..."
        avatar_pill = ""
        avatar_awareness = ""
        avatar_perception = ""
        avatar_movement = ""
        avatar_power = ""
        avatar_footwear = ""
        avatar_piercings = ""
        avatar_left_hand_accessory = ""
        avatar_name = ""
        avatar_top = ""
        avatar_persuasion = ""
        avatar_bottom = ""
        avatar_will = ""
        avatar_headjack = ""
        avatar_background = ""
        avatar_hair_style = ""
        avatar_hair_color = ""
        avatar_hair_dye = ""
        avatar_facial_hair = ""
        avatar_facial_expression = ""
        avatar_wristwear = ""
        avatar_neckwear = ""
        avatar_glasses = ""
        avatar_bicep_tattoo = ""
        avatar_forearm_tattoo = ""
        avatar_side_neck_tattoo = ""
        avatar_front_neck_tattoo = ""
        avatar_right_hand_accessory = ""
        avatar_generation = ""
        avatar_votes = ""
        avatar_strength = ""
        avatar_constitution = ""
        avatar_dexterity = ""
        avatar_intelligence = ""
        avatar_wisdom = ""
        avatar_charisma = ""
        avatar_zen = ""
        avatar_occupation = ""
        avatar_hacking = ""
        avatar_ring = ""
        avatar_headwear = ""
        avatar_accessories = ""
        avatar_credit_score = ""
        avatar_salary = ""
        avatar_social_media_followers = ""
        avatar_transportation = ""
        '''
        #First check my SQL database to see if the avatar can be grabbed from the cache
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "select * from avatars where token_id = {0}".format(avatarnumber)
        cur.execute(command)
        avatar = cur.fetchall()
        cur.close()
        conn.close()
        #If it isn't:
        if avatar[0][2] == 'None' or avatar == []:
        '''
        #Check to see if the avatar is a red-pilled one
        response = requests.get('https://api.niftys.com/v1/public/contracts/0x28e4b03bc88b59d25f3467b2252b66d4b2c43286/' + str(avatarnumber), headers=niftysAPIHeaders)
        data = json.loads(response.text)
        avatar_pill = "Red"
        avatar_contract = "0x28e4b03bc88b59d25f3467b2252b66d4b2c43286"
        #If we can't find a red-pilled avatar by that number
        if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
            #Check to see if the avatar is a blue-pilled one
            response = requests.get('https://api.niftys.com/v1/public/contracts/0x423e540cb46db0e4df1ac96bcbddf78a804647d8/' + str(avatarnumber), headers=niftysAPIHeaders)
            data = json.loads(response.text)
            avatar_pill = "Blue"
            avatar_contract = "0x423e540cb46db0e4df1ac96bcbddf78a804647d8"
            #If we can't find a blue-pilled avatar by that number
            if data == {'code': 'NOT_FOUND', 'error': 'Unable to locate resource.'}:
                #It must still be unpilled
                response = requests.get('https://api.niftys.com/v1/public/contracts/0x39ceaa47306381b6d79ad46af0f36bc5332386f2/' + str(avatarnumber), headers=niftysAPIHeaders)
                data = json.loads(response.text)
                avatar_pill = "None"
                avatar_contract = "0x39ceaa47306381b6d79ad46af0f36bc5332386f2"
        #Grab the avatar's image URL before we dive into the attribute data
        avatarImageURL = data['data']['media']['url']
        dimAdjust = avatarImageURL.find("/v3-prod")
        avatarImageURL = avatarImageURL[:dimAdjust] + "/fit-in/420x630" + avatarImageURL[dimAdjust:]
        #Iterate through all the attributes
        for attribute in data['data']['attributes']:
            if attribute['trait_type'] == 'Hair Dye':
                avatar_hair_dye = attribute['value']
            if attribute['trait_type'] == 'Awareness':
                avatar_awareness = attribute['value']
            if attribute['trait_type'] == 'Perception':
                avatar_perception = attribute['value']
            if attribute['trait_type'] == 'Movement':
                avatar_movement = attribute['value']
            if attribute['trait_type'] == 'Power':
                avatar_power = attribute['value']
            if attribute['trait_type'] == 'Footwear':
                avatar_footwear = attribute['value']
            if attribute['trait_type'] == 'Piercings':
                avatar_piercings = attribute['value']
            if attribute['trait_type'] == 'Left Hand Accessory':
                avatar_left_hand_accessory = attribute['value']
            if attribute['trait_type'] == 'Name':
                avatar_name = attribute['value']
            if attribute['trait_type'] == 'Top':
                avatar_top = attribute['value']
            if attribute['trait_type'] == 'Persuasion':
                avatar_persuasion = attribute['value']
            if attribute['trait_type'] == 'Bottom':
                avatar_bottom = attribute['value']
            if attribute['trait_type'] == 'Will':
                avatar_will = attribute['value']
            if attribute['trait_type'] == 'Headjack':
                avatar_headjack = attribute['value']
            if attribute['trait_type'] == 'Background':
                avatar_background = attribute['value']
            if attribute['trait_type'] == 'Hair Style':
                avatar_hair_style = attribute['value']
            if attribute['trait_type'] == 'Hair Color':
                avatar_hair_color = attribute['value']
            if attribute['trait_type'] == 'Facial Hair':
                avatar_facial_hair = attribute['value']
            if attribute['trait_type'] == 'Facial Expression':
                avatar_facial_expression = attribute['value']
            if attribute['trait_type'] == 'Wristwear':
                avatar_wristwear = attribute['value']
            if attribute['trait_type'] == 'Neckwear':
                avatar_neckwear = attribute['value']
            if attribute['trait_type'] == 'Glasses':
                avatar_glasses = attribute['value']
            if attribute['trait_type'] == 'Bicep Tattoo':
                avatar_bicep_tattoo = attribute['value']
            if attribute['trait_type'] == 'Forearm Tattoo':
                avatar_forearm_tattoo = attribute['value']
            if attribute['trait_type'] == 'Side Neck Tattoo':
                avatar_side_neck_tattoo = attribute['value']
            if attribute['trait_type'] == 'Front Neck Tattoo':
                avatar_front_neck_tattoo = attribute['value']
            if attribute['trait_type'] == 'Right Hand Accessory':
                avatar_right_hand_accessory = attribute['value']
            if attribute['trait_type'] == 'Generation':
                avatar_generation = attribute['value']
            if attribute['trait_type'] == 'Votes':
                avatar_votes = attribute['value']
            if attribute['trait_type'] == 'Strength':
                avatar_strength = attribute['value']
            if attribute['trait_type'] == 'Constitution':
                avatar_constitution = attribute['value']
            if attribute['trait_type'] == 'Dexterity':
                avatar_dexterity = attribute['value']
            if attribute['trait_type'] == 'Intelligence':
                avatar_intelligence = attribute['value']
            if attribute['trait_type'] == 'Wisdom':
                avatar_wisdom = attribute['value']
            if attribute['trait_type'] == 'Charisma':
                avatar_charisma = attribute['value']
            if attribute['trait_type'] == 'Zen':
                avatar_zen = attribute['value']
            if attribute['trait_type'] == 'Occupation':
                avatar_occupation = attribute['value']
            if attribute['trait_type'] == 'Hacking':
                avatar_hacking = attribute['value']
            if attribute['trait_type'] == 'Ring':
                avatar_ring = attribute['value']
            if attribute['trait_type'] == 'Headwear':
                avatar_headwear = attribute['value']
            if attribute['trait_type'] == 'Accessories':
                avatar_accessories = attribute['value']
            if attribute['trait_type'] == 'Credit Score':
                avatar_credit_score = attribute['value']
            if attribute['trait_type'] == 'Salary':
                avatar_salary = attribute['value']
            if attribute['trait_type'] == 'Social Media Followers':
                avatar_social_media_followers = attribute['value']
            if attribute['trait_type'] == 'Transportation':
                avatar_transportation = attribute['value']
        '''
        #If the avatar is in the database:
        else:
            #Technically, SQL will have returned a one-item list and that one item is the list of attributes, so we're gonna just grab that one item
            avatar = avatar[0]
            #Then set the variables appropriately
            avatar_owner = avatar[1]
            avatar_pill = avatar[2]
            avatar_awareness = avatar[4]
            avatar_perception = avatar[5]
            avatar_movement = avatar[6]
            avatar_power = avatar[7]
            avatar_footwear = avatar[8]
            avatar_piercings = avatar[9]
            avatar_left_hand_accessory = avatar[10]
            avatar_name = avatar[11]
            avatar_top = avatar[12]
            avatar_persuasion = avatar[13]
            avatar_bottom = avatar[14]
            avatar_will = avatar[15]
            avatar_headjack = avatar[16]
            avatar_background = avatar[17]
            avatar_hair_style = avatar[18]
            avatar_hair_color = avatar[19]
            avatar_hair_dye = avatar[20]
            avatar_facial_hair = avatar[21]
            avatar_facial_expression = avatar[22]
            avatar_wristwear = avatar[23]
            avatar_neckwear = avatar[24]
            avatar_glasses = avatar[25]
            avatar_bicep_tattoo = avatar[26]
            avatar_forearm_tattoo = avatar[27]
            avatar_side_neck_tattoo = avatar[28]
            avatar_front_neck_tattoo = avatar[29]
            avatar_right_hand_accessory = avatar[30]
            avatar_generation = avatar[31]
            avatar_votes = avatar[32]
            avatar_strength = avatar[33]
            avatar_constitution = avatar[34]
            avatar_dexterity = avatar[35]
            avatar_intelligence = avatar[36]
            avatar_wisdom = avatar[37]
            avatar_charisma = avatar[38]
            avatar_zen = avatar[39]
            avatar_occupation = avatar[40]
            avatar_hacking = avatar[41]
            avatar_ring = avatar[42]
            avatar_headwear = avatar[43]
            avatar_accessories = avatar[44]
            avatar_credit_score = avatar[45]
            avatar_salary = avatar[46]
            avatar_social_media_followers = avatar[47]
            avatar_transportation = avatar[48]
        '''

        embed = discord.Embed(color=0xfffaa5)
        embed.title = "Matrix Avatar " + str(avatarnumber)
        embed.description = "Looking up Matrix Avatar " + str(avatarnumber) + ". This may take a few seconds..."

        if avatar_pill == "None":
            embed.set_thumbnail(url=avatarImageURL)
            description = "*Note: if this avatar has been recently pilled, it may take up to 6 hours to reflect here*\n\n**Unpilled Matrix Avatar {0}**\n\n**Owner's Nifty's Handle:** {1}\n**Owner's Discord Username:** {2}\n\n".format(avatarnumber, avatar_owner, avatar_discord_owner)
            embed.description = """*Note: if this avatar has been recently pilled, it may take up to 6 hours to reflect here*\n
                                **Unpilled Matrix Avatar {0}**\n
                                **Owner's Nifty's Handle:** {1}
                                **Owner's Discord Username:** {2}\n
                                **Headwear:** {3}
                                **Hair Style:** {4}
                                **Hair Color:** {5}
                                **Facial Hair:** {6}
                                **Glasses:** {7}
                                **Piercings:** {8}
                                **Top:** {9}
                                **Bottom:** {10}
                                **Footwear:** {11}
                                **Ring:** {12}
                                **Accessories:** {13}
                                **Background:** {14}\n
                                https://niftys.com/nft/0x39ceaa47306381b6d79ad46af0f36bc5332386f2/{15}""".format(avatarnumber, avatar_owner, avatar_discord_owner, avatar_headwear, avatar_hair_style, avatar_hair_color, avatar_facial_hair, avatar_glasses, avatar_piercings, avatar_top, avatar_bottom, avatar_footwear, avatar_ring, avatar_accessories, avatar_background, avatarnumber)
            #embed.description = description
        elif avatar_pill == "Blue":
            embed.set_thumbnail(url=avatarImageURL)
            embed.description = """**Blue-Pilled Matrix Avatar {0}**\n
                                **Owner's Nifty's Handle:** {1}
                                **Owner's Discord Username:** {2}
                                **Avatar Name:** {3}\n
                                **Visual Attributes:**
                                **Headwear:** {4}
                                **Hair Style:** {5}
                                **Hair Color:** {6}
                                **Facial Hair:** {7}
                                **Glasses:** {8}
                                **Piercings:** {9}
                                **Top:** {10}
                                **Bottom:** {11}
                                **Footwear:** {12}
                                **Ring:** {13}
                                **Accessories:** {14}
                                **Background:** {15}\n
                                **Non-Visual Attributes:**
                                **Total Stats:** {16}
                                **Zen:** {17}
                                **Wisdom:** {18}
                                **Hacking:** {19}
                                **Intelligence:** {20}
                                **Social Media Followers:** {21}
                                **Charisma:** {22}
                                **Transportation:** {23}
                                **Dexterity:** {24}
                                **Credit Score:** {25}
                                **Constitution:** {26}
                                **Salary:** {27}
                                **Strength:** {28}
                                **Occupation:** {29}
                                **Generation:** {30}
                                **Votes:** {31}\n
                                https://niftys.com/nft/0x423e540cb46db0e4df1ac96bcbddf78a804647d8/{32}""".format(avatarnumber, avatar_owner, avatar_discord_owner, avatar_name, avatar_headwear, avatar_hair_style, avatar_hair_color, avatar_facial_hair, avatar_glasses, avatar_piercings, avatar_top, avatar_bottom, avatar_footwear, avatar_ring, avatar_accessories, avatar_background, int(avatar_wisdom)+int(avatar_intelligence)+int(avatar_charisma)+int(avatar_dexterity)+int(avatar_constitution)+int(avatar_strength), avatar_zen, avatar_wisdom, avatar_hacking, avatar_intelligence, avatar_social_media_followers, avatar_charisma, avatar_transportation, avatar_dexterity, avatar_credit_score, avatar_constitution, avatar_salary, avatar_strength, avatar_occupation, avatar_generation, avatar_votes, avatarnumber)
        elif avatar_pill == "Red":
            embed.set_thumbnail(url=avatarImageURL)
            embed.description = """**Red-Pilled Matrix Avatar {0}**\n\n**Owner's Nifty's Handle:** {1}
                                **Owner's Discord Username:** {2}
                                **Avatar Name:** {3}\n
                                **Visual Attributes:**
                                **Headwear:** {4}
                                **Hair Style:** {5}
                                **Hair Color:** {6}
                                **Hair Dye:** {7}
                                **Facial Hair:** {8}
                                **Facial Expression:** {9}
                                **Glasses:** {10}
                                **Piercings:** {11}
                                **Neckwear:** {12}
                                **Front Neck Tattoo:** {13}
                                **Side Neck Tattoo:** {14}
                                **Bicep Tattoo:** {15}
                                **Forearm Tattoo:** {16}
                                **Top:** {17}
                                **Bottom:** {18}
                                **Footwear:** {19}
                                **Ring:** {20}
                                **Wristwear:** {21} 
                                **Right Hand Accessory:** {22}
                                **Left Hand Accessory:** {23}
                                **Background:** {24}\n
                                **Non-Visual Attributes:**
                                **Total Stats:** {25}
                                **Awareness:** {26}
                                **Wisdom:** {27}
                                **Perception:** {28}
                                **Intelligence:** {29}
                                **Persuasion:** {30}
                                **Charisma:** {31}
                                **Movement:** {32}
                                **Dexterity:** {33}
                                **Will:** {34}
                                **Constitution:** {35}
                                **Power:** {36}
                                **Strength:** {37}
                                **Occupation:** {38}
                                **Headjack:** {39}
                                **Generation:** {40}
                                **Votes:** {41}\n
                                https://niftys.com/nft/0x28e4b03bc88b59d25f3467b2252b66d4b2c43286/{42}""".format(avatarnumber, avatar_owner, avatar_discord_owner, avatar_name, avatar_headwear, avatar_hair_style, avatar_hair_color, avatar_hair_dye, avatar_facial_hair, avatar_facial_expression, avatar_glasses, avatar_piercings, avatar_neckwear, avatar_front_neck_tattoo, avatar_side_neck_tattoo, avatar_bicep_tattoo, avatar_forearm_tattoo, avatar_top, avatar_bottom, avatar_footwear, avatar_ring, avatar_wristwear, avatar_right_hand_accessory, avatar_left_hand_accessory, avatar_background, int(avatar_wisdom)+int(avatar_intelligence)+int(avatar_charisma)+int(avatar_dexterity)+int(avatar_constitution)+int(avatar_strength), avatar_awareness, avatar_wisdom, avatar_perception, avatar_intelligence, avatar_persuasion, avatar_charisma, avatar_movement, avatar_dexterity, avatar_will, avatar_constitution, avatar_power, avatar_strength, avatar_occupation, avatar_headjack, avatar_generation, avatar_votes, avatarnumber)
        #await ctx.send(embed = embed)
        await message.edit_original_message(content = "", embed = embed)

        
        #Grab the owner's Discord username
        response = requests.get('https://api.niftys.com/v1/public/owners?tokenId='+str(avatarnumber)+'&contractAddress='+avatar_contract, headers=niftysAPIHeaders)
        data = json.loads(response.text)

        if data == {'kind': 'INTERNAL_SERVER_ERROR', 'error': 'An unexpected error occurred'}:
            avatar_owner = "unknown"
        elif data == {'data': [], 'total': 0, 'paginationCursor': None}:
            avatar_owner = "unknown"
        elif data['data'][0]['wallet']['account'] == None:
            avatar_owner = "unknown"
        else:
            avatar_owner = data['data'][0]['wallet']['account']['handle']

        if avatar_owner != "loading..." and avatar_owner != "unknown":
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select discord_user_id from niftysAccounts where account_id = '{0}'".format(avatar_owner)
            cur.execute(command)
            avatar_discord_owner = cur.fetchall()
            cur.close()
            conn.close()
            avatar_owner = "@" + avatar_owner
            
            if avatar_discord_owner == []:
                avatar_discord_owner = "Unknown"
            else:
                avatar_discord_owner = "<@" + str(avatar_discord_owner[0][0]) + ">"
        else:
            avatar_discord_owner = "Unknown"
            
        if avatar_pill == "None":
            embed.set_thumbnail(url=avatarImageURL)
            description = "*Note: if this avatar has been recently pilled, it may take up to 6 hours to reflect here*\n\n**Unpilled Matrix Avatar {0}**\n\n**Owner's Nifty's Handle:** {1}\n**Owner's Discord Username:** {2}\n\n".format(avatarnumber, avatar_owner, avatar_discord_owner)
            embed.description = """*Note: if this avatar has been recently pilled, it may take up to 6 hours to reflect here*\n
                                **Unpilled Matrix Avatar {0}**\n
                                **Owner's Nifty's Handle:** {1}
                                **Owner's Discord Username:** {2}\n
                                **Headwear:** {3}
                                **Hair Style:** {4}
                                **Hair Color:** {5}
                                **Facial Hair:** {6}
                                **Glasses:** {7}
                                **Piercings:** {8}
                                **Top:** {9}
                                **Bottom:** {10}
                                **Footwear:** {11}
                                **Ring:** {12}
                                **Accessories:** {13}
                                **Background:** {14}\n
                                https://niftys.com/nft/0x39ceaa47306381b6d79ad46af0f36bc5332386f2/{15}""".format(avatarnumber, avatar_owner, avatar_discord_owner, avatar_headwear, avatar_hair_style, avatar_hair_color, avatar_facial_hair, avatar_glasses, avatar_piercings, avatar_top, avatar_bottom, avatar_footwear, avatar_ring, avatar_accessories, avatar_background, avatarnumber)
            #embed.description = description
        elif avatar_pill == "Blue":
            embed.set_thumbnail(url=avatarImageURL)
            embed.description = """**Blue-Pilled Matrix Avatar {0}**\n
                                **Owner's Nifty's Handle:** {1}
                                **Owner's Discord Username:** {2}
                                **Avatar Name:** {3}\n
                                **Visual Attributes:**
                                **Headwear:** {4}
                                **Hair Style:** {5}
                                **Hair Color:** {6}
                                **Facial Hair:** {7}
                                **Glasses:** {8}
                                **Piercings:** {9}
                                **Top:** {10}
                                **Bottom:** {11}
                                **Footwear:** {12}
                                **Ring:** {13}
                                **Accessories:** {14}
                                **Background:** {15}\n
                                **Non-Visual Attributes:**
                                **Total Stats:** {16}
                                **Zen:** {17}
                                **Wisdom:** {18}
                                **Hacking:** {19}
                                **Intelligence:** {20}
                                **Social Media Followers:** {21}
                                **Charisma:** {22}
                                **Transportation:** {23}
                                **Dexterity:** {24}
                                **Credit Score:** {25}
                                **Constitution:** {26}
                                **Salary:** {27}
                                **Strength:** {28}
                                **Occupation:** {29}
                                **Generation:** {30}
                                **Votes:** {31}\n
                                https://niftys.com/nft/0x423e540cb46db0e4df1ac96bcbddf78a804647d8/{32}""".format(avatarnumber, avatar_owner, avatar_discord_owner, avatar_name, avatar_headwear, avatar_hair_style, avatar_hair_color, avatar_facial_hair, avatar_glasses, avatar_piercings, avatar_top, avatar_bottom, avatar_footwear, avatar_ring, avatar_accessories, avatar_background, int(avatar_wisdom)+int(avatar_intelligence)+int(avatar_charisma)+int(avatar_dexterity)+int(avatar_constitution)+int(avatar_strength), avatar_zen, avatar_wisdom, avatar_hacking, avatar_intelligence, avatar_social_media_followers, avatar_charisma, avatar_transportation, avatar_dexterity, avatar_credit_score, avatar_constitution, avatar_salary, avatar_strength, avatar_occupation, avatar_generation, avatar_votes, avatarnumber)
        elif avatar_pill == "Red":
            embed.set_thumbnail(url=avatarImageURL)
            embed.description = """**Red-Pilled Matrix Avatar {0}**\n\n**Owner's Nifty's Handle:** {1}
                                **Owner's Discord Username:** {2}
                                **Avatar Name:** {3}\n
                                **Visual Attributes:**
                                **Headwear:** {4}
                                **Hair Style:** {5}
                                **Hair Color:** {6}
                                **Hair Dye:** {7}
                                **Facial Hair:** {8}
                                **Facial Expression:** {9}
                                **Glasses:** {10}
                                **Piercings:** {11}
                                **Neckwear:** {12}
                                **Front Neck Tattoo:** {13}
                                **Side Neck Tattoo:** {14}
                                **Bicep Tattoo:** {15}
                                **Forearm Tattoo:** {16}
                                **Top:** {17}
                                **Bottom:** {18}
                                **Footwear:** {19}
                                **Ring:** {20}
                                **Wristwear:** {21} 
                                **Right Hand Accessory:** {22}
                                **Left Hand Accessory:** {23}
                                **Background:** {24}\n
                                **Non-Visual Attributes:**
                                **Total Stats:** {25}
                                **Awareness:** {26}
                                **Wisdom:** {27}
                                **Perception:** {28}
                                **Intelligence:** {29}
                                **Persuasion:** {30}
                                **Charisma:** {31}
                                **Movement:** {32}
                                **Dexterity:** {33}
                                **Will:** {34}
                                **Constitution:** {35}
                                **Power:** {36}
                                **Strength:** {37}
                                **Occupation:** {38}
                                **Headjack:** {39}
                                **Generation:** {40}
                                **Votes:** {41}\n
                                https://niftys.com/nft/0x28e4b03bc88b59d25f3467b2252b66d4b2c43286/{42}""".format(avatarnumber, avatar_owner, avatar_discord_owner, avatar_name, avatar_headwear, avatar_hair_style, avatar_hair_color, avatar_hair_dye, avatar_facial_hair, avatar_facial_expression, avatar_glasses, avatar_piercings, avatar_neckwear, avatar_front_neck_tattoo, avatar_side_neck_tattoo, avatar_bicep_tattoo, avatar_forearm_tattoo, avatar_top, avatar_bottom, avatar_footwear, avatar_ring, avatar_wristwear, avatar_right_hand_accessory, avatar_left_hand_accessory, avatar_background, int(avatar_wisdom)+int(avatar_intelligence)+int(avatar_charisma)+int(avatar_dexterity)+int(avatar_constitution)+int(avatar_strength), avatar_awareness, avatar_wisdom, avatar_perception, avatar_intelligence, avatar_persuasion, avatar_charisma, avatar_movement, avatar_dexterity, avatar_will, avatar_constitution, avatar_power, avatar_strength, avatar_occupation, avatar_headjack, avatar_generation, avatar_votes, avatarnumber)
        await message.edit_original_message(content = "", embed = embed)

#Defines the presidenttupper slash command (easter egg)
@bot.slash_command(guild_ids=[869370430287384576], description = "2024")
async def presidenttupper(ctx):
    await ctx.respond("https://i.imgur.com/hKYgyMW.jpg")

'''
#Defines the puddytat slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Claim sylvester coins")
async def puddytat(ctx):
    commandUser = ctx.author
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select balance from vault where discord_user_id = {0}".format(commandUser.id)
    cur.execute(command)
    userBalance = cur.fetchall()
    cur.close()
    conn.close()
    if userBalance == []:
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 11000, {1})".format(commandUser.id, int(time.time()))
        cur.execute(command)
        command = "insert into roadmapcoins (discord_user_id) values ({0})".format(commandUser.id)
        cur.execute(command)
        cur.close()
        conn.commit()
        conn.close()
        await ctx.respond("Well, hello!\n\nIt's nice to meet you!\n\nIt doesn't look like you have claimed your first daily Coin reward from the Nifty's Discord Bank yet! I'll do that for you now.\n\nYour first daily Coin claim is worth 10,000 Coins, and I have added 1,000 coins to that. That brings your current balance to 11,000 coins.\n\nFeel free to check out <#984461108347797504> for more info!")
    else:
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "select * from roadmapcoins where discord_user_id = {0}".format(commandUser.id)
        cur.execute(command)
        redeemed = cur.fetchall()
        cur.close()
        conn.close()
        if redeemed == []:
            userBalance = userBalance[0][0]
            userBalance += 1000
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "insert into roadmapcoins (discord_user_id) values ({0})".format(commandUser.id)
            cur.execute(command)
            command = "update vault set balance = {0} where discord_user_id = {1}".format(userBalance, commandUser.id)
            cur.execute(command)
            cur.close()
            conn.commit()
            conn.close()
            await ctx.respond("Success! Your new balance is 🪙"+str(userBalance)+"!")
        else:
            await ctx.respond("You have already claimed this gift!")
'''          

#Defines the shop slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Purchase items from the Nifty's Discord Shop")
async def shop(ctx):
    commandChannelID = ctx.channel.id
    commandUser = ctx.author
    lte1Role = ctx.guild.get_role(991716837995839501)
    lte2Role = ctx.guild.get_role(991718276595974195)
    syleRole = ctx.guild.get_role(1050059629738065920)
    momeRole = ctx.guild.get_role(1050067387543736322)
    modChannel = 877568938777641051
    botChannel = 965703053653192804
    bankChannel = 1060116570111758356

    '''
    if commandUser.id != 710139786404298822:
        await ctx.respond("The shop is currently closed for maintenance! Check back later!")
        return
    '''

    if commandChannelID != bankChannel:
        await ctx.respond("Please use this command in <#1060116570111758356>.")
        return

    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from wallets where discord_user_id = {0} and default_wallet = 1".format(commandUser.id)
    cur.execute(command)
    wallet = cur.fetchall()
    cur.close()
    conn.close()

    if wallet == []:
        await ctx.respond("In order to use the Discord shop, you must first link your wallet in <#971831743185297448>. For instructions, check out <#971831707735056394>.")
        return

    wallet = wallet[0][0]
    
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from discordshop where inventory > 0 or inventory is Null"
    cur.execute(command)
    shopItems = cur.fetchall()
    command = "select balance from vault where discord_user_id = {0}".format(commandUser.id)
    cur.execute(command)
    userBalance = cur.fetchall()
    cur.close()
    conn.close()

    if userBalance == []:
        userBalance = 0
    else:
        userBalance = userBalance[0][0]

    async def select_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            select.placeholder=select.values[0]
            view.clear_items()
            view.add_item(select)
            view.add_item(purchase_button)
            await interaction.response.edit_message(view = view)

    async def purchase_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            item = select.values[0]
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from discordshop where item_name = '{0}'".format(item)
            cur.execute(command)
            item = cur.fetchall()
            cur.close()
            conn.close()
            itemName = item[0][1]
            itemCost = item[0][2]
            if itemCost > userBalance:
                view.clear_items()
                await interaction.response.edit_message(content = "You cannot afford that item!", embed = None, view = view)
            else:
                view.clear_items()
                view.add_item(confirm_button)
                view.add_item(cancel_button)
                await interaction.response.edit_message(content = "Please confirm you would like to purchase a "+ itemName + " for 🪙" + str(itemCost) +".", embed = None, view = view)

    async def confirm_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            buyGITM = False
            buyAssassin = False
            buyWaterBottle = False
            buySylvester = False
            successfulPurchase = False
            item = select.values[0]
            conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
            cur = conn.cursor()
            command = "select * from discordshop where item_name = '{0}'".format(item)
            cur.execute(command)
            item = cur.fetchall()
            itemName = item[0][1]
            itemCost = item[0][2]
            itemInventory = item[0][3]

            if itemInventory < 1:
                view.clear_items()
                await interaction.response.edit_message(content = "I'm sorry, but this item has already sold out!", view = view)

            if itemName == "Looney Tunes Emoji Pack 1":
                if lte1Role in commandUser.roles:
                    view.clear_items()
                    await interaction.response.edit_message(content = "You have already purchased " + itemName + "!", view = view)
                else:
                    await commandUser.add_roles(lte1Role)
                    command = "update discordshop set inventory = {0} where item_id = 2".format(itemInventory-1)
                    cur.execute(command)
                    successfulPurchase = True
            elif itemName == "Looney Tunes Emoji Pack 2":
                if lte2Role in commandUser.roles:
                    view.clear_items()
                    await interaction.response.edit_message(content = "You have already purchased " + itemName + "!", view = view)
                else:
                    await commandUser.add_roles(lte2Role)
                    command = "update discordshop set inventory = {0} where item_id = 3".format(itemInventory-1)
                    cur.execute(command)
                    successfulPurchase = True
            elif itemName == "Tweety Avatar":
                command = "select * from discordshoptweetys where discord_user_id is Null"
                cur.execute(command)
                availableTweetys = cur.fetchall()
                command = "update discordshoptweetys set discord_user_id = {0} where prize_id = {1}".format(commandUser.id, availableTweetys[0][0])
                cur.execute(command)
                command = "update discordshop set inventory = {0} where item_id = 1".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your Tweety within a few days. <@710139786404298822>, go make that happen!")
                successfulPurchase = True
            elif itemName == "Sylvester Avatar":
                '''
                command = "select * from discordshopsylvesters where discord_user_id is Null"
                cur.execute(command)
                availableTweetys = cur.fetchall()
                command = "update discordshopsylvesters set discord_user_id = {0} where prize_id = {1}".format(commandUser.id, availableTweetys[0][0])
                cur.execute(command)
                '''
                command = "update discordshop set inventory = {0} where item_id = 5".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your Sylvester within a few hours!")
                successfulPurchase = True
                buySylvester = True
            elif itemName == "Matrix Base Avatar":
                command = "select * from discordshopmatrix where discord_user_id is Null"
                cur.execute(command)
                availableTweetys = cur.fetchall()
                command = "update discordshopmatrix set discord_user_id = {0} where prize_id = {1}".format(commandUser.id, availableTweetys[0][0])
                cur.execute(command)
                command = "update discordshop set inventory = {0} where item_id = 4".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your Matrix Avatar within a few days. <@710139786404298822>, go make that happen!")
                successfulPurchase = True
            elif itemName == "Bullet Train Assassin Avatar":
                '''
                command = "select * from discordshopassassins where discord_user_id is Null"
                cur.execute(command)
                availableTweetys = cur.fetchall()
                command = "update discordshopassassins set discord_user_id = {0} where prize_id = {1}".format(commandUser.id, availableTweetys[0][0])
                cur.execute(command)
                '''
                command = "update discordshop set inventory = {0} where item_id = 6".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your Assassin Avatar within a few hours!")
                successfulPurchase = True
                buyAssassin = True
            elif itemName == "GITM Artifact":
                '''
                command = "select * from discordshopgitm where discord_user_id is Null"
                cur.execute(command)
                availableTweetys = cur.fetchall()
                command = "update discordshopgitm set discord_user_id = {0} where prize_id = {1}".format(commandUser.id, availableTweetys[0][0])
                cur.execute(command)
                '''
                command = "update discordshop set inventory = {0} where item_id = 7".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your Glitch in the Matrix Artifact NFT within an hour!")
                successfulPurchase = True
                buyGITM = True
            elif itemName == "Sylvester Emoji Pack":
                if syleRole in commandUser.roles:
                    view.clear_items()
                    await interaction.response.edit_message(content = "You have already purchased " + itemName + "!", view = view)
                else:
                    await commandUser.add_roles(syleRole)
                    command = "update discordshop set inventory = {0} where item_id = 8".format(itemInventory-1)
                    cur.execute(command)
                    successfulPurchase = True
            elif itemName == "Momonga Emoji Pack":
                if momeRole in commandUser.roles:
                    view.clear_items()
                    await interaction.response.edit_message(content = "You have already purchased " + itemName + "!", view = view)
                else:
                    await commandUser.add_roles(momeRole)
                    command = "update discordshop set inventory = {0} where item_id = 9".format(itemInventory-1)
                    cur.execute(command)
                    successfulPurchase = True
            elif itemName == "Water Bottle Artifact":
                command = "update discordshop set inventory = {0} where item_id = 10".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your Bullet Train Water Bottle Artifact NFT within an hour!")
                successfulPurchase = True
                buyWaterBottle = True
            elif itemName == "GoT Hero Box":
                command = "update discordshop set inventory = {0} where item_id = 11".format(itemInventory-1)
                cur.execute(command)
                await ctx.send("<@" + str(commandUser.id)+">, you will receive your GoT Hero Box within a few days. <@710139786404298822>, go make that happen!")
                successfulPurchase = True
                
            if successfulPurchase:
                view.clear_items()
                nonlocal userBalance
                nonlocal wallet
                userBalance -= itemCost
                command = "update vault set balance = {0} where discord_user_id = {1}".format(userBalance, commandUser.id)
                cur.execute(command)
                conn.commit()
                await interaction.response.edit_message(content = "You have successfully purchased one " + itemName + "!", view = view)
                if buyGITM:
                    await sendGITM(wallet, 1)
                if buyAssassin:
                    await mint721("0xf49034ee4d5d6a0b6f3325a3827bf0a7e6159069", "ETHEREUM", wallet, 1)
                if buySylvester:
                    await mint721("0x6f5dcc70c39eb64d7e4b70a212367bb895e17e0b", "ETHEREUM", wallet, 1)
                if buyWaterBottle:
                    await mint1155("0xc926101089c49c57ecc64006f47a5365dc6d9786", "92500044470403", "PALM", wallet, 1)

            cur.close()
            conn.commit()
            conn.close()

    async def cancel_button_callback(interaction):
        if commandUser != interaction.user:
            await interaction.response.send_message("This is not your menu.", ephemeral = True)
        else:
            view.clear_items()
            await interaction.response.edit_message(content = "This transaction has been canceled.", view = view)
    
    itemList = "Please note that this menu is subject to change without notice.\n\nYour current balance: 🪙"+str(userBalance)+".\n\n**Shop Items:**\n``Item:                        Price:    Inventory:"
    for item in shopItems:
        if item[3] == None:
            inventory = "Unlimited"
        else:
            inventory = str(item[3])
        itemList += "\n{:<29}🪙{:<8}{:<10}".format(item[1],str(item[2]),inventory)
    itemList += "``"
    view = MyView(ctx)
    embed = discord.Embed(color=0xffffff)
    embed.title = "Welcome to the Nifty's Discord Shop!"
    embed.description = itemList
    view.message = await ctx.respond(embed=embed, view = view)
    
    #Populate our menu
    options = []
    for item in shopItems:
        options.append(discord.SelectOption(label=item[1]))
        
    select = Select(placeholder = "Purchase an Item!",
        options=options)
    select.callback = select_callback
    purchase_button = Button(label="Purchase", style = discord.ButtonStyle.blurple)
    purchase_button.callback = purchase_button_callback
    confirm_button = Button(label="Confirm", style = discord.ButtonStyle.blurple)
    confirm_button.callback = confirm_button_callback
    cancel_button = Button(label="Cancel", style = discord.ButtonStyle.blurple)
    cancel_button.callback = cancel_button_callback
    
    view.add_item(select)
    view.add_item(purchase_button)
    await view.message.edit_original_message(view = view)

@bot.command(name='balance')
async def balance(ctx, member: discord.Member=None):
    if ctx.channel.id == 1060116570111758356:
        if member is None:
            member = ctx.message.author
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "select balance from vault where discord_user_id = {0}".format(member.id)
        cur.execute(command)
        balance = cur.fetchall()
        if balance == []:
            await ctx.send("<@"+str(member.id)+"> currently has a balance of 0 coins.")
        else:
            balance = balance[0][0]
            await ctx.send("<@"+str(member.id)+"> currently has a balance of " + str(balance) + " coins.")
        cur.close()
        conn.close()

@bot.command(name='daily')
async def daily(ctx):
    if ctx.channel.id == 1060116570111758356:
        member = ctx.message.author
        conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
        cur = conn.cursor()
        command = "select * from vault where discord_user_id = {0}".format(member.id)
        cur.execute(command)
        account = cur.fetchall()
        if account == []:
            command = "insert into vault (discord_user_id, balance, daily_claimed) values ({0}, 10000, {1})".format(member.id, int(time.time()))
            cur.execute(command)
            await ctx.send("Daily claimed! Since this is your first one, you have been given 10,000 Coins!")
        else:
            account = account[0]
            eligibleToClaim = account[2] + 79200
            if eligibleToClaim < int(time.time()):
                newBalance = account[1] + 1000
                command = "update vault set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
                cur.execute(command)
                command = "update vault set daily_claimed = {0} where discord_user_id = {1}".format(int(time.time()),member.id)
                cur.execute(command)
                await ctx.send("Daily claimed! You have been given 1000 Coins bringing your Coin balance to " + str(newBalance) + ".")
            else:
                await ctx.send("You have already claimed your daily today. You may claim again <t:" + str(eligibleToClaim) +":R>.")
        cur.close()
        conn.commit()
        conn.close()

@bot.command(name='share')
async def share(ctx, member: discord.Member=None, amount = None):
    await ctx.send("This command has been disabled due to user abuse. We'll try to get a better system for trading/sharing in place!")
    if ctx.channel.id == 1060116570111758356:
        '''
        fromMember = ctx.message.author
        if member is None:
            await ctx.send("You need to specify who you're trying to send coins to!")
        elif member == fromMember:
            await ctx.send("You can't give Coins to yourself!")
        elif amount is None:
            await ctx.send("You need to specify a number of Coins you want to send!")
        else:
            try:
                amount = int(amount)
            except:
                await ctx.send("The number of coins you want to send must be an integer!")
            else:
                if amount < 0:
                    await ctx.send("Trying to steal coins from <@" + str(toMemberID) + ">? You gotta share a positive number of coins.")
                else:
                    toMemberID = member.id
                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                    cur = conn.cursor()
                    command = "select * from vault where discord_user_id = {0}".format(fromMember.id)
                    cur.execute(command)
                    fromAccount = cur.fetchall()
                    command = "select * from vault where discord_user_id = {0}".format(toMemberID)
                    cur.execute(command)
                    toAccount = cur.fetchall()
                    cur.close()
                    conn.close()
                    if fromAccount == []:
                        await ctx.send("You haven't set up an account with the Nifty's Discord Bank yet! Use the +daily command to open an account.")
                    elif toAccount == []:
                        await ctx.send("<@" + str(toMemberID) + "> hasn't set up an account with the Nifty's Discord Bank yet! The need to use the +daily command to open an account first before you can send them coins.")
                    else:
                        fromAccount = fromAccount[0]
                        toAccount = toAccount[0]
                        fromAccountBalance = fromAccount[1]
                        toAccountBalance = toAccount[1]
                        if fromAccountBalance < amount:
                            await ctx.send("You don't even have that many Coins!")
                        else:
                            async def yesButton_callback(interaction):
                                if ctx.message.author != interaction.user:
                                    await interaction.response.send_message("This is not your menu.", ephemeral = True)
                                else:
                                    nonlocal fromAccountBalance
                                    fromAccountBalance -= amount
                                    nonlocal toAccountBalance
                                    toAccountBalance += amount
                                    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
                                    cur = conn.cursor()
                                    command = "update vault set balance = {0} where discord_user_id = {1}".format(toAccountBalance, toMemberID)
                                    cur.execute(command)
                                    command = "update vault set balance = {0} where discord_user_id = {1}".format(fromAccountBalance, fromMember.id)
                                    cur.execute(command)
                                    cur.close()
                                    conn.commit()
                                    conn.close()
                                    view.clear_items()
                                    await interaction.response.edit_message(content = str(amount) + " Coins sent to <@" + str(toMemberID) + ">.", view = view)

                            async def noButton_callback(interaction):
                                if ctx.message.author != interaction.user:
                                    await interaction.response.send_message("This is not your menu.", ephemeral = True)
                                else:
                                    view.clear_items()
                                    await interaction.response.edit_message(content = "Transaction canceled.", view = view)

                            yesButton = Button(label="Yes", style = discord.ButtonStyle.blurple)
                            yesButton.callback = yesButton_callback
                            noButton = Button(label="No", style = discord.ButtonStyle.blurple)
                            noButton.callback = noButton_callback

                            view = MyView(ctx)
                            view.add_item(yesButton)
                            view.add_item(noButton)
                            
                            view.message = await ctx.send("Are you sure you want to send " + str(amount) + " Coins to <@"+str(toMemberID) + ">?", view = view)
        '''

@share.error
async def shareErrorHandler(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("You must specify who you're trying to send coins to! See <#984461108347797504> for instructions!")

#This is an easter egg. lol
@bot.command(name='steal')
async def steal(ctx):
    response = random.randint(1,7)
    if response == 1:
        await ctx.send("https://tenor.com/view/loki-dont-just-dont-stop-gif-23310589")
    elif response == 2:
        await ctx.send("https://tenor.com/view/dont-benedict-c-umberbatch-sherlock-holmes-just-dont-no-gif-4908001")
    elif response == 3:
        await ctx.send("https://tenor.com/view/son-just-dont-captain-america-chris-evans-gif-5705357")
    elif response == 4:
        await ctx.send("https://tenor.com/view/sam-wilson-falcon-ashamed-gif-10724725")
    elif response == 5:
        await ctx.send("https://tenor.com/view/ugh-donald-trump-head-shake-eye-roll-gif-6253515")
    elif response == 6:
        await ctx.send("https://tenor.com/view/we-dont-do-that-here-black-panther-tchalla-bruce-gif-16558003")
    elif response == 7:
        await ctx.send("https://tenor.com/view/daddys-home2-daddys-home2gifs-stop-it-stop-that-i-mean-it-gif-9694318")

#calls the steal command
@bot.command(name='rob')
async def rob(ctx):
    await steal(ctx)

#Defines the avatar quiz slash command
@bot.slash_command(guild_ids=[869370430287384576], description = "Which Build Your Realm avatar best represents you?")
async def avatarquiz(ctx):
    commandChannelID = ctx.channel.id
    commandUser = ctx.author
    weaponChannel = 1047547749572292669
    view = MyView(ctx, 60)
    
    if commandChannelID == weaponChannel:
        counts = [0,0,0,0,0,0,0]
        embed = discord.Embed(description="""<@""" + str(commandUser.id) +""">,\n\nWhat Build Your Realm avatar type best represents you?""", color=0x000000)
        
        async def beginButton_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                view.add_item(a1Button)
                view.add_item(b1Button)
                view.add_item(c1Button)
                view.add_item(d1Button)
                view.add_item(e1Button)
                embed.description = "**How do you react when faced with a difficult situation?**\n\nA) I try to stay calm and find a solution.\nB) I become angry and lash out.\nC) I try to stay out of the situation and avoid getting involved.\nD) I try to manipulate the situation to my advantage.\nE) I do whatever it takes to survive, even if it means making difficult or unpopular choices."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a1Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a2Button)
                view.add_item(b2Button)
                view.add_item(c2Button)
                view.add_item(d2Button)
                view.add_item(e2Button)
                embed.description = "**How do you make decisions?**\n\nA) I rely on my own instincts and experiences.\nB) I seek the counsel of others and consider their opinions.\nC) I carefully weigh the pros and cons and make logical decisions.\nD) I let my emotions guide me.\nE) I do whatever will benefit me the most."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b1Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a2Button)
                view.add_item(b2Button)
                view.add_item(c2Button)
                view.add_item(d2Button)
                view.add_item(e2Button)
                embed.description = "**How do you make decisions?**\n\nA) I rely on my own instincts and experiences.\nB) I seek the counsel of others and consider their opinions.\nC) I carefully weigh the pros and cons and make logical decisions.\nD) I let my emotions guide me.\nE) I do whatever will benefit me the most."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c1Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a2Button)
                view.add_item(b2Button)
                view.add_item(c2Button)
                view.add_item(d2Button)
                view.add_item(e2Button)
                embed.description = "**How do you make decisions?**\n\nA) I rely on my own instincts and experiences.\nB) I seek the counsel of others and consider their opinions.\nC) I carefully weigh the pros and cons and make logical decisions.\nD) I let my emotions guide me.\nE) I do whatever will benefit me the most."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d1Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a2Button)
                view.add_item(b2Button)
                view.add_item(c2Button)
                view.add_item(d2Button)
                view.add_item(e2Button)
                embed.description = "**How do you make decisions?**\n\nA) I rely on my own instincts and experiences.\nB) I seek the counsel of others and consider their opinions.\nC) I carefully weigh the pros and cons and make logical decisions.\nD) I let my emotions guide me.\nE) I do whatever will benefit me the most."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e1Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a2Button)
                view.add_item(b2Button)
                view.add_item(c2Button)
                view.add_item(d2Button)
                view.add_item(e2Button)
                embed.description = "**How do you make decisions?**\n\nA) I rely on my own instincts and experiences.\nB) I seek the counsel of others and consider their opinions.\nC) I carefully weigh the pros and cons and make logical decisions.\nD) I let my emotions guide me.\nE) I do whatever will benefit me the most."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a2Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a3Button)
                view.add_item(b3Button)
                view.add_item(c3Button)
                view.add_item(d3Button)
                view.add_item(e3Button)
                embed.description = "**How do you view the world?**\n\nA) I see the good in people and try to help them.\nB) I am cynical and distrusting of others.\nC) I see the world as a dangerous and unpredictable place.\nD) I see the world as a place full of opportunity and potential.\nE) I see the world as a battleground where only the strongest survive."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b2Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a3Button)
                view.add_item(b3Button)
                view.add_item(c3Button)
                view.add_item(d3Button)
                view.add_item(e3Button)
                embed.description = "**How do you view the world?**\n\nA) I see the good in people and try to help them.\nB) I am cynical and distrusting of others.\nC) I see the world as a dangerous and unpredictable place.\nD) I see the world as a place full of opportunity and potential.\nE) I see the world as a battleground where only the strongest survive."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c2Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[6]
                value += 1
                counts[6] = value
                view.add_item(a3Button)
                view.add_item(b3Button)
                view.add_item(c3Button)
                view.add_item(d3Button)
                view.add_item(e3Button)
                embed.description = "**How do you view the world?**\n\nA) I see the good in people and try to help them.\nB) I am cynical and distrusting of others.\nC) I see the world as a dangerous and unpredictable place.\nD) I see the world as a place full of opportunity and potential.\nE) I see the world as a battleground where only the strongest survive."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d2Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a3Button)
                view.add_item(b3Button)
                view.add_item(c3Button)
                view.add_item(d3Button)
                view.add_item(e3Button)
                embed.description = "**How do you view the world?**\n\nA) I see the good in people and try to help them.\nB) I am cynical and distrusting of others.\nC) I see the world as a dangerous and unpredictable place.\nD) I see the world as a place full of opportunity and potential.\nE) I see the world as a battleground where only the strongest survive."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e2Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a3Button)
                view.add_item(b3Button)
                view.add_item(c3Button)
                view.add_item(d3Button)
                view.add_item(e3Button)
                embed.description = "**How do you view the world?**\n\nA) I see the good in people and try to help them.\nB) I am cynical and distrusting of others.\nC) I see the world as a dangerous and unpredictable place.\nD) I see the world as a place full of opportunity and potential.\nE) I see the world as a battleground where only the strongest survive."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a3Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a4Button)
                view.add_item(b4Button)
                view.add_item(c4Button)
                view.add_item(d4Button)
                view.add_item(e4Button)
                embed.description = "**How do you relate to others?**\n\nA) I am loyal and protective of those close to me.\nB) I am friendly and try to get along with everyone.\nC) I am independent and prefer to work alone.\nD) I am private and keep my feelings to myself.\nE) I am charming and try to get what I want through my relationships with others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b3Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a4Button)
                view.add_item(b4Button)
                view.add_item(c4Button)
                view.add_item(d4Button)
                view.add_item(e4Button)
                embed.description = "**How do you relate to others?**\n\nA) I am loyal and protective of those close to me.\nB) I am friendly and try to get along with everyone.\nC) I am independent and prefer to work alone.\nD) I am private and keep my feelings to myself.\nE) I am charming and try to get what I want through my relationships with others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c3Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a4Button)
                view.add_item(b4Button)
                view.add_item(c4Button)
                view.add_item(d4Button)
                view.add_item(e4Button)
                embed.description = "**How do you relate to others?**\n\nA) I am loyal and protective of those close to me.\nB) I am friendly and try to get along with everyone.\nC) I am independent and prefer to work alone.\nD) I am private and keep my feelings to myself.\nE) I am charming and try to get what I want through my relationships with others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d3Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a4Button)
                view.add_item(b4Button)
                view.add_item(c4Button)
                view.add_item(d4Button)
                view.add_item(e4Button)
                embed.description = "**How do you relate to others?**\n\nA) I am loyal and protective of those close to me.\nB) I am friendly and try to get along with everyone.\nC) I am independent and prefer to work alone.\nD) I am private and keep my feelings to myself.\nE) I am charming and try to get what I want through my relationships with others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e3Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a4Button)
                view.add_item(b4Button)
                view.add_item(c4Button)
                view.add_item(d4Button)
                view.add_item(e4Button)
                embed.description = "**How do you relate to others?**\n\nA) I am loyal and protective of those close to me.\nB) I am friendly and try to get along with everyone.\nC) I am independent and prefer to work alone.\nD) I am private and keep my feelings to myself.\nE) I am charming and try to get what I want through my relationships with others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a4Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a5Button)
                view.add_item(b5Button)
                view.add_item(c5Button)
                view.add_item(d5Button)
                view.add_item(e5Button)
                embed.description = "**How do you view yourself?**\n\nA) I am confident in my abilities and believe in myself.\nB) I am insecure and have low self-esteem.\nC) I am proud of my heritage and place in the world.\nD) I am self-centered and only care about my own needs.\nE) I am constantly questioning myself and my place in the world."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b4Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a5Button)
                view.add_item(b5Button)
                view.add_item(c5Button)
                view.add_item(d5Button)
                view.add_item(e5Button)
                embed.description = "**How do you view yourself?**\n\nA) I am confident in my abilities and believe in myself.\nB) I am insecure and have low self-esteem.\nC) I am proud of my heritage and place in the world.\nD) I am self-centered and only care about my own needs.\nE) I am constantly questioning myself and my place in the world."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c4Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a5Button)
                view.add_item(b5Button)
                view.add_item(c5Button)
                view.add_item(d5Button)
                view.add_item(e5Button)
                embed.description = "**How do you view yourself?**\n\nA) I am confident in my abilities and believe in myself.\nB) I am insecure and have low self-esteem.\nC) I am proud of my heritage and place in the world.\nD) I am self-centered and only care about my own needs.\nE) I am constantly questioning myself and my place in the world."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d4Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a5Button)
                view.add_item(b5Button)
                view.add_item(c5Button)
                view.add_item(d5Button)
                view.add_item(e5Button)
                embed.description = "**How do you view yourself?**\n\nA) I am confident in my abilities and believe in myself.\nB) I am insecure and have low self-esteem.\nC) I am proud of my heritage and place in the world.\nD) I am self-centered and only care about my own needs.\nE) I am constantly questioning myself and my place in the world."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e4Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a5Button)
                view.add_item(b5Button)
                view.add_item(c5Button)
                view.add_item(d5Button)
                view.add_item(e5Button)
                embed.description = "**How do you view yourself?**\n\nA) I am confident in my abilities and believe in myself.\nB) I am insecure and have low self-esteem.\nC) I am proud of my heritage and place in the world.\nD) I am self-centered and only care about my own needs.\nE) I am constantly questioning myself and my place in the world."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a5Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a6Button)
                view.add_item(b6Button)
                view.add_item(c6Button)
                view.add_item(d6Button)
                view.add_item(e6Button)
                embed.description = "**What is most important to you?**\n\nA) My family and loved ones.\nB) My own personal gain.\nC) Protecting the realm.\nD) My freedom and independence.\nE) Bringing about death and destruction."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b5Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a6Button)
                view.add_item(b6Button)
                view.add_item(c6Button)
                view.add_item(d6Button)
                view.add_item(e6Button)
                embed.description = "**What is most important to you?**\n\nA) My family and loved ones.\nB) My own personal gain.\nC) Protecting the realm.\nD) My freedom and independence.\nE) Bringing about death and destruction."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c5Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a6Button)
                view.add_item(b6Button)
                view.add_item(c6Button)
                view.add_item(d6Button)
                view.add_item(e6Button)
                embed.description = "**What is most important to you?**\n\nA) My family and loved ones.\nB) My own personal gain.\nC) Protecting the realm.\nD) My freedom and independence.\nE) Bringing about death and destruction."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d5Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a6Button)
                view.add_item(b6Button)
                view.add_item(c6Button)
                view.add_item(d6Button)
                view.add_item(e6Button)
                embed.description = "**What is most important to you?**\n\nA) My family and loved ones.\nB) My own personal gain.\nC) Protecting the realm.\nD) My freedom and independence.\nE) Bringing about death and destruction."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e5Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[6]
                value += 1
                counts[6] = value
                view.add_item(a6Button)
                view.add_item(b6Button)
                view.add_item(c6Button)
                view.add_item(d6Button)
                view.add_item(e6Button)
                embed.description = "**What is most important to you?**\n\nA) My family and loved ones.\nB) My own personal gain.\nC) Protecting the realm.\nD) My freedom and independence.\nE) Bringing about death and destruction."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a6Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a7Button)
                view.add_item(b7Button)
                view.add_item(c7Button)
                view.add_item(d7Button)
                view.add_item(e7Button)
                embed.description = "**How do you approach new situations?**\n\nA) With caution and skepticism.\nB) With enthusiasm and a willingness to try new things.\nC) With a sense of duty and responsibility.\nD) With a desire to assert my dominance.\nE) With confidence and a sense of entitlement."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b6Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a7Button)
                view.add_item(b7Button)
                view.add_item(c7Button)
                view.add_item(d7Button)
                view.add_item(e7Button)
                embed.description = "**How do you approach new situations?**\n\nA) With caution and skepticism.\nB) With enthusiasm and a willingness to try new things.\nC) With a sense of duty and responsibility.\nD) With a desire to assert my dominance.\nE) With confidence and a sense of entitlement."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c6Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a7Button)
                view.add_item(b7Button)
                view.add_item(c7Button)
                view.add_item(d7Button)
                view.add_item(e7Button)
                embed.description = "**How do you approach new situations?**\n\nA) With caution and skepticism.\nB) With enthusiasm and a willingness to try new things.\nC) With a sense of duty and responsibility.\nD) With a desire to assert my dominance.\nE) With confidence and a sense of entitlement."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d6Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a7Button)
                view.add_item(b7Button)
                view.add_item(c7Button)
                view.add_item(d7Button)
                view.add_item(e7Button)
                embed.description = "**How do you approach new situations?**\n\nA) With caution and skepticism.\nB) With enthusiasm and a willingness to try new things.\nC) With a sense of duty and responsibility.\nD) With a desire to assert my dominance.\nE) With confidence and a sense of entitlement."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e6Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a7Button)
                view.add_item(b7Button)
                view.add_item(c7Button)
                view.add_item(d7Button)
                view.add_item(e7Button)
                embed.description = "**How do you approach new situations?**\n\nA) With caution and skepticism.\nB) With enthusiasm and a willingness to try new things.\nC) With a sense of duty and responsibility.\nD) With a desire to assert my dominance.\nE) With confidence and a sense of entitlement."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a7Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[6]
                value += 1
                counts[6] = value
                view.add_item(a8Button)
                view.add_item(b8Button)
                view.add_item(c8Button)
                view.add_item(d8Button)
                view.add_item(e8Button)
                embed.description = "**How do you deal with conflict?**\n\nA) I try to find a peaceful resolution.\nB) I use my words to persuade others.\nC) I use physical force to solve problems.\nD) I try to escape or avoid conflict.\nE) I use whatever means necessary to win."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b7Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a8Button)
                view.add_item(b8Button)
                view.add_item(c8Button)
                view.add_item(d8Button)
                view.add_item(e8Button)
                embed.description = "**How do you deal with conflict?**\n\nA) I try to find a peaceful resolution.\nB) I use my words to persuade others.\nC) I use physical force to solve problems.\nD) I try to escape or avoid conflict.\nE) I use whatever means necessary to win."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c7Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a8Button)
                view.add_item(b8Button)
                view.add_item(c8Button)
                view.add_item(d8Button)
                view.add_item(e8Button)
                embed.description = "**How do you deal with conflict?**\n\nA) I try to find a peaceful resolution.\nB) I use my words to persuade others.\nC) I use physical force to solve problems.\nD) I try to escape or avoid conflict.\nE) I use whatever means necessary to win."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d7Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a8Button)
                view.add_item(b8Button)
                view.add_item(c8Button)
                view.add_item(d8Button)
                view.add_item(e8Button)
                embed.description = "**How do you deal with conflict?**\n\nA) I try to find a peaceful resolution.\nB) I use my words to persuade others.\nC) I use physical force to solve problems.\nD) I try to escape or avoid conflict.\nE) I use whatever means necessary to win."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e7Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a8Button)
                view.add_item(b8Button)
                view.add_item(c8Button)
                view.add_item(d8Button)
                view.add_item(e8Button)
                embed.description = "**How do you deal with conflict?**\n\nA) I try to find a peaceful resolution.\nB) I use my words to persuade others.\nC) I use physical force to solve problems.\nD) I try to escape or avoid conflict.\nE) I use whatever means necessary to win."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a8Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[6]
                value += 1
                counts[6] = value
                view.add_item(a9Button)
                view.add_item(b9Button)
                view.add_item(c9Button)
                view.add_item(d9Button)
                view.add_item(e9Button)
                embed.description = "**How do you express your emotions?**\n\nA) I am open and honest about my feelings.\nB) I keep my emotions to myself.\nC) I let my emotions guide my actions.\nD) I try to maintain a calm and composed exterior.\nE) I use my emotions to manipulate others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b8Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a9Button)
                view.add_item(b9Button)
                view.add_item(c9Button)
                view.add_item(d9Button)
                view.add_item(e9Button)
                embed.description = "**How do you express your emotions?**\n\nA) I am open and honest about my feelings.\nB) I keep my emotions to myself.\nC) I let my emotions guide my actions.\nD) I try to maintain a calm and composed exterior.\nE) I use my emotions to manipulate others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c8Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a9Button)
                view.add_item(b9Button)
                view.add_item(c9Button)
                view.add_item(d9Button)
                view.add_item(e9Button)
                embed.description = "**How do you express your emotions?**\n\nA) I am open and honest about my feelings.\nB) I keep my emotions to myself.\nC) I let my emotions guide my actions.\nD) I try to maintain a calm and composed exterior.\nE) I use my emotions to manipulate others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d8Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a9Button)
                view.add_item(b9Button)
                view.add_item(c9Button)
                view.add_item(d9Button)
                view.add_item(e9Button)
                embed.description = "**How do you express your emotions?**\n\nA) I am open and honest about my feelings.\nB) I keep my emotions to myself.\nC) I let my emotions guide my actions.\nD) I try to maintain a calm and composed exterior.\nE) I use my emotions to manipulate others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e8Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a9Button)
                view.add_item(b9Button)
                view.add_item(c9Button)
                view.add_item(d9Button)
                view.add_item(e9Button)
                embed.description = "**How do you express your emotions?**\n\nA) I am open and honest about my feelings.\nB) I keep my emotions to myself.\nC) I let my emotions guide my actions.\nD) I try to maintain a calm and composed exterior.\nE) I use my emotions to manipulate others."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a9Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a10Button)
                view.add_item(b10Button)
                view.add_item(c10Button)
                view.add_item(d10Button)
                view.add_item(e10Button)
                embed.description = "**How do you view change?**\n\nA) I embrace change and see it as an opportunity.\nB) I resist change and prefer to stick with what is familiar.\nC) I am indifferent to change and go with the flow.\nD) I am cautious of change and carefully consider its consequences.\nE) I bring about change through any means necessary.\n"
                await interaction.response.edit_message(view = view, embed = embed)

        async def b9Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[4]
                value += 1
                counts[4] = value
                view.add_item(a10Button)
                view.add_item(b10Button)
                view.add_item(c10Button)
                view.add_item(d10Button)
                view.add_item(e10Button)
                embed.description = "**How do you view change?**\n\nA) I embrace change and see it as an opportunity.\nB) I resist change and prefer to stick with what is familiar.\nC) I am indifferent to change and go with the flow.\nD) I am cautious of change and carefully consider its consequences.\nE) I bring about change through any means necessary.\n"
                await interaction.response.edit_message(view = view, embed = embed)

        async def c9Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a10Button)
                view.add_item(b10Button)
                view.add_item(c10Button)
                view.add_item(d10Button)
                view.add_item(e10Button)
                embed.description = "**How do you view change?**\n\nA) I embrace change and see it as an opportunity.\nB) I resist change and prefer to stick with what is familiar.\nC) I am indifferent to change and go with the flow.\nD) I am cautious of change and carefully consider its consequences.\nE) I bring about change through any means necessary.\n"
                await interaction.response.edit_message(view = view, embed = embed)

        async def d9Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a10Button)
                view.add_item(b10Button)
                view.add_item(c10Button)
                view.add_item(d10Button)
                view.add_item(e10Button)
                embed.description = "**How do you view change?**\n\nA) I embrace change and see it as an opportunity.\nB) I resist change and prefer to stick with what is familiar.\nC) I am indifferent to change and go with the flow.\nD) I am cautious of change and carefully consider its consequences.\nE) I bring about change through any means necessary.\n"
                await interaction.response.edit_message(view = view, embed = embed)

        async def e9Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a10Button)
                view.add_item(b10Button)
                view.add_item(c10Button)
                view.add_item(d10Button)
                view.add_item(e10Button)
                embed.description = "**How do you view change?**\n\nA) I embrace change and see it as an opportunity.\nB) I resist change and prefer to stick with what is familiar.\nC) I am indifferent to change and go with the flow.\nD) I am cautious of change and carefully consider its consequences.\nE) I bring about change through any means necessary.\n"
                await interaction.response.edit_message(view = view, embed = embed)

        async def a10Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a11Button)
                view.add_item(b11Button)
                view.add_item(c11Button)
                view.add_item(d11Button)
                view.add_item(e11Button)
                embed.description = "**How do you approach problems?**\n\nA) I try to understand and solve the root cause.\nB) I take a practical and hands-on approach.\nC) I rely on my instincts and gut feelings.\nD) I use logical and analytical thinking.\nE) I take a trial and error approach and learn from my mistakes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b10Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a11Button)
                view.add_item(b11Button)
                view.add_item(c11Button)
                view.add_item(d11Button)
                view.add_item(e11Button)
                embed.description = "**How do you approach problems?**\n\nA) I try to understand and solve the root cause.\nB) I take a practical and hands-on approach.\nC) I rely on my instincts and gut feelings.\nD) I use logical and analytical thinking.\nE) I take a trial and error approach and learn from my mistakes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c10Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a11Button)
                view.add_item(b11Button)
                view.add_item(c11Button)
                view.add_item(d11Button)
                view.add_item(e11Button)
                embed.description = "**How do you approach problems?**\n\nA) I try to understand and solve the root cause.\nB) I take a practical and hands-on approach.\nC) I rely on my instincts and gut feelings.\nD) I use logical and analytical thinking.\nE) I take a trial and error approach and learn from my mistakes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d10Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[6]
                value += 1
                counts[6] = value
                view.add_item(a11Button)
                view.add_item(b11Button)
                view.add_item(c11Button)
                view.add_item(d11Button)
                view.add_item(e11Button)
                embed.description = "**How do you approach problems?**\n\nA) I try to understand and solve the root cause.\nB) I take a practical and hands-on approach.\nC) I rely on my instincts and gut feelings.\nD) I use logical and analytical thinking.\nE) I take a trial and error approach and learn from my mistakes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e10Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a11Button)
                view.add_item(b11Button)
                view.add_item(c11Button)
                view.add_item(d11Button)
                view.add_item(e11Button)
                embed.description = "**How do you approach problems?**\n\nA) I try to understand and solve the root cause.\nB) I take a practical and hands-on approach.\nC) I rely on my instincts and gut feelings.\nD) I use logical and analytical thinking.\nE) I take a trial and error approach and learn from my mistakes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a11Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[6]
                value += 1
                counts[6] = value
                view.add_item(a12Button)
                view.add_item(b12Button)
                view.add_item(c12Button)
                view.add_item(d12Button)
                view.add_item(e12Button)
                embed.description = "**How do you handle responsibility?**\n\nA) I take responsibility seriously and do my best to fulfill my duties.\nB) I try to avoid responsibility whenever possible.\nC) I am reliable and can be counted on to follow through.\nD) I take on as much responsibility as I can handle.\nE) I see responsibility as a burden and resent it."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b11Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a12Button)
                view.add_item(b12Button)
                view.add_item(c12Button)
                view.add_item(d12Button)
                view.add_item(e12Button)
                embed.description = "**How do you handle responsibility?**\n\nA) I take responsibility seriously and do my best to fulfill my duties.\nB) I try to avoid responsibility whenever possible.\nC) I am reliable and can be counted on to follow through.\nD) I take on as much responsibility as I can handle.\nE) I see responsibility as a burden and resent it."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c11Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a12Button)
                view.add_item(b12Button)
                view.add_item(c12Button)
                view.add_item(d12Button)
                view.add_item(e12Button)
                embed.description = "**How do you handle responsibility?**\n\nA) I take responsibility seriously and do my best to fulfill my duties.\nB) I try to avoid responsibility whenever possible.\nC) I am reliable and can be counted on to follow through.\nD) I take on as much responsibility as I can handle.\nE) I see responsibility as a burden and resent it."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d11Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a12Button)
                view.add_item(b12Button)
                view.add_item(c12Button)
                view.add_item(d12Button)
                view.add_item(e12Button)
                embed.description = "**How do you handle responsibility?**\n\nA) I take responsibility seriously and do my best to fulfill my duties.\nB) I try to avoid responsibility whenever possible.\nC) I am reliable and can be counted on to follow through.\nD) I take on as much responsibility as I can handle.\nE) I see responsibility as a burden and resent it."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e11Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a12Button)
                view.add_item(b12Button)
                view.add_item(c12Button)
                view.add_item(d12Button)
                view.add_item(e12Button)
                embed.description = "**How do you handle responsibility?**\n\nA) I take responsibility seriously and do my best to fulfill my duties.\nB) I try to avoid responsibility whenever possible.\nC) I am reliable and can be counted on to follow through.\nD) I take on as much responsibility as I can handle.\nE) I see responsibility as a burden and resent it."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a12Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a13Button)
                view.add_item(b13Button)
                view.add_item(c13Button)
                view.add_item(d13Button)
                view.add_item(e13Button)
                embed.description = "**How do you view rules and laws?**\n\nA) I follow rules and laws strictly.\nB) I follow rules and laws as long as they don't interfere with my goals.\nC) I follow rules and laws only when it is convenient.\nD) I believe in doing what is right, even if it means breaking rules and laws.\nE) I have my own set of rules and laws that I follow."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b12Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a13Button)
                view.add_item(b13Button)
                view.add_item(c13Button)
                view.add_item(d13Button)
                view.add_item(e13Button)
                embed.description = "**How do you view rules and laws?**\n\nA) I follow rules and laws strictly.\nB) I follow rules and laws as long as they don't interfere with my goals.\nC) I follow rules and laws only when it is convenient.\nD) I believe in doing what is right, even if it means breaking rules and laws.\nE) I have my own set of rules and laws that I follow."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c12Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[4]
                value += 1
                counts[4] = value
                view.add_item(a13Button)
                view.add_item(b13Button)
                view.add_item(c13Button)
                view.add_item(d13Button)
                view.add_item(e13Button)
                embed.description = "**How do you view rules and laws?**\n\nA) I follow rules and laws strictly.\nB) I follow rules and laws as long as they don't interfere with my goals.\nC) I follow rules and laws only when it is convenient.\nD) I believe in doing what is right, even if it means breaking rules and laws.\nE) I have my own set of rules and laws that I follow."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d12Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a13Button)
                view.add_item(b13Button)
                view.add_item(c13Button)
                view.add_item(d13Button)
                view.add_item(e13Button)
                embed.description = "**How do you view rules and laws?**\n\nA) I follow rules and laws strictly.\nB) I follow rules and laws as long as they don't interfere with my goals.\nC) I follow rules and laws only when it is convenient.\nD) I believe in doing what is right, even if it means breaking rules and laws.\nE) I have my own set of rules and laws that I follow."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e12Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a13Button)
                view.add_item(b13Button)
                view.add_item(c13Button)
                view.add_item(d13Button)
                view.add_item(e13Button)
                embed.description = "**How do you view rules and laws?**\n\nA) I follow rules and laws strictly.\nB) I follow rules and laws as long as they don't interfere with my goals.\nC) I follow rules and laws only when it is convenient.\nD) I believe in doing what is right, even if it means breaking rules and laws.\nE) I have my own set of rules and laws that I follow."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a13Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a14Button)
                view.add_item(b14Button)
                view.add_item(c14Button)
                view.add_item(d14Button)
                view.add_item(e14Button)
                embed.description = "**How do you view social status and class?**\n\nA) I believe in equal treatment for all, regardless of social status or class.\nB) I respect social hierarchy and believe in maintaining the proper social order.\nC) I am indifferent to social status and class.\nD) I am ambitious and strive to improve my social status.\nE) I believe in the inherent superiority of certain social classes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b13Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a14Button)
                view.add_item(b14Button)
                view.add_item(c14Button)
                view.add_item(d14Button)
                view.add_item(e14Button)
                embed.description = "**How do you view social status and class?**\n\nA) I believe in equal treatment for all, regardless of social status or class.\nB) I respect social hierarchy and believe in maintaining the proper social order.\nC) I am indifferent to social status and class.\nD) I am ambitious and strive to improve my social status.\nE) I believe in the inherent superiority of certain social classes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c13Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a14Button)
                view.add_item(b14Button)
                view.add_item(c14Button)
                view.add_item(d14Button)
                view.add_item(e14Button)
                embed.description = "**How do you view social status and class?**\n\nA) I believe in equal treatment for all, regardless of social status or class.\nB) I respect social hierarchy and believe in maintaining the proper social order.\nC) I am indifferent to social status and class.\nD) I am ambitious and strive to improve my social status.\nE) I believe in the inherent superiority of certain social classes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d13Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a14Button)
                view.add_item(b14Button)
                view.add_item(c14Button)
                view.add_item(d14Button)
                view.add_item(e14Button)
                embed.description = "**How do you view social status and class?**\n\nA) I believe in equal treatment for all, regardless of social status or class.\nB) I respect social hierarchy and believe in maintaining the proper social order.\nC) I am indifferent to social status and class.\nD) I am ambitious and strive to improve my social status.\nE) I believe in the inherent superiority of certain social classes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e13Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a14Button)
                view.add_item(b14Button)
                view.add_item(c14Button)
                view.add_item(d14Button)
                view.add_item(e14Button)
                embed.description = "**How do you view social status and class?**\n\nA) I believe in equal treatment for all, regardless of social status or class.\nB) I respect social hierarchy and believe in maintaining the proper social order.\nC) I am indifferent to social status and class.\nD) I am ambitious and strive to improve my social status.\nE) I believe in the inherent superiority of certain social classes."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a14Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                view.add_item(a15Button)
                view.add_item(b15Button)
                view.add_item(c15Button)
                view.add_item(d15Button)
                view.add_item(e15Button)
                embed.description = "**How do you view loyalty?**\n\nA) Loyalty is very important to me and I am fiercely loyal to those close to me.\nB) Loyalty is important to me, but I also value my own independence.\nC) Loyalty is not a priority for me.\nD) Loyalty is a necessity in the relationships I form.\nE) Loyalty is a tool that I use to further my own goals."
                await interaction.response.edit_message(view = view, embed = embed)

        async def b14Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                view.add_item(a15Button)
                view.add_item(b15Button)
                view.add_item(c15Button)
                view.add_item(d15Button)
                view.add_item(e15Button)
                embed.description = "**How do you view loyalty?**\n\nA) Loyalty is very important to me and I am fiercely loyal to those close to me.\nB) Loyalty is important to me, but I also value my own independence.\nC) Loyalty is not a priority for me.\nD) Loyalty is a necessity in the relationships I form.\nE) Loyalty is a tool that I use to further my own goals."
                await interaction.response.edit_message(view = view, embed = embed)

        async def c14Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[2]
                value += 1
                counts[2] = value
                view.add_item(a15Button)
                view.add_item(b15Button)
                view.add_item(c15Button)
                view.add_item(d15Button)
                view.add_item(e15Button)
                embed.description = "**How do you view loyalty?**\n\nA) Loyalty is very important to me and I am fiercely loyal to those close to me.\nB) Loyalty is important to me, but I also value my own independence.\nC) Loyalty is not a priority for me.\nD) Loyalty is a necessity in the relationships I form.\nE) Loyalty is a tool that I use to further my own goals."
                await interaction.response.edit_message(view = view, embed = embed)

        async def d14Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                view.add_item(a15Button)
                view.add_item(b15Button)
                view.add_item(c15Button)
                view.add_item(d15Button)
                view.add_item(e15Button)
                embed.description = "**How do you view loyalty?**\n\nA) Loyalty is very important to me and I am fiercely loyal to those close to me.\nB) Loyalty is important to me, but I also value my own independence.\nC) Loyalty is not a priority for me.\nD) Loyalty is a necessity in the relationships I form.\nE) Loyalty is a tool that I use to further my own goals."
                await interaction.response.edit_message(view = view, embed = embed)

        async def e14Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                view.clear_items()
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                view.add_item(a15Button)
                view.add_item(b15Button)
                view.add_item(c15Button)
                view.add_item(d15Button)
                view.add_item(e15Button)
                embed.description = "**How do you view loyalty?**\n\nA) Loyalty is very important to me and I am fiercely loyal to those close to me.\nB) Loyalty is important to me, but I also value my own independence.\nC) Loyalty is not a priority for me.\nD) Loyalty is a necessity in the relationships I form.\nE) Loyalty is a tool that I use to further my own goals."
                await interaction.response.edit_message(view = view, embed = embed)

        async def a15Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                await finalMessage(interaction)

        async def b15Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                nonlocal counts
                value = counts[1]
                value += 1
                counts[1] = value
                await finalMessage(interaction)

        async def c15Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                nonlocal counts
                value = counts[3]
                value += 1
                counts[3] = value
                await finalMessage(interaction)

        async def d15Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                nonlocal counts
                value = counts[0]
                value += 1
                counts[0] = value
                await finalMessage(interaction)

        async def e15Button_callback(interaction):
            if commandUser != interaction.user:
                await interaction.response.send_message("This is not your quiz!", ephemeral = True)
            else:
                nonlocal counts
                value = counts[5]
                value += 1
                counts[5] = value
                await finalMessage(interaction)

        async def finalMessage(interaction):
            view.clear_items()
            nonlocal counts
            commoner = float(counts[0])/15.0
            counts[0] = commoner
            noble = float(counts[1])/15.0
            counts[1] = noble
            manAtArms = float(counts[2])/15.0
            counts[2] = manAtArms
            freeFolk = float(counts[3])/13.0
            counts[3] = freeFolk
            nightsWatch = float(counts[4])/2.0
            counts[4] = nightsWatch
            whiteWalkers = float(counts[5])/8.0
            counts[5] = whiteWalkers
            maesters = float(counts[6])/7.0
            counts[6] = maesters
            maxValue = max(counts)
            if counts[0] == maxValue:
                embed.title = "Commoner"
                embed.description = """'Commoner' - The name doesn’t do it justice. Commoners typically have a strong sense of loyalty and honor. They are often brave and courageous, willing to fight for what they believe in. They are also often wise and calculating, able to make difficult decisions in difficult situations."""
            if counts[1] == maxValue:
                embed.title = "Noble"
                embed.description = """As a noble, you have a strong sense of honor, loyalty, and justice. You are often seen as wise and courageous, willing to make difficult decisions for the greater good. You are also often seen as having a strong sense of duty and responsibility, and are willing to put their own lives at risk to protect their people/house."""
            if counts[2] == maxValue:
                embed.title = "Man-at-Arms"
                embed.description = """Men-at-arms are typically portrayed as loyal, brave, and honorable. They are often willing to put their lives on the line to protect their lords and ladies, and they are willing to fight for what they believe in. They are also often portrayed as having a strong sense of justice and a willingness to stand up for the weak and oppressed."""
            if counts[3] == maxValue:
                embed.title = "Free Folk"
                embed.description = """Free Folk have a reputation for being barbaric and uncivilized, but this is not necessarily true of all of them. Many Free Folk are simply trying to survive in a harsh environment, and their actions and behaviors may be shaped by their circumstances. Some Free Folk are kind and noble, while others are cruel and violent. Overall, the Free Folk can be seen as a diverse group with a range of personalities, just like any other group of people."""
            if counts[4] == maxValue:
                embed.title = "The Night's Watch"
                embed.description = """The Night's Watch is sworn to protect the realm and to hold no lands or titles, living a life of service and duty. The men of the Night's Watch come from all walks of life and possess a wide range of personalities. Some are honorable and devoted to their duty, while others are more cynical and are only there because they have nowhere else to go. Overall, the Night's Watch is a diverse group, but they are united in their commitment to defend the realm."""
            if counts[5] == maxValue:
                embed.title = "White Walkers"
                embed.description = """You were matched with White Walkers... Interesting... White Walkers do not appear to think or feel in the same way that humans do."""
            if counts[6] == maxValue:
                embed.title = "Maesters"
                embed.description = """Maesters are expected to be objective and neutral, and to serve the greater good rather than the interests of any one person or house."""
            await interaction.response.edit_message(view = view, embed = embed)
                

        beginButton = Button(label="Begin", style = discord.ButtonStyle.blurple)
        beginButton.callback = beginButton_callback
        a1Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a1Button.callback = a1Button_callback
        b1Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b1Button.callback = b1Button_callback
        c1Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c1Button.callback = c1Button_callback
        d1Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d1Button.callback = d1Button_callback
        e1Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e1Button.callback = e1Button_callback
        a2Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a2Button.callback = a2Button_callback
        b2Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b2Button.callback = b2Button_callback
        c2Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c2Button.callback = c2Button_callback
        d2Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d2Button.callback = d2Button_callback
        e2Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e2Button.callback = e2Button_callback
        a3Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a3Button.callback = a3Button_callback
        b3Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b3Button.callback = b3Button_callback
        c3Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c3Button.callback = c3Button_callback
        d3Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d3Button.callback = d3Button_callback
        e3Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e3Button.callback = e3Button_callback
        a4Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a4Button.callback = a4Button_callback
        b4Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b4Button.callback = b4Button_callback
        c4Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c4Button.callback = c4Button_callback
        d4Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d4Button.callback = d4Button_callback
        e4Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e4Button.callback = e4Button_callback
        a5Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a5Button.callback = a5Button_callback
        b5Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b5Button.callback = b5Button_callback
        c5Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c5Button.callback = c5Button_callback
        d5Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d5Button.callback = d5Button_callback
        e5Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e5Button.callback = e5Button_callback
        a6Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a6Button.callback = a6Button_callback
        b6Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b6Button.callback = b6Button_callback
        c6Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c6Button.callback = c6Button_callback
        d6Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d6Button.callback = d6Button_callback
        e6Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e6Button.callback = e6Button_callback
        a7Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a7Button.callback = a7Button_callback
        b7Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b7Button.callback = b7Button_callback
        c7Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c7Button.callback = c7Button_callback
        d7Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d7Button.callback = d7Button_callback
        e7Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e7Button.callback = e7Button_callback
        a8Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a8Button.callback = a8Button_callback
        b8Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b8Button.callback = b8Button_callback
        c8Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c8Button.callback = c8Button_callback
        d8Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d8Button.callback = d8Button_callback
        e8Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e8Button.callback = e8Button_callback
        a9Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a9Button.callback = a9Button_callback
        b9Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b9Button.callback = b9Button_callback
        c9Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c9Button.callback = c9Button_callback
        d9Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d9Button.callback = d9Button_callback
        e9Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e9Button.callback = e9Button_callback
        a10Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a10Button.callback = a10Button_callback
        b10Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b10Button.callback = b10Button_callback
        c10Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c10Button.callback = c10Button_callback
        d10Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d10Button.callback = d10Button_callback
        e10Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e10Button.callback = e10Button_callback
        a11Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a11Button.callback = a11Button_callback
        b11Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b11Button.callback = b11Button_callback
        c11Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c11Button.callback = c11Button_callback
        d11Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d11Button.callback = d11Button_callback
        e11Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e11Button.callback = e11Button_callback
        a12Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a12Button.callback = a12Button_callback
        b12Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b12Button.callback = b12Button_callback
        c12Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c12Button.callback = c12Button_callback
        d12Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d12Button.callback = d12Button_callback
        e12Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e12Button.callback = e12Button_callback
        a13Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a13Button.callback = a13Button_callback
        b13Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b13Button.callback = b13Button_callback
        c13Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c13Button.callback = c13Button_callback
        d13Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d13Button.callback = d13Button_callback
        e13Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e13Button.callback = e13Button_callback
        a14Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a14Button.callback = a14Button_callback
        b14Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b14Button.callback = b14Button_callback
        c14Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c14Button.callback = c14Button_callback
        d14Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d14Button.callback = d14Button_callback
        e14Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e14Button.callback = e14Button_callback
        a15Button = Button(label="A", style = discord.ButtonStyle.blurple)
        a15Button.callback = a15Button_callback
        b15Button = Button(label="B", style = discord.ButtonStyle.blurple)
        b15Button.callback = b15Button_callback
        c15Button = Button(label="C", style = discord.ButtonStyle.blurple)
        c15Button.callback = c15Button_callback
        d15Button = Button(label="D", style = discord.ButtonStyle.blurple)
        d15Button.callback = d15Button_callback
        e15Button = Button(label="E", style = discord.ButtonStyle.blurple)
        e15Button.callback = e15Button_callback
        
        view.add_item(beginButton)
        view.message = await ctx.respond(embed = embed, view = view)    

@bot.command(name='collect')
async def collect(ctx):
    if ctx.channel.id != 1044082179287818250:
        return
    member = ctx.message.author
    outcome = random.randint(1,100)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from pretzelsalt where discord_user_id = {0}".format(member.id)
    cur.execute(command)
    status = cur.fetchall()
    if status == []:
        command = "insert into pretzelsalt (discord_user_id, balance, cooldown_time) values ({0}, 0, {1})".format(member.id, int(time.time()))
        cur.execute(command)
        conn.commit()
        account = member.id
        balance = 0
        eligibleToClaim = int(time.time())
    else:
        account = status[0]
        eligibleToClaim = account[1]
        balance = account[2]
    if eligibleToClaim <= int(time.time()):
        if outcome > 90:
            embed = discord.Embed(title = "You've been caught by the Pretzel King!", color=0x000000)
            await ctx.send(embed = embed)
            await ctx.send("https://imgur.com/c0KrDQ4")
            command = "update pretzelsalt set balance = 0 where discord_user_id = {0}".format(member.id)
            cur.execute(command)
            conn.commit()
            command = "update pretzelsalt set cooldown_time = {0} where discord_user_id = {1}".format(int(time.time())+10800,member.id)
            cur.execute(command)
            conn.commit()
        else:
            saltFound = random.randint(5,15)
            newBalance = balance + saltFound
            command = "update pretzelsalt set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
            cur.execute(command)
            conn.commit()
            await ctx.send("<@" + str(member.id) + ">, you collected " + str(saltFound) + " grains of salt. You now have " + str(newBalance) + ".")
    else:
        await ctx.send("You are still in pretzel jail. You will be released <t:" + str(eligibleToClaim) +":R>.")
    cur.close()
    conn.commit()
    conn.close()

@bot.command(name='matrixcollect')
async def matrixcollect(ctx):
    if ctx.channel.id != 1069634512490877008 and ctx.channel.id != 1069700044585979944:
        return
    member = ctx.message.author
    outcome = random.randint(1,100)
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    cur = conn.cursor()
    command = "select * from matrixcollect where discord_user_id = {0}".format(member.id)
    cur.execute(command)
    status = cur.fetchall()
    if status == []:
        command = "insert into matrixcollect (discord_user_id, balance, cooldown_time) values ({0}, 0, {1})".format(member.id, int(time.time()))
        cur.execute(command)
        conn.commit()
        account = member.id
        balance = 0
        eligibleToClaim = int(time.time())
    else:
        account = status[0]
        eligibleToClaim = account[1]
        balance = account[2]
    if eligibleToClaim <= int(time.time()):
        if outcome > 90:
            await ctx.send("<@" + str(member.id) + ">, you have been caught by The Twins! They confiscate all of your keys.")
            await ctx.send("https://tenor.com/view/the-matrix-the-matrix-reloaded-the-twins-gif-21388926")
            command = "update matrixcollect set balance = 0 where discord_user_id = {0}".format(member.id)
            cur.execute(command)
            conn.commit()
            command = "update matrixcollect set cooldown_time = {0} where discord_user_id = {1}".format(int(time.time())+10800,member.id)
            cur.execute(command)
            conn.commit()
        else:
            maxSalt = int(balance/10)
            if maxSalt < 15:
                maxSalt = 15
            saltFound = random.randint(maxSalt-10,maxSalt)
            newBalance = balance + saltFound
            command = "update matrixcollect set balance = {0} where discord_user_id = {1}".format(newBalance,member.id)
            cur.execute(command)
            conn.commit()
            await ctx.send("<@" + str(member.id) + ">, you collected " + str(saltFound) + " keys. You now have " + str(newBalance) + ".")
    else:
        await ctx.send("<@" + str(member.id) + ">, you are still being held by The Twins. The Oracle predicts you will be sprung free <t:" + str(eligibleToClaim) +":R>.")
    cur.close()
    conn.commit()
    conn.close()
    #Get the current list of avatars to see if the leaderboard needs to be updated
    conn = psycopg2.connect(DATABASETOKEN, sslmode='require')
    command = "select * from matrixcollect"
    cur = conn.cursor()
    cur.execute(command)
    searchResult = cur.fetchall()
    cur.close()
    conn.close()
    #Sort the list of avatars by EXP descending
    listOfAvatars = []
    for avatar in searchResult:
        listOfAvatars.append([avatar[2],avatar[0]])
    listOfAvatars.sort(reverse=True)
    #See if either participating avatar is in the top 10 EXP leaderboard. If so, we need to update it.
    i = 0
    iMax = len(listOfAvatars)
    if iMax > 10:
        iMax = 10
    leaderboardUpdate = False
    if outcome > 90:
        leaderboardUpdate = True
    while i < iMax and leaderboardUpdate == False:
        if listOfAvatars[i][1]==member.id:
            leaderboardUpdate=True
        i+=1
    if leaderboardUpdate:
        guild1 = bot.get_guild(869370430287384576)
        channel1 = discord.utils.get(guild1.channels, id=1069702139506606171)
        guild2 = bot.get_guild(930990319078637591)
        channel2 = discord.utils.get(guild2.channels, id=1069655342566359151)
        i = 0
        leaderboardString = ""
        while i < iMax:
            leaderboardString += "<@" + str(listOfAvatars[i][1]) + "> - " + str(listOfAvatars[i][0]) + " keys\n"
            i+=1
        #Clear the EXP Leaderboard channel and send the new top 10
        await channel1.purge()
        await channel2.purge()
        embed = discord.Embed(description = leaderboardString, color=0x000000)
        await channel1.send(embed = embed)
        await channel2.send(embed = embed)
    

#Runs the bot using the TOKEN defined in the environmental variables.         
bot.run(TOKEN)
