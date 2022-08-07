"""Main file, starts the bot and the scheduler."""

from utils import env
from utils import config

from bot import SubjectsBot

# Get environment variables
token = env.get("TOKEN")
guild_id = int(env.get("GUILD"))
role_id = int(env.get("ROLE"))
prefix = env.get("PREFIX")

# Get config
color = config.get("color")

# Define bot
bot = SubjectsBot(guild_id, role_id, prefix, color)

# Start the bot
bot.run(token)