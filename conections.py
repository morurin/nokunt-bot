import os 
import discord
from dotenv import load_dotenv
from pymongo import MongoClient
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

DB_URL = os.getenv('MONGO_DB_URL')
client = MongoClient(DB_URL)
db = client['your date base']



intents = discord.Intents().all()
bot = discord.Client()
bot = commands.Bot(command_prefix = '?', intents = intents)
bot.remove_command('help')



@bot.event
async def on_ready():
    print( f'{bot.user} is connected')


async def open_account(user):

    user_inventory = inventory.find_one({"_id": str(user.id)})

    if user_inventory == None:
        inventory.insert_one({"_id": str(user.id), "Inventario":{"Monedero": 350}})
        inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos':{}}})
    else:
        return False

#Date base documents in mongoDB
inventory = db['user_inventory']
shop = db['shop']
availableCards = db['available_cards']
personalCards =db['personal_cards']