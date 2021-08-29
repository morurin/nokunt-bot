# moruwubot.py
from conections import *
from gacha_cards import *
from theShop import *
from errorHandler import *

import os
import time
import random
import discord
from datetime import datetime, timedelta
from asyncio import sleep
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType



if __name__ == "__main__":
    

    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        return hours, minutes

    #----------------ECONOMY---------------------------------------------------
    async def open_account(user):

        user_inventory = inventory.find_one({"_id": str(user.id)})

        if user_inventory == None:
            inventory.insert_one({"_id": str(user.id), "Inventario":{"Monedero": 350}})
            inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos':{}}})
        else:
            return False


    
    #ECONOMY COMMANDS muestra la cantidad de nekoins
    @bot.command(pass_context = True, aliases = ['inventario', 'inve', 'perfil', 'cosas','monedero'])
    async def Nekoins(ctx):

        
        await open_account(ctx.author)
        user = ctx.author
        user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
        user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']

        #Discord custom emotes
        emote_nek = '<:nekoin:864645921824047156>'
        emote_bag = '<:bag:874859628230492180>'

        embed= discord.Embed(title = f'Perfil de {user.display_name}', color = discord.Color.orange())
        embed.add_field(name = 'Monedero 💰', value = f'**{user_inventory["Monedero"]}** {emote_nek}', inline = False)
        embed.set_thumbnail(url = user.avatar_url)

        user_inventory.pop('Monedero')
        it = []
        
        if user_inventory == {}:
            embed.add_field(name = f'Inventario {emote_bag}', value = '*vacio*', inline= False)
            embed.add_field(name = 'ㅤ', value = 'ㅤ', inline= True)
                      
        else:
            for item, value in user_inventory.items():
                
                it.append('*'+item +'  x'+str(value)+'*')
                invent = '\n'.join(it)
            
            embed.add_field(name = 'ㅤ', value = 'ㅤ', inline= True)
            embed.add_field(name = f'Inventario {emote_bag}', value = invent, inline= False)

        li = []   
        now = datetime.now()
        try:

            pot = user_effects['Pocion efecto']['Estado']
            remaining = user_effects['Pocion efecto']['Tiempo restante']

            if now >= remaining:
                pot = False
                inventory.update_one({'_id': str(user.id)}, {'$set':{'Efectos.Pocion efecto.Estado': False}})
            else:
                if pot == True:
                    time = remaining - now
                    hours, minutes = convert_timedelta(time)
                    li.append(f'🔸 Poción de Suerte:  {hours}h {minutes}m restantes')
                    effects = '\n'.join(li)
            
        except KeyError:
            pot = False

        try:
            anti = user_effects['Seguro efecto']['Estado']
            remaining = user_effects['Seguro efecto']['Tiempo restante']
            
            
            if now >= remaining:
                inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos.Seguro efecto.Estado': False}})
                anti = False
            else:
                if anti == True:
                    time = remaining - now
                    hours, minutes = convert_timedelta(time)
                    li.append(f'🔸 Seguro Antirrobo:  {hours}h {minutes}m restantes')
                    effects = '\n'.join(li)

                
        except KeyError:
            anti = False
        
        try:
            dagg = user_effects['Daga efecto']['Estado']
            usage = user_effects['Daga efecto']['Usos restantes']
            if usage <= 0:
                dagg = False
            
            if dagg == True:
                li.append(f'🔸 Daga:  {usage} usos restantes')
                effects = '\n'.join(li)
                
        except KeyError:
            dagg = False
        

        try:
            diap = user_effects['PicoD efecto']['Estado']
            usage = user_effects['PicoD efecto']['Usos restantes']
            if usage <= 0:
                diap = False
            if diap == True:
                li.append(f'🔸 Pico de Diamante:  {usage} usos restantes')
                effects = '\n'.join(li)
                
        except KeyError:
            diap = False

        try:
            ironp = user_effects['PicoH efecto']['Estado']
            usage = user_effects['PicoH efecto']['Usos restantes']
            if usage <= 0:
                ironp = False
            if ironp == True:
                li.append(f'🔸 Pico de Hierro:  {usage} usos restantes')
                effects = '\n'.join(li)
                
        except KeyError:
            ironp = False
        
        if any([pot, anti, dagg, diap, ironp]):
            embed.set_footer(text = (f'--------------------------------------------------\nEfectos activos\n{effects}'))
        else:
            embed.set_footer(text = '--------------------------------------------------')
            
        
        await ctx.send(embed = embed)
    



     #----------------------------------USAR------------------------------------------------------------
    @bot.command(name = 'usar')
    async def use_(ctx, *, item = None):
        user = ctx.author 
        item = str(item).lower()
        user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
        user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']
        
        
        #Discord custom emotes
        emote_pot = '<:lucky:874436858405351474>'
        emote_no = '<:blobno:874809722652459048>'
        emote_ironp = '<:picohierro:875941132054442005>'
        emote_diamondp = '<:picodiamante:875941154263289886>'

        #User effects 
        active = False
        exist = None

        if item  not in ['pocion', 'seguro', 'daga', 'pico hierro', 'pico diamante']:
            msg = await ctx.send(f'**{item}** no es un nombre **válido**\n\
                \n**pocion**\n**seguro**\n**daga**\n**pico hierro**\n**pico diamante**\n*Son los nombres validos*')
            await asyncio.sleep(5)
            await msg.delete()
        
        elif item == 'pocion':
            

            try:
                user_inventory[f'Poción de suerte {emote_pot}']
            except KeyError:
                msg = await ctx.send(f'{emote_no} **No tienes** este objeto en tu **Inventario**')
                await asyncio.sleep(3)
                await msg.delete()
                return

           

            try:
                active = user_effects['Pocion efecto']['Estado']
            except KeyError:
                exist = False
            
            
            if active == False or exist == False:
                
                active_potion = True
                inventory.update_one({'_id': str(user.id)}, {'$inc':{f'Inventario.Poción de suerte {emote_pot}': -1}})
                user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']

                if user_inventory[f'Poción de suerte {emote_pot}'] <= 0:
                    inventory.update_one({'_id': str(user.id)}, {'$unset': {f'Inventario.Poción de suerte {emote_pot}':0}})
                
                remaining = datetime.now() + timedelta(hours = 6)
                inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Pocion efecto.Estado': active_potion}})
                inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Pocion efecto.Tiempo restante': remaining}})


            
                await ctx.send(f'**{user.display_name}** has usado una **Poción de suerte** {emote_pot}')
            
            else:

                msg = await ctx.send(f'**No puedes** tomar más **Pociones de suerte** {emote_pot}')
                await asyncio.sleep(4)
                await msg.delete()

        elif item == 'seguro':
            

            try:
                user_inventory['Seguro antirrobo 📜']
            except KeyError:
                msg = await ctx.send(f'{emote_no} **No tienes** este objeto en tu **inventario**')
                await asyncio.sleep(3)
                await msg.delete()
                return

            

            try:
                active = user_effects['Seguro efecto']['Estado']
            except KeyError:
                exist = False
            
            
            if active == False or exist == False:
                
                active_anti = True
                inventory.update_one({'_id': str(user.id)}, {'$inc':{'Inventario.Seguro antirrobo 📜': -1}})
                user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']

                if user_inventory['Seguro antirrobo 📜'] <= 0:
                    inventory.update_one({'_id': str(user.id)}, {'$unset': {'Inventario.Seguro antirrobo 📜':0}})
                
                remaining = datetime.now() + timedelta(hours = 72)
                inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Seguro efecto.Estado': active_anti}})
                inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Seguro efecto.Tiempo restante': remaining}})
            
                await ctx.send(f'**{user.display_name}** has usado un **Seguro antirrobo 📜** ')
            
            else:

                msg = await ctx.send(f'**No puedes** usar más de un **Seguro antirrobo** 📜')
                await asyncio.sleep(4)
                await msg.delete()
                    
                    
        elif item == 'daga':
            

            try:
                user_inventory['Daga 🗡️']
            except KeyError:
                tenure = None
                msg = await ctx.send(f'{emote_no} **No tienes** este objeto en tu **inventario**')
                await asyncio.sleep(3)
                await msg.delete()
                return


            try:
                active = user_effects['Daga efecto']['Estado']
                usage = user_effects['Daga efecto']['Usos restantes']
                if usage <= 0:
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Daga efecto.Estado': False}})
                    active = False
            except KeyError:
                exist = False
            
            
            if active == False or exist == False:
                
                active_dag = True
                inventory.update_one({'_id': str(user.id)}, {'$inc':{'Inventario.Daga 🗡️': -1}})
                user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']

                if user_inventory['Daga 🗡️'] <= 0:
                    inventory.update_one({'_id': str(user.id)}, {'$unset': {'Inventario.Daga 🗡️':0}})
                

                inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Daga efecto.Estado': active_dag}})
                inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.Daga efecto.Usos restantes': 2}})
            
                await ctx.send(f'**{user.display_name}** has usado una **Daga** 🗡️ ')
            
            else:

                msg = await ctx.send(f'**No puedes** usar más de una **Daga** 🗡️ ')
                await asyncio.sleep(4)
                await msg.delete()
                    
        elif item == 'pico hierro':
            

            try:
                user_inventory[f'Pico de Hierro {emote_ironp}']
            except KeyError:
                tenure = None
                msg = await ctx.send(f'{emote_no} **No tienes** este objeto en tu **inventario**')
                await asyncio.sleep(3)
                await msg.delete()
                return


            try:
                active = user_effects['PicoH efecto']['Estado']
                usage = user_effects['PicoH efecto']['Usos restantes']
                if usage <= 0:
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.PicoH efecto.Estado': False}})
                    active = False
            except KeyError:
                exist = False
            
            try:
                otherActive = user_effects['PicoD efecto']['Estado']
            except KeyError:
                otherActive = False

            if otherActive == True:
                msg = await ctx.send(f'Ya tienes un **Pico de Diamante {emote_diamondp}  activado**')
                await asyncio.sleep(3)
                await msg.delete()
                return
            
            else:

                if active == False or exist == False:
                    
                    active_ironp = True
                    inventory.update_one({'_id': str(user.id)}, {'$inc':{f'Inventario.Pico de Hierro {emote_ironp}': -1}})
                    user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']

                    if user_inventory[f'Pico de Hierro {emote_ironp}'] <= 0:
                        inventory.update_one({'_id': str(user.id)}, {'$unset': {f'Inventario.Pico de Hierro {emote_ironp}':0}})
                    
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.PicoH efecto.Estado': active_ironp}})
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.PicoH efecto.Usos restantes': 4}})

                    await ctx.send(f'**{user.display_name}** has usado un **Pico de Hierro** {emote_ironp}')
                
                else:

                    msg = await ctx.send(f'**No puedes** usar más de un **Pico de Hierro** {emote_ironp}')
                    await asyncio.sleep(4)
                    await msg.delete()

        elif item == 'pico diamante':
            

            try:
                user_inventory[f'Pico de Diamante {emote_diamondp}']
            except KeyError:
                tenure = None
                msg = await ctx.send(f'{emote_no} **No tienes** este objeto en tu **Inventario**')
                await asyncio.sleep(3)
                await msg.delete()
                return


            try:
                active = user_effects['PicoD efecto']['Estado']
                usage = user_effects['PicoD efecto']['Usos restantes']
                if usage <= 0:
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.PicoD efecto.Estado': False}})
                    active = False
            except KeyError:
                exist = False

            try:
                otherActive = user_effects['PicoH efecto']['Estado']
            except KeyError:
                otherActive = False
            
            if otherActive == True:
                msg = await ctx.send(f'Ya tienes un **Pico de Hierro {emote_ironp}  activado**')
                await asyncio.sleep(3)
                await msg.delete()
                return
                
            else:
                if active == False or exist == False:
                    
                    active_diamondp = True
                    inventory.update_one({'_id': str(user.id)}, {'$inc':{f'Inventario.Pico de Diamante {emote_diamondp}': -1}})
                    user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']

                    if user_inventory[f'Pico de Diamante {emote_diamondp}'] <= 0:
                        inventory.update_one({'_id': str(user.id)}, {'$unset': {f'Inventario.Pico de Diamante {emote_diamondp}':0}})
                    
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.PicoD efecto.Estado': active_diamondp}})
                    inventory.update_one({'_id': str(user.id)},{'$set': {'Efectos.PicoD efecto.Usos restantes': 3}})
                
                    await ctx.send(f'**{user.display_name}** has usado un **Pico de Diamante** {emote_diamondp}')
                
                else:

                    msg = await ctx.send(f'**No puedes** usar más de un **Pico de Diamante** {emote_diamondp}')
                    await asyncio.sleep(4)
                    await msg.delete()
        else:
            await ctx.send('puto')




    @bot.command(name = 'robar')
    @commands.cooldown(1, 43200, BucketType.user)
    async def roba(ctx, *, prey: discord.Member):
        user = ctx.author
        await open_account(ctx.author)
        now = datetime.now()

        try:
            prey.nick
        except Exception as err:
            exception_type = type(err).__name__
            print(f'ha ocurrido un error de tipo: {exception_type} /comando robar')
            await ctx.send('El **@usuario** escrito **no** es válido')
            roba.reset_cooldown(ctx)
            return
        

        if prey == None:
            roba.reset_cooldown(ctx)
            msg = await ctx.send('Usuario **no** válido, usa el **@**')
            await asyncio.sleep(3)
            await msg.delete()
            return False
        
        await open_account(prey)
        prey_inventory = inventory.find_one({"_id": str(prey.id)})['Inventario']
        prey_effects = inventory.find_one({"_id": str(prey.id)})['Efectos']

        try:
            antActive = prey_effects['Seguro efecto']['Estado']
            remaining = prey_effects['Seguro efecto']['Tiempo restante']
            if now >= remaining:
                antActive = False
        except KeyError:
            antActive = False

        #Discord custom emotes
        emote_nek = ' <:nekoin:864645921824047156>'
        emote_poli = '<:blobpolice:875484529324855337>'
        emote_thief ='<:blobthief:874809722203680839>'
         

        if antActive == True:
            embed = discord.Embed(description =f'{emote_poli} **Alto** ahí rufian, esta persona está **protegida**',
            color = discord.Color.red())
            await ctx.send(embed = embed)

        else:
            if prey_inventory["Monedero"] >= 1000:
                user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']
                rob = random.randrange(1, 101)

                try:
                    daActive = user_effects['Daga efecto']['Estado']
                    usage = user_effects['Daga efecto']['Usos restantes']
                    if usage <= 1:
                        inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos.Daga efecto.Estado': False}})
                except KeyError:
                    daActive = False

                if daActive == True:
                    inventory.update_one({'_id': str(user.id)},{'$inc':{'Efectos.Daga efecto.Usos restantes': -1}})
                    rob += (100 * 8) / 100
                    rob = int(rob)

                if rob < 60:
                    if daActive == True:
                        embed = discord.Embed(description = f'🗡️ **{user.display_name}** no has podido robar **nada** de **{prey.display_name}**', color = discord.Color.red())
                        await ctx.send(embed = embed)
                    else:
                        embed = discord.Embed(description = f'**{user.display_name}** no has podido robar **nada** de **{prey.display_name}**', color = discord.Color.red())
                        await ctx.send(embed = embed)

                else:
            
                    percent = (prey_inventory["Monedero"] * 60)/100
                    percent += 10
                    rob = random.randrange(5, int(percent))

                    if prey_inventory["Monedero"] < rob:
                        rob = prey_inventory["Monedero"]
                    
                    if prey_inventory["Monedero"] <= 0:
                        pass

                    else:
                        #Dinero del robado
                        inventory.update_one({"_id":str(prey.id)},{"$inc": {"Inventario.Monedero": -rob}})

                        #Dinero del ladrón
                        inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": rob}})
                    
                    user_inventory = inventory.find_one({"_id": str(user.id)})["Inventario"]

                    if daActive == True:
                        embed = discord.Embed(description = f'🗡️ **{user.display_name}** has robado **{rob} nekoins** {emote_nek} de **{prey.display_name}** {emote_thief}', color = discord.Color.green())
                        embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
                    else:
                        embed = discord.Embed(description = f'**{user.display_name}** has robado **{rob} nekoins** {emote_nek} de **{prey.display_name}** {emote_thief}', color = discord.Color.green())
                        embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')

                    await ctx.send(embed = embed)
            
            else:
                user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']
                rob = random.randrange(1, 101)

                try:
                    daActive = user_effects['Daga efecto']['Estado']
                    usage = user_effects['Daga efecto']['Usos restantes']
                    if usage <= 1:
                        inventory.update_one({'_id': str(user.id)},{'$set':{'Efectos.Daga efecto.Estado': False}})
                except KeyError:
                    daActive = False

                if daActive == True:
                    inventory.update_one({'_id': str(user.id)},{'$inc':{'Efectos.Daga efecto.Usos restantes': -1}})
                    rob += (100 * 8) / 100
                    rob = int(rob)

                if rob < 75:

                    if daActive == True:
                        embed = discord.Embed(description = f'🗡️ **{user.display_name}** no has podido robar **nada** de **{prey.display_name}**', color = discord.Color.red())
                        await ctx.send(embed = embed)
                    else:
                        embed = discord.Embed(description = f'**{user.display_name}** no has podido robar **nada** de **{prey.display_name}**', color = discord.Color.red())
                        await ctx.send(embed = embed)
                else:
                    
                    percent = (prey_inventory["Monedero"] * 50)/100
                    percent += 10
                    rob = random.randrange(5, int(percent))
                    

                    if prey_inventory["Monedero"] < rob:
                        rob = prey_inventory["Monedero"]
                    
                    if prey_inventory["Monedero"] <= 0:
                       pass

                    else:
                        #Dinero del robado
                        inventory.update_one({"_id":str(prey.id)},{"$inc": {"Inventario.Monedero": -rob}})
                        
                        #Dinero del ladrón
                        inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": rob}})

                    user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']

                    if daActive == True:

                        embed = discord.Embed(description = f'🗡️ {user.display_name} has robado **{rob} nekoins** {emote_nek} de **{prey.display_name}** {emote_thief}', color = discord.Color.green())
                        embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
                    else:
                        embed = discord.Embed(description = f'{user.display_name} has robado **{rob} nekoins** {emote_nek} de **{prey.display_name}** {emote_thief}', color = discord.Color.green())
                        embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')

                    await ctx.send(embed = embed)


    #El ususario gana un numero aleatorio de nekoins
    @bot.command(name = 'minar')
    @commands.cooldown(1, 1800, BucketType.user)
    async def getMoney(ctx):
        
        user = ctx.author
        await open_account(ctx.author)
        maxCoins = 250
        minCoins = 50
        
        user_effects = inventory.find_one({"_id": str(user.id)})['Efectos']
        

      
        #Discord custom emotes
        emote_ironp = '<:picohierro:875941132054442005>'
        emote_diamondp = '<:picodiamante:875941154263289886>'
        emote_nek = ' <:nekoin:864645921824047156>'

        try:
            iActive = user_effects['PicoH efecto']['Estado']
            usage = user_effects['PicoH efecto']['Usos restantes']
            if usage <= 1:
                inventory.update_one({"_id": str(user.id)}, {"$set":{"Efectos.PicoH efecto.Estado": False}})
        except KeyError:
            iActive = False
           
        if iActive == True:
            inventory.update_one({'_id': str(user.id)}, {'$inc':{'Efectos.PicoH efecto.Usos restantes':-1}})
            maxCoins += 75  #+30%
            minCoins += 15

        else:
            try:
                dActive = user_effects['PicoD efecto']['Estado']
                usage = user_effects['PicoD efecto']['Usos restantes']
                if usage <= 1:
                    inventory.update_one({"_id": str(user.id)},{"$set":{"Efectos.PicoD efecto.Estado": False}})
            except KeyError:
                dActive = False

            if dActive == True:
                inventory.update_one({'_id': str(user.id)},{'$inc':{'Efectos.PicoD efecto.Usos restantes':-1}})
                maxCoins += 250  #+100% 
                minCoins += 50
                
        
        earnings = random.randrange(minCoins, maxCoins)
        inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": earnings}})
        user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
        
        if iActive == True:
            embed = discord.Embed(description = f'{emote_ironp} **{user.display_name}** has minado **{earnings} nekoins!!** {emote_nek}', color = discord.Color.green())
        elif dActive == True:
            embed = discord.Embed(description = f'{emote_diamondp} **{user.display_name}** has minado **{earnings} nekoins!!** {emote_nek}', color = discord.Color.green())
        else:
            embed = discord.Embed(description = f'**{user.display_name}** has minado **{earnings} nekoins!!** {emote_nek}', color = discord.Color.green())
        embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
        await ctx.send(embed = embed)
       


#--------------------EL PACHINKO--------------------------------------

    @bot.command(pass_context = True, aliases = ['pachinko', 'pachi'])
    @commands.cooldown(1, 120, BucketType.user)
    async def slots (ctx, *, bet = None):
        user =ctx.author                #RECUERDA QUE BET ES UN STRING!
        pa_number = random.randrange(1,100001)

        if bet == None:
            bet = 10
        
        user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
    
        
        if user_inventory['Monedero']  >= int(bet):

            inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": -int(bet)}})
            
            
            if pa_number <= 60000:
                embed = discord.Embed(title = 'ㅤㅤㅤㅤㅤ**SLOTS**', color = discord.Color.gold())
                embed.set_image(url ='choose any image')
                embed.set_footer(text = '{} le has dado a la palanca'.format(user.display_name), icon_url = user.avatar_url)
                await ctx.send(file = file2, embed = embed)
                await asyncio.sleep(3)

                embed2 = (discord.Embed(description = f'**{user.display_name}** has gastado **{bet} nekoins** y no has ganado **nada**',
                        color = discord.Color.red() ))
                await ctx.send(embed = embed2)
            
            elif pa_number > 60000 and pa_number <= 89000:
                won = int(bet) * 1.35
                won = int(won)
                embed = discord.Embed(title = 'ㅤㅤㅤㅤㅤ**SLOTS**', color = discord.Color.gold())
                embed.set_image(url = 'choose any image')
                embed.set_footer(text = '{} le has dado a la palanca'.format(user.display_name), icon_url = user.avatar_url)
                await ctx.send(file = file1, embed = embed)
                await asyncio.sleep(3)

                inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": won}})  
                user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
                embed2 = (discord.Embed(description = f'**{user.display_name}** has gastado **{bet} nekoins** y has ganado **{won}**',
                        color = discord.Color.dark_green()))
                embed2.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
                await ctx.send(embed = embed2)
            
            elif pa_number > 89000 and pa_number <= 99999:
                won = int(bet) * 3.25
                won = int(won)
                embed = discord.Embed(title = 'ㅤㅤㅤㅤㅤ**SLOTS**', color = discord.Color.gold())
                embed.set_image(url = 'choose any image')
                embed.set_footer(text = '{} le has dado a la palanca'.format(user.display_name), icon_url = user.avatar_url)
                await ctx.send(file = file1, embed = embed)
                await asyncio.sleep(3)

                inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": won}})  
                user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
                embed2 = (discord.Embed(description = f'**{user.display_name}** has gastado **{bet} nekoins** y has ganado **{won}**!!',
                        color = discord.Color.dark_green()))
                embed2.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
                await ctx.send(embed = embed2)

                

            elif pa_number == 100000:
                won = int(bet) * 10
                won = int(won)
                embed = discord.Embed(title = 'ㅤㅤㅤㅤㅤ**SLOTS**', color = discord.Color.gold())
                embed.set_image(url = 'choose any image')
                embed.set_footer(text ='{} le has dado a la palanca'.format(user.display_name), icon_url = user.avatar_url)
                await ctx.send(file = file1, embed = embed)
                await asyncio.sleep(3)

                inventory.update_one({"_id":str(user.id)},{"$inc": {"Inventario.Monedero": won}})  
                user_inventory = inventory.find_one({"_id": str(user.id)})['Inventario']
                embed2 = (discord.Embed(description =f'**{user.display_name}** has gastado **{bet} nekoins** y has ganado **{won}**, mucho más de lo normal!!!',
                        color = discord.Color.green()))
                embed2.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
                await ctx.send(embed = embed2)
        
            
        else :
            embed = discord.Embed(description = f"***No tienes*** ese dinero para apostar ***{user.display_name}!***", color = discord.Color.red())
            embed.set_footer(text = f'Monedero: {user_inventory["Monedero"]} nekoins')
            await ctx.send(embed = embed)
            slots.reset_cooldown(ctx)


    bot.run(TOKEN)
