from conections import bot

import discord
from discord.ext import commands



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):

        seconds = float('%.2f' % error.retry_after)        
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours > 1 and minutes > 1:
            await ctx.send(f'***Espera {hours:.0f} horas y {minutes:.0f} minutos para usar el comando***')
            raise error
        elif hours == 1 and minutes > 1:
            await ctx.send(f'***Espera {hours:.0f} hora y {minutes:.0f} minutos para usar el comando***')
            raise error
        elif minutes == 1 and hours > 1:
            await ctx.send(f'***Espera {hours:.0f} horas y {minutes:.0f} minuto para usar el comando***')
            raise 
        elif hours == 1 and minutes == 1:
            await ctx.send(f'***Espera {hours:.0f} hora y {minutes:.0f} minuto para usar el comando***')
            raise error
        elif minutes == 0 and hours > 1:
            await ctx.send(f'***Espera {hours:.0f} horas para usar el comando***')
            raise error
        elif minutes == 0 and hours == 1:
            await ctx.send(f'***Espera {hours:.0f} hora para usar el comando***')
            raise error
        elif hours == 0 and minutes == 1:
            await ctx.send(f'***Espera {minutes:.0f} minuto y {seconds:.0f} segundos para usar el comando***')
            raise error
        elif hours == 0 and minutes == 0:
            await ctx.send(f'***Espera {seconds:.0f} segundos para usar el comando***')
            raise error
        elif hours == 0 and minutes > 1:
            await ctx.send(f'***Espera {minutes:.0f} minutos y {seconds:.0f} segundos para usar el comando***')
            raise error
