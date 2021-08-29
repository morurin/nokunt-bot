from conections import *
from cards_info import *
from trade import the_trade

import discord
import random
import asyncio
import time
from datetime import datetime, timedelta
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType



#GACHA COMMAND 
@bot.command (name = 'gacha')
#@commands.cooldown(4, 3600, BucketType.user)
async def gaMachine (ctx):
    #Gasta nekoins por usar el comando +gacha
    await open_account(ctx.author)
    user = ctx.author
    user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
    gPrice = 125
    
    #Discord custom emotes
    emote_nek = ' <:nekoin:864645921824047156>'
    emote_pot = '<:lucky:874436858405351474>'

    now = datetime.now()
    user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']

    try:
        active = user_effects['Pocion efecto']['Estado']
        remaining = user_effects['Pocion efecto']['Tiempo restante']
        if now >= remaining:
            active = False
            
    except KeyError:
        active = False
    
    if user_inventory['Monedero']  >= gPrice:  #No olvidar cambiar a >=

        inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -gPrice}})
        user_inventory = inventory.find_one({"_id": str(user.id)})["Inventario"]
        
        for i in range(2):
            await showGacha(ctx)
        
        if active == True:
            embed = discord.Embed(description = f'{emote_pot} **{user.display_name}** has usado **{gPrice} nekoins** {emote_nek}', color = discord.Color.red())
            embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
        else:
            embed = discord.Embed(description = f'**{user.display_name}** has usado **{gPrice} nekoins** {emote_nek}', color = discord.Color.red())
            embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')

        await ctx.send(embed = embed)

    else:
        embed = discord.Embed(description = f'***{user.display_name}*** no tienes suficentes ***nekoins!*** {emote_nek}', color = discord.Color.red())
        embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
        await ctx.send(embed = embed)


async def showGacha(ctx):
    
    global rari, cardID
    user = ctx.author
    now = datetime.now()
    
    user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']
    
    try:
        active = user_effects['Pocion efecto']['Estado']
        remaining = user_effects['Pocion efecto']['Tiempo restante']
        if now >= remaining:
            inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos.Pocion efecto.Estado': False}})
            active = False
            
    except KeyError:
        active = False

    #Elige un numero aleatorio del 1 al 100000
    #If user have lucky potion active +5%
    if active == True:
        rarity = random.randrange(5000, 100001)
    else:
        rarity = random.randrange(1,100001)
    
    
    #Dependiendo del número escoge la rareza de la carta
    if rarity <= 47000:                                 
        cardID = random.choice(list(sinValor.keys()))  #Escoge una key aleatoria del diccionario sinValor
        cardInfo = sinValor.get(str(cardID))           #De la key obtenida obtiene su información
        rari = 'sinValor'                              #Guarda el nombre del dccionario para usarlo luego

        print(cardID) 
        print(cardInfo['rareza'])


    elif rarity > 47000 and rarity <= 86009:

        cardID = random.choice(list(comunes.keys()))
        cardInfo = comunes.get(str(cardID))
        rari = 'comunes'
        print(cardID) 
        print(cardInfo['rareza'])
    
    
    elif rarity > 86009 and rarity <= 98509:
        cardID = random.choice(list(raros.keys()))
        cardInfo = raros.get(str(cardID))
        rari = 'raros'
        print(cardID) 
        print(cardInfo['rareza'])
        

    elif rarity > 98509 and rarity <= 99989:
        cardID = random.choice(list(miticos.keys()))
        cardInfo = miticos.get(str(cardID))
        rari = 'miticos'

        print(cardID)    
        print(cardInfo['rareza'])
    
    elif rarity > 99989 and rarity <= 99999:
        cardID = random.choice(list(legendarios.keys()))
        cardInfo = legendarios.get(str(cardID))
        rari = 'legendarios'
        print(cardID) 
        print(cardInfo['rareza'])
    
    elif rarity == 100000:
        cardID = random.choice(list(legendariosMiticos.keys()))
        cardInfo = legendariosMiticos.get(str(cardID))
        rari = 'legendariosMiticos'
        print(cardID) 
        print(cardInfo['rareza'])
        
        
                                            
    temp = cardInfo["disponible"]
    available_cards = available.find_one({"_id": "namae"})
    

    if rari == 'sinValor':  
        pass
    else:

        if available_cards == None:
        
            available.insert_one({"_id": "namae", cardID: temp})
        
        elif cardID not in available_cards:
            available.update_one({"_id": "namae"}, {"$set":{cardID: temp}})
            
        available_cards = available.find_one({"_id": "namae"})

        if available_cards[cardID] <= 0:
            pass

        else:
            #Ahora las cartas de cada usuario se guardan aquí
            user = ctx.author  
            private_C = privateCards.find_one({"_id": str(user.id)})  

            if private_C == None:
                privateCards.insert_one({"_id": str(user.id), cardID+'-'+rari: 0})

            
            privateCards.update_one({"_id": str(user.id)}, {"$inc":{cardID+'-'+rari: 1}})
            #Resto uno a las cartas disponibles
            available.update_one({"_id": "namae"}, {"$inc":{cardID: -1}})
        

    #Aquí muestra las cartas que salen al usar el comando +gacha
    embed = discord.Embed(title = cardInfo["nombre"], description = cardInfo["descripcion"], color = discord.Color.blurple())
    embed.add_field(name = 'Rareza', value = cardInfo["rareza"] )
    embed.set_image(url = cardInfo["imagen"])
    #Muestra un footer diferente dependiendo si hay cartas disponibles o si estas no tienen valor
    if rari == 'sinValor':     
        embed.add_field(name = 'Disponible', value =  cardInfo["disponible"])
        embed.set_footer(text = 'No ganas nada', icon_url = ctx.author.avatar_url)

    elif available_cards[cardID] == 0:
        embed.set_footer(text = 'No quedan cartas disponibles!', icon_url = ctx.author.avatar_url)
        embed.add_field(name = 'Disponible', value = str(available_cards[cardID]) +'/'+ str(cardInfo["disponible"]))
    else:
        embed.add_field(name = 'Disponible', value = str(available_cards[cardID]) +'/'+ str(cardInfo["disponible"]))
        embed.set_footer(text = 'Ahora es tuyo {}!'.format(ctx.author.display_name), icon_url = ctx.author.avatar_url)
    await ctx.send (embed = embed)
    

        

#Muestra las cartas guardadas de cada usuario con el comando +cartas
@bot.command (name = 'cartas')
async def your_cards(ctx, *, member : discord.Member = None):
    
    if member == None:
        user = ctx.author
    else: 
        user = member
    
    private_C = privateCards.find_one({"_id": str(user.id)})  

    if private_C == None:

        embed = discord.Embed(description = '***Usuario sin cartas***', color = discord.Color.red())
        await ctx.send(embed = embed)
    
    
    #Creo una lista con las keys del diccionario del usuario
    del private_C["_id"]
    list_cards_keys = list(private_C)
    #Guarda la longitud de la lista
    total = len(list_cards_keys)

    #Ciclo for para crear diferentes variables de un embed
    for it in range(total): 
        #Separa la rareza y la Id de la carta en dos strings
        card_rarity = list_cards_keys[it].split('-')[1]
        card_id = list_cards_keys[it].split('-')[0]
        #Cantidad de cartas que tiene el usuario
        amountCards = private_C[list_cards_keys[it]]
        
        #Convierte el string separado anteriormente en nombre de variable, en este caso
        #es el nombre del diccionario y obtiene la información de este
        
        yourCard = globals()[card_rarity].get(card_id)
        
        #Convierte los srtrings en nombres de variables embed0,embed1 etc
        globals()['embed'+str(it)] = discord.Embed(title = yourCard["nombre"], description = yourCard["descripcion"], color = discord.Color.blurple())
        #embed = globals()['embed'+str(it)] 
        globals()['embed'+str(it)].add_field(name = 'Rareza', value = yourCard["rareza"], inline = True)
        globals()['embed'+str(it)].add_field(name = 'Cartas', value = amountCards, inline = True)
        
        #Dependiendo de la rareza muestra un valor distinto
        if yourCard["rareza"] == '⚪ Común':
            globals()['embed'+str(it)].add_field(name = 'Reciclar ♻️', value = '10-40 🪙', inline = False)
            globals()['value1'+str(it)] = 10
            globals()['value2'+str(it)] = 40

        elif yourCard["rareza"] == '🔵 Raro':
            globals()['embed'+str(it)].add_field(name = 'Reciclar ♻️', value = '40-100 🪙', inline = False)
            globals()['value1'+str(it)] = 40
            globals()['value2'+str(it)] = 100
        
        elif yourCard["rareza"] == '🟣 Mítico':
            globals()['embed'+str(it)].add_field(name = 'Reciclar ♻️', value = '100-400 🪙', inline = False)
            globals()['value1'+str(it)] = 100
            globals()['value2'+str(it)] = 400
        
        elif yourCard["rareza"] == '🟡 Legendario':
            globals()['embed'+str(it)].add_field(name = 'Reciclar ♻️', value = '300-1000 🪙', inline = False)
            globals()['value1'+str(it)] = 300
            globals()['value2'+str(it)] = 1000

        elif yourCard["rareza"] == '🔶 Legendario mítico':
            globals()['embed'+str(it)].add_field(name = 'Reciclar ♻️', value = '1000-2500 🪙', inline = False)
            globals()['value1'+str(it)] = 1000
            globals()['value2'+str(it)] = 2500
        
        globals()['embed'+str(it)].set_image(url = yourCard["imagen"])

        if member == None:
            globals()['embed'+str(it)].set_footer(text ='Cartas de {} -- {}/{}'.format(ctx.author.display_name, it+1, total), icon_url = ctx.author.avatar_url)
        else:

            globals()['embed'+str(it)].set_footer(text ='Cartas de {} -- {}/{}'.format(member.display_name, it+1, total), icon_url = member.avatar_url)
    
    #Muestra la primer varable embed y añade reacciones
    message = await ctx.send (embed = globals()['embed'+str(0)])

    if member != None:
        for emoji in ["🔻","🔺"]:
            await message.add_reaction(emoji)
    else:
        for emoji in ["🔻","🔺","♻️","🔁"]:
            await message.add_reaction(emoji)
            
    
    def check(reaction, user):
        return user == ctx.author 
    
    button = False
    reaction = None
    it = 0
    
    #Dependiendo de la reacción el mensaje embed cambia 
    while True:

        if str(reaction) == "🔻" and button == False :

            button = True
            it -= 1
            if it < 0:
                it = total - 1
            #Edita el mensaje seleccionando un embed diferente 
            await message.edit(embed = globals()['embed'+str(it)])

        
        elif str(reaction) == "🔺" and button == False:

            button = True
            it += 1
            if it > total-1:
                it = 0
            await message.edit(embed = globals()['embed'+str(it)])
            

        elif member == None:    
        
            if str(reaction) == "♻️" and button == False:
        
                button = True
                amount = private_C[list_cards_keys[it]]
                if amount > 0:
                    #Resta "uno" a la cantidad de cartas del usuario
                    pCardID = list_cards_keys[it]

                    privateCards.update_one({"_id": str(user.id)}, {"$inc":{pCardID: -1}})
                    private_C[list_cards_keys[it]] -= 1
                    amount = private_C[list_cards_keys[it]]
                    
                    
                    if amount <= 0:
                        privateCards.update_one({"_id": str(user.id)}, {"$unset": {pCardID: 1}})
                        globals()['embed'+str(it)].set_field_at(1, name= 'Cartas', value = 'N/A')
                        await message.edit(embed = globals()['embed'+str(it)])
                    else:
                        globals()['embed'+str(it)].set_field_at(1, name= 'Cartas', value = amount)
                        await message.edit(embed = globals()['embed'+str(it)])


                    val1 = globals()['value1'+str(it)]
                    val2 =globals()['value2'+str(it)]
                    #Selecciona un numero aleatorio dependiendo de la rareza
                    recicle= random.randrange(val1, val2)
                   
                    recicled = await ctx.send(f"Has **reciclado** tu carta por **{recicle} nekoins** <:nekoin:864645921824047156>")
                    await asyncio.sleep(2)
                    await recicled.delete()
                    await message.edit(embed = globals()['embed'+str(it)])

                    #Suma el dinero de la carta reciclada al monedero del usuario
                    card_id = list_cards_keys[it].split('-')[0]
                    available.update_one({"_id": "namae"}, {"$inc":{card_id: 1}})
                
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": recicle}})

                    
                else:
                    err = await ctx.send('***Ya no tienes más cartas***')
                    await asyncio.sleep(2)
                    await err.delete()
            

            elif str(reaction) == '🔁' and button == False:
                button = True
                #Separa Id de la carta y la rareza que anterioarmente
                #se unieron para poder obeter la info del diccionario
                card_rarity = list_cards_keys[it].split('-')[1]
                card_id = list_cards_keys[it].split('-')[0]
                yourCard = globals()[card_rarity].get(card_id)
                
                #Id de cada carta en el inventario de cartas Id + rareza
                pCardID = list_cards_keys[it]
                amount = private_C[list_cards_keys[it]]

                await the_trade(ctx, pCardID, amount, yourCard)
                amount -= 1

                if amount <= 0:
                        
                    globals()['embed'+str(it)].set_field_at(1, name= 'Cartas', value = 'N/A')
                    await message.edit(embed = globals()['embed'+str(it)])
                else:
                    globals()['embed'+str(it)].set_field_at(1, name= 'Cartas', value = amount)
                    await message.edit(embed = globals()['embed'+str(it)])


        else:
            pass        
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout = 60.0, check = check)
            await message.remove_reaction(reaction, user)
            button = False

        except:
            break
    
    await message.clear_reactions()