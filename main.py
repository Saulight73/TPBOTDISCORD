
from asyncio.windows_events import NULL
import os
from discord.channel import CategoryChannel
import youtube_dl
from types import NoneType
import discord
import time
import aiohttp
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions


client = commands.Bot(command_prefix='*', intents = discord.Intents.all())

load_dotenv(dotenv_path="config")




@client.command(name='cat',pass_context = True)
async def cat(ctx):
    async with aiohttp.ClientSession() as cs:
            async with cs.get("https://aws.random.cat/meow") as r:
                
                data = await r.json()
                embed = discord.Embed(
                    title="Cutty Car or not ?",
                    color = ctx.author.color
                )
                embed.set_image(url=data['file'])
                await ctx.send(embed=embed)

@client.command(name='join',pass_context = True)
async def join(ctx):
    voice_state = ctx.author.voice
    if voice_state is not None:
        channel = ctx.message.author.voice.channel
        await channel.connect() # se connect au channel vocal de l'auteur du message

    else:
         await ctx.send("Tu n'es pas dans un channel vocal je ne peux donc pas te rejoindre")

@client.command(name='leave',pass_context = True)
async def leave(ctx):
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
    else: # But if it isn't
        await ctx.send("Je ne suis pas dans channel Vocal ! Fais moi rejoindre un channel avec ***join**")

@client.command(name='create',pass_context = True)
@has_permissions(administrator=True)
async def create(ctx, argument1):
    try:
        f = open('Channel.txt')
        print("File is available for use")
        await ctx.send("Le channel auto existe déjà")
        f.close()
    except IOError:
        print('File is not accessible')
        file = open("Channel.txt", "w")
        await ctx.guild.create_voice_channel(argument1)
        for channel in ctx. guild. channels:
            if channel.name == argument1:
                wanted_channel_id = channel.id
        print(wanted_channel_id)
        file.write(str(wanted_channel_id)) 
        file.close()
    print("ok")

@client.command(name='rename',pass_context = True)
@has_permissions(administrator=True)
async def rename(ctx, argument1):
    try:
        f = open('Channel.txt')
        print("File is available for use")
        idtrouvé = int(f.read())
        for channel in ctx. guild. channels:

            if channel.id == idtrouvé:
                await channel.edit(name=argument1)
        f.close()
    except IOError:
        print('File is not accessible')
        await ctx.send("Pour renomer le channel AUTO tu doit d'abord le créer avec ***create nomdetonchannel**")


@client.command(name='delete',pass_context = True)
@has_permissions(administrator=True)
async def delete(ctx):
    try:
        f = open('Channel.txt')
        print("File is available for use")
        idtrouvé = int(f.read())
        for channel in ctx.guild.channels:

            if channel.id == idtrouvé:
                await channel.delete()
                f.close()
                os.remove('Channel.txt')
            
    except IOError:
        print('File is not accessible')
        await ctx.send("Pour supprimer le channel AUTO tu doit d'abord le créer avec ***create nomdetonchannel**")



    
@client.event
async def on_voice_state_update(member, before, after):
    
    if (before.channel is not None or before.channel is None) and after.channel is not None:
        file = open("Channel.txt")
        if after.channel.id == int(file.read()):
            await member.guild.create_category(member.name + "_private")
            B = discord.utils.get(member.guild.channels, name=member.name+"_private")
            await member.guild.create_voice_channel(member.name + "_Private_voice", category=B)
            await member.guild.create_text_channel(member.name + "_private_channel", category=B)
            
            
            for channel in member.guild.voice_channels:
                if channel.name == member.name+"_Private_voice":
                    wanted_channel_id = channel.id
                    await member.move_to(channel)

    if before.channel is not None and before.channel.name == member.name + "_Private_voice":
        existing_channel = discord.utils.get(member.guild.voice_channels, name=member.name+"_Private_voice")
        await existing_channel.delete()
        for category in member.guild.categories:          
            if category.name == member.name+"_private":
                
                await category.delete()
        for channel in member.guild.text_channels:
            name = member.name.lower()
            print(name)
            if channel.name == name+"_private_channel":
                print(channel.name)
                await channel.delete()
client.run(os.getenv("TOKEN"))




