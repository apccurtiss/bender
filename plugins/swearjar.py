import re
import json
import random
from datetime import datetime
from slackbot.bot import Bot
from slackbot.bot import listen_to
from slackbot.bot import respond_to

OUTFILE = 'jar.json'

try:
    with open(OUTFILE) as f:
        jar = json.loads(f.read())
except FileNotFoundError:
    jar = {}

users = None

@listen_to('(fuck)|(shit)|(goddamn?)|(oweijf)', re.IGNORECASE)
def catch_swear(res, *swears):
    user_id = res.body['user']
    user_name = users[user_id]['name']
    stats = jar.get(user_name, {})
    print("Swears:", swears)
    for swear in swears:
        if swear is not None:
            count = stats.get(swear, 0)
            stats[swear] = count + 1
    jar[user_name] = stats

    with open(OUTFILE, 'w') as f:
        f.write(json.dumps(jar))

    res.react('slightly_frowning_face')

@respond_to("What'?s in the swear jar?", re.IGNORECASE)
def show_jar(res):
    if jar == {}:
        res.send("The jar's empty! Nobody's said anything fun yet!")
    else:
        quote_strs = ['%s:\n%s' % (u, '\n'.join(['\t%s: %d' % (x, c) for x, c in s.items()]))
                for u, s in jar.items()]
        res.send('\n'.join(quote_strs))

if __name__ == "__main__":
    bot = Bot()
    #TODO(alex) Provide a designated interface rather than leaving this hack here
    users = bot._client.users
    bot.run()
