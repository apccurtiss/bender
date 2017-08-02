import re
import json
import random
import logging
from datetime import datetime
from slackbot.bot import Bot
from slackbot.bot import listen_to
from slackbot.bot import respond_to

OUTFILE = 'quotes.json'

# Read in persistant quotes list
try:
    with open(OUTFILE) as f:
        quote_str = f.read()
        if quote_str:
            quotes = json.loads(quote_str)
        else:
            quotes = []
except FileNotFoundError:
    quotes = []

def strip_quotes(msg):
    if msg[0] is '"' and msg[-1] is '"':
        return msg[1:-1]
    return msg

# Each regex group is passed as a new argument
@respond_to("Save (.*)'s quote:? (.*)", re.IGNORECASE)
def quote(res, author, quote):
    # In format 'January 01, 1970''
    timestamp = datetime.now().strftime('%B %d, %Y')
    quotes.append({
        'author': author,
        'quote': strip_quotes(quote),
        'time': timestamp,
    })
    with open(OUTFILE, 'w') as f:
        f.write(json.dumps(quotes))

    # Reaction is a check mark instead of a message to avoid spamming everyone
    res.react('heavy_check_mark')


@listen_to("!quote (.*)", re.IGNORECASE)
def specific_quote(res, quote):
    try:
        if(int(quote) < len(quotes)):
            q = quotes[int(quote)]
            quote_strs = ['%s: "%s"\n\t-%s'%(q['time'],q['quote'],q['author'])]
            res.send(''.join(quote_strs))
        else:
            res.send("Quote Doesn't Exist")
    except:
        res.send("Bite my shiny metal ass")

@listen_to("!break (.*)", re.IGNORECASE)
def break_(res, n):
    res.send("!break n")

@respond_to('Show quotes', re.IGNORECASE)
def show_quotes(res):
    if len(quotes) is 0:
        res.send('There are no quotes! Get off your lazy ass and make some!')
    else:
        quote_strs = ['%s: "%s"\n\t-%s' % (q['time'], q['quote'], q['author'])
                for q in quotes]
        res.send('\n'.join(quote_strs))

if __name__ == "__main__":
    bot = Bot()
    bot.run()
