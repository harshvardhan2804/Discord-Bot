import os
import discord
import requests # to  make https request to api
import json 
import random
from replit import db
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']


#this is an asynchronous library so functions are done by callback



client = discord.Client(intents=discord.Intents.default()) # will create an object of discord bot

sad_words = ['sad','unhappy','depressed','pain','angry','miserable'] #make a list so that whenever bot sees them in chat it will respond

starter_encouragements = ['hurray','cheers up!','you are a gr8 person']

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] +" -"+json_data[0]['a'] # where q will be key having json data i.e. quote and a will stand for author
  return quote

#function to delete an encouragemnts
def  update_encouragements(enc_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements #to append in database

  else:
    db["encouragements"] = [enc_msg]

# function to add an encouragements
def delete_encouragements(index):
  encouragements = db["encouragements"]

  if len(encouragements) > index :
    del encouragements[index]
    db["encouragements"]=encouragements
  


@client.event #dedorator to specify event
async def on_ready():  # function will be called when our bot is ready
  print("we have been logged as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user: #if author is us then we have toreturn
    return

  if message.content=='$inspire':
    quote = get_quote()
    print("recieved message:",message.content)
    await message.channel.send(quote)

  
  if db["responding"]:
    option = starter_encouragements
    if "encouragements" in db.keys():
      option += db["encouragements"]
  
    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(option))

  
  if message.content.startswith("$new"):
    encouraging_msg = message.content.split("$new ",1)[1]
    update_encouragements(encouraging_msg)
    await message.channel.send("New encouraging messsage is added")

  
  if message.content.startswith("$del"):
    encouragements = []

    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
      
    await message.channel.send(encouragements)


  if message.content.startswith("$list"):
    encouragements = []

    if "encouragements" in db.keys():
      
      encouragements = db["encouragements"]
      
    await message.channel.send(encouragements)

    
  if message.content.startswith("$responding"):
    value = message.content.split("$responding ",1)[1]

    if value.lower() == 'true':
      db["responding"] = True
      await message.channel.send("responding is on")

    else:
      db["responding"] = False
      await message.channel.send("responding is off")



keep_alive()
client.run(my_secret)



