import re
import json
import random
import logging
from datetime import datetime
from slackbot.bot import listen_to
from slackbot.bot import respond_to
import slackbot.bot as bot

@listen_to("Start Game", re.IGNORECASE)
def break_(res):
    chans = bot.channels.list
    res.send("Channels: ",chans)
