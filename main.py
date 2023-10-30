import discord
from discord import app_commands

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_BOT_SECRET')
guild_id = os.getenv('GUILD_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(client)

class Connection:
    connection = None

CurrentConnection = Connection()

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Ready!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@tree.command(name = "join_channel", description = "Makes the Dodi bot join your voice channel.", guild=discord.Object(id=guild_id))
async def join_channel(interaction):
    channel = interaction.channel
    if not interaction.user.voice:
        await channel.send(f"🤖 Oopsie! I can't join the voice channel if you're not there, {interaction.user}! 🙁\n👻 It's like trying to have a conversation with a ghost – can't do that! 👻\n🔒 Make sure you're in a voice channel, and I'll be there in a jiffy! 🔓")
        return
    elif interaction.client.voice_clients:
        await channel.send(f"🤖 Hey there! I'm already grooving in a voice channel, {interaction.user}. Double the fun! 🎵🎤\n🔊 Let the party continue, ready to chat and jam. 🔊\n📢 I'm here and ready to roll, no need to rejoin! 🎉")
        return
    else:
        await channel.send(f"🎉 Wheee! It's time to party in the voice channel! 🎉\n🎤 Connecting the dots... I mean, connecting to the channel! 🎤\n🕺💃 Let's groove to the beats and chat like never before, {interaction.user}! 💬🔊")
        voice_channel = interaction.user.voice.channel
        CurrentConnection.connection = await voice_channel.connect(reconnect=True)

@tree.command(name = "leave_channel", description = "Makes the Dodi bot leave your voice channel.", guild=discord.Object(id=guild_id))
async def leave_channel(interaction):
    channel = interaction.channel
    if not interaction.client.voice_clients:
        await channel.send(f"🤖 Wait, I wasn't even in a voice channel to begin with, {interaction.user}! 😅\n🚫 Ghost bot, reporting in, there's no need for me to leave! 👻")
        return
    else:
        await channel.send(f"👋 Farewell, {interaction.user}! It's been a blast, but I must go for now. 👋\n🎤 Mic drop! Leaving the stage... I mean, the voice channel. 🎤\n🏃‍♂️ Zoom! I'm outta here. Thanks for the chitchat and tunes! 🏃‍♂️")
        for vc in interaction.client.voice_clients:
            await vc.disconnect()
        CurrentConnection.connection = None


@tree.command(name="upload_file",
              description="Here you can upload a txt file to the bot",
              guild=discord.Object(id=guild_id))
async def upload_file(interaction, file: discord.Attachment):
    try:
        if file.filename.endswith(".txt"):
            await file.save(f"textfiles/{file.id}_{file.filename}")
            await interaction.response.send_message(f"Ta-da! Your file's safely tucked away in the magical land of textfiles! 🪄✨ Just saved it as '{file.id}_{file.filename}'! Easy-peasy, right?")
        else:
            await interaction.response.send_message("Hey there! 😄 Looks like you've dropped a file, but, uh-oh, it's not a textfile! 🙅‍♂️ I'm a picky bot, you know. I only roll with files that strut their stuff with a .txt ending. 💃 So, what do you say? Got a sassy .txt file for me? 😏💬")
    except Exception:
        await interaction.response.send_message(f"failed to save file \n {Exception}")


@tree.command(name="play_sound",
              description="play a test sound",
              guild=discord.Object(id=guild_id))
async def play_sound(interaction):
    await interaction.response.send_message("now playing audio")
    CurrentConnection.connection.play(discord.FFmpegPCMAudio("test.wav"))

client.run(token)