import discord
from discord import app_commands
import asyncio
from gtts import gTTS
import os
from env import TOKEN

# Set up the bot
intents = discord.Intents.default()
intents.voice_states = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Define the join command
@tree.command(
    name="dcdc",
    description="Start voice channel disconnect countdown"
)
@app_commands.describe(countdown="Countdown seconds")
async def join(interaction, countdown: int):
    """Joins a voice channel and performs a countdown with TTS."""
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        voice = await channel.connect()

        await interaction.response.send_message(f"Starting countdown from {countdown}", ephemeral=True)

        # Generate the TTS audio for the countdown
        for i in range(countdown, 0, -1):
            tts = gTTS(text=str(i), lang='en')
            tts.save("countdown.mp3")
            voice.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="countdown.mp3"))
            while voice.is_playing():
                await asyncio.sleep(0.1)  # Wait for the audio to finish playing

        # Inform the end of the countdown
        tts = gTTS(text="Bye!", lang='en')
        tts.save("complete.mp3")
        voice.play(discord.FFmpegPCMAudio(executable="ffmpeg", source="complete.mp3"))
        while voice.is_playing():
            await asyncio.sleep(0.1)

        # Disconnect all members
        for member in channel.members:
            await member.move_to(None)

        # Disconnect the bot
        await voice.disconnect()
        os.remove("countdown.mp3")
        os.remove("complete.mp3")
    else:
        await interaction.response.send_message("You are not in a voice channel.")

@client.event
async def on_ready():
    await tree.sync()

# Run the bot
client.run(TOKEN)
