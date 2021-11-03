import asyncio
import random
import os
import asyncio
from discord.color import Color
from discord.message import Message
from discord.utils import get

from discord.ext import commands

import config

import discord
from discord import Member, Guild, User, Client

client = commands.Bot(command_prefix="!")

#########################################################################

antworten =['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
            'Sehr unwahrscheinlich']


@client.event
async def on_ready():
    print("Ready!")
    while True:
        print("Sauber!")
        await asyncio.sleep(10)
        with open("spam_detect.txt", "r+") as file:
            file.truncate(0)
    client.loop.create_task(status_task())


async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
              discord.Colour.blue(), discord.Colour.purple()]
    while True:
        await client.change_presence(activity=discord.Game('Clean man'), status=discord.Status.online)
        if client.get_guild(658960248345853952):
            guild: Guild = client.get_guild(658960248345853952)
            role = guild.get_role(662606175862521856)
            if role:
                if role.position < guild.get_member(client.user.id).top_role.position:
                    await role.edit(colour=random.choice(colors))


def is_not_pinned(mess):
    return not mess.pinned


@client.event
async def on_message(message, mess=None):
    if message.author.bot:
        return




    ##########          ANTI Spam          ##########
    counter = 0
    with open("spam_detect.txt", "r+") as file:
        for lines in file:
            if lines.strip("\n") == str(message.author.id):
                counter+=1

        file.writelines(f"{str(message.author.id)}\n")
        if counter > 5:
            warnung = discord.Embed(title="User wurde gekickt!", description="user <@{}> wurde gekickt. reason=`Spam´".format(message.author.id), color=15158332)
            await message.channel.send(embed=warnung)
            Nachricht = discord.Embed(title="Sie wurden Gekickt!", description="reason`Spam`", color=15158332)
            await message.author.send(embed=Nachricht)
            
            
            await message.guild.ban(message.author, reason="spam")
            
            
            asyncio.sleep(2)
            
            await asyncio.sleep(1)
            await message.guild.unban(message.author)
            print("oh oh")
            asyncio.sleep(5)
            

    ##########          Clear befehl          ###########

    if message.content.startswith('!clear'):
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('`{}` Nachrichten gelöscht.'.format(len(deleted) - 1))
                    import asyncio

                    await asyncio.sleep(3)
                    await message.channel.purge(limit=1, check=is_not_pinned)

   
## Server Info ##

client.run(config.Token)