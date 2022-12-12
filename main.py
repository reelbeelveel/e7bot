#!/env/python3

import sys
import os
import json

import discord
from discord_ext import commands
from discord import guild
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from dotenv import load_dotenv

def init_env():
    """Load the .env file and return the token"""
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    if token is None:
        raise Exception("No token found in .env file")
    return token

def load_state():
    """Load state from json file."""
    try:
        with open("guild_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Guild data could not be found.")
        return {}
    except json.decoder.JSONDecodeError:
        print("Guild data could not be decoded.")
        return {}

