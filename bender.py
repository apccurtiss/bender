import re
import json
import random
import logging
from datetime import datetime
from slackbot.bot import Bot
from slackbot.bot import listen_to
from slackbot.bot import respond_to

from bender_commands import quotes
from bender_commands import slap

if __name__ == "__main__":
    bot = Bot()
    bot.run()
