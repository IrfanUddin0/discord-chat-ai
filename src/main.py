import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime, timedelta
from typing import Dict, Any

import os

from config import DISCORD_APP_TOKEN
from tts import *

from GPT import GPT


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
guild_to_voice_client: Dict[discord.VoiceClient, Any] = dict()


@bot.event
async def on_ready():
    try:
        sync = await bot.tree.sync()
        print(f"Synced {len(sync)} command(s)")
    except Exception as e:
        print(f"Error syncing command(s):{e}")


@bot.tree.command(name="ask")
@app_commands.describe(prompt="Speak to the AI")
async def text_promt(ctx: discord.Interaction, prompt: str):
    result = GPT.make_prompt(prompt)
    await ctx.response.send_message(f'{ctx.user.name}: "{prompt}"'+'\n'+f'**BOT cyno: "{result}"**')


@bot.tree.command(name="join-channel")
async def join_channel(ctx: discord.Interaction):
    voice_client, joined = await _get_or_create_voice_client(ctx)
    if voice_client is None:
        await display_msg(ctx, "Error", "User not in channel")
    elif ctx.user.voice and voice_client.channel.id != ctx.user.voice.channel.id:
        old_channel_name = voice_client.channel.name
        await voice_client.disconnect()
        voice_client = await ctx.user.voice.channel.connect()
        new_channel_name = voice_client.channel.name
        guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())
        await display_msg(ctx, "Switched channels", f"Switched from #{old_channel_name} to #{new_channel_name}!")
    else:
        await display_msg(ctx, "Joined", "Connected to voice channel!")
        guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())


@bot.tree.command(name="kick-channel")
async def kick_vc(ctx: discord.Interaction):
    if ctx.guild.id in guild_to_voice_client:
        voice_client, _ = guild_to_voice_client.pop(ctx.guild.id)
        await voice_client.disconnect()
        await ctx.response.send_message("Disconnected from voice channel")
    else:
        await ctx.response.send_message(
            "Bot is not connected to a voice channel. Nothing to kick.", ephemeral=True
        )


@bot.tree.command(name="tts")
@app_commands.describe(text="tts text")
async def play_sound(ctx: discord.Interaction, text: str):
    await ctx.response.send_message("playing tts message in vc")
    await play_tts_in_vc(ctx, text)

async def display_msg(ctx: discord.Interaction, title: str, msg: str):
    embed = discord.Embed(title=title,
                          description=msg)
    await ctx.response.send_message(embed=embed)


def _context_to_voice_channel(ctx):
    return ctx.user.voice.channel if ctx.user.voice else None


async def _get_or_create_voice_client(ctx) -> tuple[discord.VoiceClient, bool]:
    joined = False
    if ctx.guild.id in guild_to_voice_client:
        voice_client, last_used = guild_to_voice_client[ctx.guild.id]
    else:
        voice_channel = _context_to_voice_channel(ctx)
        if voice_channel is None:
            voice_client = None
        else:
            voice_client = await voice_channel.connect()
            joined = True
    return (voice_client, joined)


async def play_tts_in_vc(ctx, text):
    voice_client, _ = await _get_or_create_voice_client(ctx)

    audio_src = query_uberduck(text)

    audio = discord.FFmpegPCMAudio(source=audio_src)
    voice_client.play(audio)


def main():
    GPT.init()
    bot.run(DISCORD_APP_TOKEN)


if __name__ == "__main__":
    main()
