import discord
from discord import app_commands

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_BOT_SECRET')
guildID = os.getenv('GUILDID')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildID))
    print("Ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tree.command(name="upload_file",
              description="Here you can upload a txt file to the bot",
              guild=discord.Object(id=guildID))
async def upload_file(interaction, file: discord.Attachment):
    try:
        if file.filename.endswith(".txt"):
            await file.save(f"textfiles/{file.id}_{file.filename}")
            await interaction.response.send_message(f"Ta-da! Your file's safely tucked away in the magical land of textfiles! 🪄✨ Just saved it as '{file.id}_{file.filename}'! Easy-peasy, right?")
        else:
            await interaction.response.send_message("Hey there! 😄 Looks like you've dropped a file, but, uh-oh, it's not a textfile! 🙅‍♂️ I'm a picky bot, you know. I only roll with files that strut their stuff with a .txt ending. 💃 So, what do you say? Got a sassy .txt file for me? 😏💬")
    except Exception:
        await interaction.response.send_message(f"failed to save file \n {Exception}")

client.run(token)