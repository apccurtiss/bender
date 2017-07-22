import re
import json
from datetime import datetime
from slackbot.bot import listen_to
from slackbot.bot import respond_to

# Read in persistant quotes list
try:
    with open('quotes.json') as f:
        quotes = json.loads(f.read())
except FileNotFoundError:
    quotes = []

# Each regex group is passed as a new argument
@respond_to("Save (.*)'s quote: \"?(.*)\"?", re.IGNORECASE)
def quote(res, author, quote):
    # In format 'January 01, 1970''
    timestamp = datetime.now().strftime('%B %d, %Y')
    quotes.append({
        'author': author,
        'quote': quote,
        'time': timestamp,
    })
    with open('quotes.json', 'w') as f:
        f.write(json.dumps(quotes))
    # Reaction is a check mark instead of a message to avoid spamming everyone
    res.react('heavy_check_mark')

@respond_to('Show quotes', re.IGNORECASE)
def show_quotes(res):
    if len(quotes) is 0:
        res.send('There are no quotes! Get off your lazy ass and make some!')
    else:
        quote_strs = ['%s: "%s"\n\t-%s' % (q['time'], q['quote'], q['author'])
                for q in quotes]
        res.send('\n'.join(quote_strs))

@listen_to('Can someone help me?')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    message.reply('Yes, I can!')

    # Message is sent on the channel
    # message.send('I can help everybody!')
