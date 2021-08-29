from conections import *
from cards_info import *

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands.cooldowns import BucketType



async def the_trade(ctx, cardID, author_amount, cardName):
    
    user = ctx.author
    button = True
    
    #Custom discord emote
    emote_nek ='<:nekoin:864645921824047156>'
    emote_no = '<:blobno:874809722652459048>'

    def check(message):
        return message.author == ctx.author

    embed = discord.Embed(description = '¿A que **@usuario** quieres **vender/tradear** la carta?',
    color = discord.Color.orange())
    await ctx.send(embed = embed)
    message = await bot.wait_for('message', check = check, timeout = 15)
    

    try:
        member_id = message.mentions[0].id
        member = bot.get_user(member_id)
        await open_account(member)

        if message.author.id == member.id:
            embed = discord.Embed(description ='**No puedes** hacer intercambio **contigo mismo** ❌', color = discord.Color.red())
            await ctx.send(embed = embed)
            return

    except Exception as err:
        exception_type = type(err).__name__
        print(f'ha ocurrido un error de tipo: {exception_type}')
        embed = discord.Embed(description ='Ups el **@usuario** escrito **no** es válido ❌', color = discord.Color.red())
        await ctx.send(embed = embed)
        return
    
    

    embed = discord.Embed(description = f'**{user.display_name}** elige el **precio** a vender, escribe **0** si la quieres **regalar**',
    color = discord.Color.orange())
    await ctx.send(embed = embed)
    coins = await bot.wait_for('message', check = check, timeout = 15)
    
   
    try:
        coins = int(coins.content)
    except Exception:
        embed = discord.Embed(description ='Ups algo salió mal, intercambio **cancelado** ❌', color = discord.Color.red())
        await ctx.send(embed = embed)
        return
    

    if coins == 0:
        embed = discord.Embed(description = f'**{member.display_name}**, {user.display_name} quiere **darte** un(a) **{cardName["nombre"]}** lo **¿aceptas?**',
                color = discord.Color.orange())
       
    else:
        embed = discord.Embed(description = f'**{member.display_name}**, {user.display_name} quiere **venderte** un(a) **{cardName["nombre"]}** por **{coins}** {emote_nek} **¿aceptas?**',
                color = discord.Color.orange())
    
    await ctx.send(embed = embed)

    def check2(message):
        if message.author.id == member.id:
            return True
        else:
            False
    
    message = await bot.wait_for('message', check = check2, timeout = 15)
    

    if str(message.content).lower()  in ('si', 's', 'yes', 'y', 'chi', 'zi', 'shi'):


        if coins > 0:
                
                member_money = inventory.find_one({"_id": str(member.id)})['Inventario']['Monedero']

                if member_money < coins:
                    embed = discord.Embed(descriptions = 'Ups **no** tienes suficientes **nekoins** ❌',
                    color = discord.Color.red())
                    await ctx.send(embed = embed)
                    return

                else:    
                    inventory.update_one({"_id":str(member.id)},{"$inc": {"Inventario.Monedero": -coins}})
                    inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": coins}})
        
        try:
            privateC_member = privateCards.find_one({"_id": str(member.id)})  

            if privateC_member == None:
                privateCards.insert_one({"_id": str(member.id), cardID: 0})
            
            privateCards.update_one({"_id": str(user.id)},{'$inc':{cardID: -1}})
            privateCards.update_one({"_id": str(member.id)},{'$inc':{cardID: 1}})
            
            #Numero de cartas de la persona que usa el comando
            author_amount -= 1
            if author_amount <= 0:
                privateCards.update_one({"_id": str(user.id)}, {"$unset": {cardID: 0}})


        except Exception:
            embed = discord.Embed(description ='Ups algo salió mal, intercambio **cancelado** ❌',
            color = discord.Color.red())
            await ctx.send(embed = embed)
            return


        embed1 = discord.Embed(color = discord.Color.green())
        embed1.set_image(url = 'choose any image')
        await ctx.send(embed = embed1)
        embed = discord.Embed(description = '**Intercambio** realizado con **éxito** 🤝ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ',
        color = discord.Color.green())
        
    elif str(message.content).lower() in ('no', 'n', 'ño', 'nop'):
        embed = discord.Embed(description = f'No hay trato {emote_no}', 
        color = discord.Color.dark_orange())
    
    else:
        msg = await ctx.send('Maricón')
        await asyncio.sleep(1)
        await msg.delete()
        return

    await ctx.send(embed = embed)