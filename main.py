import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = [
    "Cheer up!",
    "Hang in there!",
    "Almost there!"
]

command = [".list", ".joke", ".quote"]

headers = {
    'Jasonchua': 'My Library (https://github.com/JasonChua1312/Anxiety)',
}

response = requests.get('https://icanhazdadjoke.com/', headers=headers)

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
        db["encouragements"] = encouragements


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('.quote'):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        if "encouragements" in db.keys():
            options = options + db["encouragements"]

        if any(word in msg for word in sad_words):
            await message.channel.send(random.choice(options))

    if msg.startswith(".new"):
        encouraging_message = msg.split(".new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith(".delete"):
        encouragements = []
        if "encouragements" in db.keys():
            index = int(msg.split(".delete", 1)[1])
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith(".list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)
    
    if msg.startswith('.joke'):
      await message.channel.send(response.text)

    if msg.startswith('.help'):
      await message.channel.send('Try typing '+ random.choice(command))
    
keep_alive()
client.run(os.getenv('TOKEN'))
