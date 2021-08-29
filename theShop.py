from conections import *

import discord
import random
import threading
from datetime import datetime
import asyncio
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType



async def open_account(user):

    user_inventory = inventory.find_one({"_id": str(user.id)})

    if user_inventory == None:
        inventory.insert_one({"_id": str(user.id), "Inventario":{"Monedero": 350}})
        inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos':{}}})
    else:
        return False

newshop = shop.find_one({"_id": "shop"})

if newshop == None:
    shop.insert_one({"_id":"shop"})

def shopTime():
    # This function runs periodically every 3600 seconds
    threading.Timer(3600, shopTime).start()

    now = datetime.now()
    current_time = now.strftime("%H")
    
    if current_time == '01':
        print('La tienda abre')
        potP = random.randrange(280, 400)
        antiP = random.randrange(650, 800)
        dagP = random.randrange(235, 330)
        ironp = random.randrange(160, 200)
        diamondpP = random.randrange(330, 375)

        potNumber = random.randrange(5, 10)
        antiNumber = random.randrange(4, 6)
        dagNumber = random.randrange(5, 7)
        ironpNumber = random.randrange(2, 5)
        diamondpNumber = random.randrange(1, 3)
        
        random_item =  random.randrange(1,100)
        
        shop.update_one({"_id": "shop"},{'$set':{'Poción de suerte <:lucky:874436858405351474>':{'cantidad':potNumber, 'precio': potP}}})
        shop.update_one({"_id": "shop"},{'$set':{'Seguro antirrobo 📜':{'cantidad': antiNumber, 'precio':antiP}}})
        shop.update_one({"_id": "shop"},{'$set':{'Daga 🗡️':{'cantidad': dagNumber, 'precio':dagP}}})
        shop.update_one({"_id":"shop"},{"$set":{"Pico de Hierro <:picohierro:875941132054442005>":{"cantidad": ironpNumber, "precio":ironp}}})
        shop.update_one({"_id":"shop"},{"$set":{"Pico de Diamante <:picodiamante:875941154263289886>":{"cantidad": diamondpNumber, "precio":diamondpP}}})
        shop.update_one({"_id":"shop"},{"$set":{"Random": random_item}})

shopTime()            

@bot.command(name = 'tienda')
async def shop_ (ctx):

    await open_account(ctx.author)
    #Discord custom emotes
    emote_pot = '<:lucky:874436858405351474>'
    emote_check = '<:checkbox:875501231651586110>'
    emote_upset = '<:blobupset:874809721943633950>'
    emote_no = '<:blobno:874809722652459048>'
    emote_nek = '<:nekoin:864645921824047156>'
    emote_ironp = '<:picohierro:875941132054442005>'
    emote_diamondp = '<:picodiamante:875941154263289886>'

    daily_shop = shop.find_one({"_id": "shop"})
    potion = daily_shop[f'Poción de suerte {emote_pot}']['cantidad']
    antithief = daily_shop['Seguro antirrobo 📜']['cantidad']
    dagger = daily_shop['Daga 🗡️']['cantidad']
    ironp = daily_shop[f'Pico de Hierro {emote_ironp}']['cantidad']
    diamondp = daily_shop[f'Pico de Diamante {emote_diamondp}']['cantidad']
    random_item = daily_shop['Random']


    potPrice = daily_shop[f'Poción de suerte {emote_pot}']['precio']
    antiPrice = daily_shop['Seguro antirrobo 📜']['precio']
    dagPrice = daily_shop['Daga 🗡️']['precio']
    ironpPrice = daily_shop[f'Pico de Hierro {emote_ironp}']['precio']
    diamondpPrice = daily_shop[f'Pico de Diamante {emote_diamondp}']['precio']

    
    dag_info = {"nombre": "Daga 🗡️", 
                "descripcion":"+8% de exito en los robos (2 usos)", 
                "precio": dagPrice,
                "cantidad":dagger,
                "emoji": '🗡️'}

    diamp_info = {"nombre": f"Pico de Diamante {emote_diamondp}",
                    "descripcion":"+100% de nekoins en las minadas (3 usos)", 
                    "precio": diamondpPrice,
                    "cantidad":diamondp,
                    "emoji": emote_diamondp}

    ironp_info = {"nombre": f"Pico de Hierro {emote_ironp}", 
                    "descripcion":"+30% de nekoins en las minadas (4 usos)", 
                    "precio": ironpPrice,
                    "cantidad":ironp,
                    "emoji": emote_ironp}
    
    if random_item <= 40:

        item_info = ironp_info

    elif random_item > 40 and random_item <= 80:

        item_info = dag_info
    else:
        item_info = diamp_info
    
    #Random item selected
    name = item_info["nombre"]
    description = item_info["descripcion"]
    price = item_info["precio"]
    amount = item_info["cantidad"]

    embed = discord.Embed(title ='Tienda', color = discord.Color.magenta())
    embed.set_image(url = 'chosee any image do you want')
    
    if potion <= 0:
        embed.add_field(name = f'Poción de suerte {emote_pot}',   
                        value = f"🚫 ***Agotado*** \n+5% de suerte en el gacha por 6h", inline = True)                  #0
        embed.add_field(name = f'| {potPrice} {emote_nek}', value = '\u200B', inline = True)                            #1
        embed.add_field(name = '\u200B', value = '\u200B', inline = True)                                               #2
    else:
        embed.add_field(name = f'Poción de suerte {emote_pot}',                                             
                        value = f"{emote_check} **Quedan: {potion}** \n+5% de suerte en el gacha por 6h", inline = True) 
        embed.add_field(name = f'| {potPrice} {emote_nek}', value = '\u200B', inline = True)                             
        embed.add_field(name = '\u200B', value = '\u200B', inline = True)                                                

    if antithief <= 0:
        embed.add_field(name = f'Seguro antirrobo 📜', 
                        value = f'🚫 ***Agotado*** \nImpide hurtos por 72h', inline = True)                              
        embed.add_field(name = f'| {antiPrice} {emote_nek}', value = '\u200B', inline = True)                            
        embed.add_field(name = '\u200B', value = '\u200B', inline = True)                                              
    else:
        embed.add_field(name = f'Seguro antirrobo 📜', 
                        value = f'{emote_check} **Quedan: {antithief}** \nImpide hurtos por 72h', inline = True)      #3
        embed.add_field(name = f'| {antiPrice} {emote_nek}', value = '\u200B', inline = True)                         #4
        embed.add_field(name = '\u200B', value = '\u200B', inline = True)                                             #5
    
    if amount <= 0:
        embed.add_field(name = name,
                        value = f'🚫 ***Agotado*** \n{description}', inline = True)                  
        embed.add_field(name = f'| {price} {emote_nek}', value = '\u200B', inline = True)            
        embed.add_field(name = '\u200B', value = '\u200B', inline = True)                                          
    else: 
        embed.add_field(name = name,
                        value = f'{emote_check} **Quedan: {amount}** \n{description}', inline = True)
        embed.add_field(name = f'| {price} {emote_nek}', value = '\u200B', inline = True)
        embed.add_field(name = '\u200B', value = '\u200B', inline = True)
    

    embed.set_footer(text = '-----------------------------------------------------------------------------------')
    
    msg = await ctx.send(embed = embed)
    emoji = item_info["emoji"]
    for emoji in [emote_pot,'📜', emoji]:
        await msg.add_reaction(emoji)

    def check(reaction, user):
        return user == ctx.author

    reaction = None
    button = False
    user = ctx.author

    while True:

        user_inventory = inventory.find_one({'_id': str(user.id)})['Inventario']
        #--------------pocion------------------------------------------------------
        if str(reaction) == emote_pot and button == False:
            
            button = True
            
            if user_inventory["Monedero"] < potPrice:
                msg1 = await ctx.send(f'Hey! no tienes para ***pagar*** eso {emote_upset}')
                await asyncio.sleep(3)
                await msg1.delete()
            else:
                
                if potion < 1:
                    
                    msg1 = await ctx.send(f'{emote_no} Este producto está ***agotado*** vuelve mañana')
                    await asyncio.sleep(2)
                    await msg1.delete()
                else:
                    potion -= 1
                    
                    if potion > 0:
                        
                        embed.set_field_at(0, name = f'Poción de suerte {emote_pot}',
                                        value = f"{emote_check} **Quedan: {potion}** \n+5% de suerte en el gacha por 6h", inline = True)                           
                    else:                           
                        embed.set_field_at(0, name = f'Poción de suerte {emote_pot}',
                                    value = f"🚫 ***Agotado*** \n+5% de suerte en el gacha por 6h", inline = True)
                        
                    await msg.edit(embed = embed) 
                    shop.update_one({"_id": "shop"},{'$set':{f'Poción de suerte {emote_pot}':{'cantidad':potion, 'precio': potPrice}}})

                    try:
                        user_inventory[f'Poción de suerte {emote_pot}']
                    except KeyError:
                        inventory.update_one({'_id': str(user.id)}, {'$set': {f'Inventario.Poción de suerte {emote_pot}': 0}})  

                    
                    inventory.update_one({'_id': str(user.id)}, {'$inc': {f'Inventario.Poción de suerte {emote_pot}': 1}})   
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -potPrice}})
                    
                    msg1 = await ctx.send(f'Has comprado una **Poción de suerte {emote_pot}** por **{potPrice}** {emote_nek}')
                    await asyncio.sleep(2)
                    await msg1.delete()


        #----------------seguro--------------------------------
        if str(reaction) == '📜' and button == False:
            button = True

            if user_inventory["Monedero"] < antiPrice:
                msg1 = await ctx.send(f'Hey! no tienes para ***pagar*** eso {emote_upset}')
                await asyncio.sleep(3)
                await msg1.delete()

            else:

                if antithief < 1:
                    
                    msg1 = await ctx.send(f'{emote_no} Este producto está ***agotado*** vuelve mañana')
                    await asyncio.sleep(2)
                    await msg1.delete()
                else:
                    antithief -= 1
                    
                    if antithief > 0:

                        embed.set_field_at(3, name = f'Seguro antirrobo 📜', 
                                            value = f'{emote_check} **Quedan: {antithief}** \nImpide hurtos por 72h', inline = True)
                    else:                         
                        embed.set_field_at(3, name = f'Seguro antirrobo 📜', 
                                        value = f'🚫 ***Agotado*** \nImpide hurtos por 72h', inline = True)
                        
                    await msg.edit(embed = embed)
                    shop.update_one({"_id": "shop"},{'$set':{'Seguro antirrobo 📜':{'cantidad':antithief, 'precio': antiPrice}}})
                    
                    

                    try:
                        user_inventory['Seguro antirrobo 📜']
                    except KeyError:
                        inventory.update_one({'_id': str(user.id)}, {'$set': {'Inventario.Seguro antirrobo 📜': 0}})  
                    
                    inventory.update_one({'_id': str(user.id)}, {'$inc': {'Inventario.Seguro antirrobo 📜': 1}})
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -antiPrice}})

                    msg1 = await ctx.send(f'Has comprado un **Seguro antirrobo 📜** por **{antiPrice}** {emote_nek}')
                    await asyncio.sleep(2)
                    await msg1.delete()
        
        
        #-------------------------daga------------------------------------
        if str(reaction) == '🗡️' and button == False:
            button = True

            if user_inventory["Monedero"] < dagPrice:
                msg1 = await ctx.send(f'Hey! no tienes para ***pagar*** eso {emote_upset}')
                await asyncio.sleep(3)
                await msg1.delete()

            else:

                if dagger < 1:
                    
                    msg1 = await ctx.send(f'{emote_no} Este producto está ***agotado*** vuelve mañana')
                    await asyncio.sleep(2)
                    await msg1.delete()
                else:
                    dagger -= 1
                    
                    if dagger > 0:

                        embed.set_field_at(6, name = f'Daga 🗡️',
                                            value = f'{emote_check} **Quedan: {dagger}** \n+8% de exito en los robos (2 usos)', inline = True)
                    else:
                        embed.set_field_at(6, name = 'Daga 🗡️',
                                    value = f'🚫 ***Agotado*** \n+8% de exito en los robos (2 usos)', inline = True)
                        
                    
                    await msg.edit(embed = embed)
                    shop.update_one({"_id": "shop"},{'$set':{'Daga 🗡️':{'cantidad':dagger, 'precio': dagPrice}}})
                    
                    try:
                        user_inventory['Daga 🗡️']
                    except KeyError:
                        inventory.update_one({'_id': str(user.id)}, {'$set': {'Inventario.Daga 🗡️': 0}})  

                    inventory.update_one({'_id': str(user.id)}, {'$inc': {'Inventario.Daga 🗡️': 1}})
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -dagPrice}})
                    
                    msg1 = await ctx.send(f'Has comprado una **daga 🗡️** por **{dagPrice}** {emote_nek}')
                    await asyncio.sleep(2)
                    await msg1.delete()


        #--------------------pico-de-hierro--------------------------------------------------------------
        if str(reaction) == emote_ironp and button == False:
            button = True

            if user_inventory["Monedero"] < ironpPrice:
                msg1 = await ctx.send(f'Hey! no tienes para ***pagar*** eso {emote_upset}')
                await asyncio.sleep(3)
                await msg1.delete()

            else:

                if ironp < 1:
                    
                    msg1 = await ctx.send(f'{emote_no} Este producto está ***agotado*** vuelve mañana')
                    await asyncio.sleep(2)
                    await msg1.delete()
                else:
                    ironp -= 1
                    
                    if ironp <= 0:
                        
                        embed.set_field_at(6, name = f'Pico de Hierro {emote_ironp}',
                                    value = f'🚫 ***Agotado*** \n25% de nekoins en las minadas (4 usos)', inline = True)                                                   
                    else:                           
                        embed.set_field_at(6, name = f'Pico de Hierro {emote_ironp}',
                                            value = f'{emote_check} **Quedan: {ironp}** \n+25% de nekoins en las minadas (4 usos)', inline = True)
                        
                    
                    await msg.edit(embed = embed)
                    shop.update_one({"_id": "shop"},{'$set':{f'Pico de Hierro {emote_ironp}':{'cantidad':ironp, 'precio': ironpPrice}}})

                    try:
                        user_inventory[f'Pico de Hierro {emote_ironp}']
                    except KeyError:
                        inventory.update_one({'_id': str(user.id)}, {'$set': {f'Inventario.Pico de Hierro {emote_ironp}': 0}})  

                    inventory.update_one({'_id': str(user.id)}, {'$inc': {f'Inventario.Pico de Hierro {emote_ironp}': 1}})
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -ironpPrice}})
                    
                    msg1 = await ctx.send(f'Has comprado un **Pico de Hierro {emote_ironp}** por **{ironpPrice}** {emote_nek}')
                    await asyncio.sleep(2)
                    await msg1.delete()
        

        #-------------------pico de diamante---------------------------------------
        if str(reaction) == emote_diamondp and button == False:
            button = True

            if user_inventory["Monedero"] < diamondpPrice:
                msg1 = await ctx.send(f'Hey! no tienes para ***pagar*** eso {emote_upset}')
                await asyncio.sleep(3)
                await msg1.delete()

            else:

                if diamondp <= 0:
                    
                    msg1 = await ctx.send(f'{emote_no} Este producto está ***agotado*** vuelve mañana')
                    await asyncio.sleep(2)
                    await msg1.delete()
                else:
                    diamondp -= 1
                    
                    if diamondp <= 0:
                        
                        print('agotao')
                        embed.set_field_at(6, name = f'Pico de Diamante {emote_diamondp}',
                                            value = f'🚫 ***Agotado*** \n45% de nekoins en las minadas (3 usos)', inline = True)
                        await msg.edit(embed = embed)
                        
                    else:
                        
                        embed.set_field_at(6, name = f'Pico de Diamante {emote_diamondp}',
                                            value = f'{emote_check} **Quedan: {diamondp}** \n+45% de nekoins en las minadas (3 usos)', inline = True)
                        await msg.edit(embed = embed)
                    
                    shop.update_one({"_id": "shop"},{'$set':{f'Pico de Diamante {emote_diamondp}':{'cantidad':diamondp, 'precio': diamondpPrice}}})

                        
                    
                    try:
                        user_inventory[f'Pico de Diamante {emote_diamondp}']
                    except KeyError:
                        inventory.update_one({'_id': str(user.id)}, {'$set': {f'Inventario.Pico de Diamante {emote_diamondp}': 0}})  

                    inventory.update_one({'_id': str(user.id)}, {'$inc': {f'Inventario.Pico de Diamante {emote_diamondp}': 1}})
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -diamondpPrice}})
                    
                    msg1 = await ctx.send(f'Has comprado un **Pico de Diamante {emote_diamondp}** por **{diamondpPrice}** {emote_nek}')
                    await asyncio.sleep(2)
                    await msg1.delete()
        else:
            pass
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout = 60.0, check = check)
            await msg.remove_reaction(reaction, user)
            await asyncio.sleep(1)
            button = False
        except:
            break
    
    await msg.clear_reactions()