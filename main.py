import discord
from discord import app_commands

import os
from dotenv import load_dotenv
import enum

from gtts import gTTS
from time import sleep
from picamera import PiCamera

load_dotenv()
token = os.getenv('DISCORD_BOT_SECRET') # TEST_TOKEN or DISCORD_BOT_SECRET
guild_id = os.getenv('GUILD_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
intents.message_content = True
tree = app_commands.CommandTree(client)

class Connection:
    connection = None

class Language(enum.Enum):
    deutsch = "de"
    english = "en"

CurrentConnection = Connection()

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guild_id))
    print("Ready!")

@tree.command(name = "join_channel", 
              description = "Makes the Dodi bot join your voice channel.", 
              guild=discord.Object(id=guild_id))
async def join_channel(interaction):
    response = interaction.response
    if not interaction.user.voice:
        await response.send_message(f"🤖 Oopsie! I can't join the voice channel if you're not there, {interaction.user}! 🙁")
        return
    elif interaction.client.voice_clients:
        await response.send_message(f"🤖 Hey there! I'm already grooving in a voice channel, {interaction.user}. 🎵🎤")
        return
    else:
        await response.send_message(f"🎉 Wheee! It's time to party in the voice channel! 🕺💃 Let's groove to the beats and chat like never before, {interaction.user}! 💬🔊")
        voice_channel = interaction.user.voice.channel
        CurrentConnection.connection = await voice_channel.connect(reconnect=True)

@tree.command(name = "leave_channel", 
              description = "Makes the Dodi bot leave your voice channel.", 
              guild=discord.Object(id=guild_id))
async def leave_channel(interaction):
    response = interaction.response
    if not interaction.client.voice_clients:
        await response.send_message(f"🤖 Wait, I wasn't even in a voice channel to begin with, {interaction.user}! 😅")
        return
    else:
        await response.send_message(f"👋 Farewell, {interaction.user}! It's been a blast, but I must go for now. 👋")
        for vc in interaction.client.voice_clients:
            await vc.disconnect()
        CurrentConnection.connection = None


@tree.command(name="upload_file",
              description="Here you can upload a txt file to the bot",
              guild=discord.Object(id=guild_id))
async def upload_file(interaction, file: discord.Attachment):
    try:
        if file.filename.endswith(".txt"):
            await interaction.response.send_message(f"⌛ Now creating {file.filename}")
            text_file_path = str(f"textfiles/{file.id}_{file.filename}")

            await file.save(text_file_path)
            await interaction.channel.send(f"💾 Your file's safely tucked away in the magical land of textfiles! 🪄✨ Just saved it as '{file.id}_{file.filename}'!")

        else:
            await interaction.response.send_message(f"🤖 Looks like you've dropped a file, but, uh-oh, it's not a textfile, {interaction.user}! 🙅‍♂️ I'm a picky bot, I only roll with files that strut their stuff with a .txt ending. 💃")
    except Exception:
        await interaction.response.send_message(f"⚠️ Failed to save file \n {Exception}")


@tree.command(name="convert_file",
              description="Here you can convert a uploaded file",
              guild=discord.Object(id=guild_id))
async def convert_file(interaction, file: str, language: Language):
    try:
        text_file_path = f"textfiles/{file}"
        if file.endswith(".txt") and os.path.exists(text_file_path):

            await interaction.response.send_message(f"⌛ Converting: {text_file_path}")
            with open(text_file_path) as f:
                data = f.read().replace('\n',' ')
            
            speaker = gTTS(text=data, lang=language.value, slow=False) 
            sound_file_path = f"soundfiles/{os.path.splitext(file)[0]}.mp3"
            speaker.save(sound_file_path)

            await interaction.channel.send(f"💾 Your sound file has been saved at the enchanted location: {sound_file_path}! Get ready to enjoy some magical sounds! 🎶🎧")
        else:
            await interaction.response.send_message("ℹ️ That file doesnt exist or isnt a .txt file.")
    except Exception:
        await interaction.response.send_message(f"⚠️ Failed to save file \n {Exception}")

        
@tree.command(name="play_sound",
              description="Plays a test sound.",
              guild=discord.Object(id=guild_id))
async def play_sound(interaction, file: str):
    sound_file_path = f"soundfiles/{file}"
    if os.path.exists(sound_file_path):
        await interaction.response.send_message(f"🎧 Now playing: {sound_file_path}")
        CurrentConnection.connection.play(discord.FFmpegPCMAudio(sound_file_path))


@tree.command(name="tell_story",
              description="Tells you a story based on a .txt file.",
              guild=discord.Object(id=guild_id))
async def tell_story(interaction, file: discord.Attachment, language: Language):
        if file.filename.endswith(".txt"):
            await interaction.response.send_message(f"🚧 Now creating: {file.filename}")
            text_file_path = str(f"textfiles/{file.id}_{file.filename}")

            await file.save(text_file_path)
            await interaction.channel.send(f"💾 Your file's safely tucked away in the magical land of textfiles! 🪄✨ Just saved it as '{file.id}_{file.filename}'!")

            with open(text_file_path) as f:
                data = f.read().replace('\n',' ')
            speaker = gTTS(text=data, lang=language.value, slow=False) 
            sound_file_path = f"soundfiles/{file.id}_{os.path.splitext(file.filename)[0]}.mp3"
            speaker.save(sound_file_path)
            await interaction.channel.send(f"💾 Your sound file has been saved as: '{file.id}_{os.path.splitext(file.filename)[0]}.mp3'!")

            if not interaction.user.voice:
                await interaction.channel.send(f"🤖 Oopsie! I can't join the voice channel if you're not there, {interaction.user}! 🙁")
                return
            elif interaction.client.voice_clients:
                await interaction.channel.send(f"🤖 Hey there! I'm already grooving in a voice channel, {interaction.user}. 🎵🎤")
            else:
                await interaction.channel.send(f"🎉 Wheee! It's time to party in the voice channel! 🕺💃 Let's groove to the beats and chat like never before, {interaction.user}! 💬🔊")
                voice_channel = interaction.user.voice.channel
                CurrentConnection.connection = await voice_channel.connect(reconnect=True)

            CurrentConnection.connection.play(discord.FFmpegPCMAudio(sound_file_path))
            

        else:
            await interaction.response.send_message(f"🤖 Looks like you've dropped a file, but, uh-oh, it's not a textfile, {interaction.user}! 🙅‍♂️ I'm a picky bot, I only roll with files that strut their stuff with a .txt ending. 💃")


@tree.command(name="snapshot",
              description="Take a picture.",
              guild=discord.Object(id=guild_id))
async def snapshot(interaction):
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)
    camera.capture('imagefiles/foo.jpg')
    await interaction.response.send_message(file=discord.File('imagefiles/foo.jpg'))


client.run(token)