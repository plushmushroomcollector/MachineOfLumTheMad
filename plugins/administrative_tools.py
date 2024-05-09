import discord
import discord.ext.commands as commands
import datetime

import functools as ft

def is_admin(func):
        @ft.wraps(func)
        async def decorated(self, ctx, *args, **kwargs):
            if ctx.message.author.id in self.bot.config['ADMIN_LIST']:
                return await func(self, ctx, *args, **kwargs)
            else:
                await ctx.send(f'{ctx.author.mention} you are not an admin')

        return decorated

class administrative_tools(commands.Cog, name='Admin Tools'):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def __unload(self, bot):
        print('administrative functions have been removed')

    @property
    def help():
        #TODO: finish the help information
        return ''
    
    def make_datetime_readable_full(self, my_datetime : datetime.datetime):
        formated_date = datetime.datetime.strptime(my_datetime.strftime("%m/%d/%Y, %H:%M:%S"),"%m/%d/%Y, %H:%M:%S")
        return '<t:' + str(datetime.datetime.timestamp(formated_date))[:-2] + ':F>'
    
    def make_datetime_readable_relative(self, my_datetime : datetime.datetime):
        formated_date = datetime.datetime.strptime(my_datetime.strftime("%m/%d/%Y, %H:%M:%S"),"%m/%d/%Y, %H:%M:%S")
        return '<t:' + str(datetime.datetime.timestamp(formated_date))[:-2] + ':R>'

    @commands.command(name='timeout')
    @is_admin
    async def timeout_user(self, ctx, member : discord.Member, time : int, *reason : str):
        reason_string = ' '.join(reason)
        until = datetime.timedelta(minutes=time)
        await ctx.send(f'user [{member.mention}] has been timed out for {str(time)} minutes because: {reason_string}')
        await member.timeout(until, reason=reason_string)

    @commands.command(name='untimeout')
    @is_admin
    async def untimeout_user(self, ctx, member : discord.Member, *reason : str):
        reason_string = ' '.join(reason)
        until = datetime.timedelta(seconds=0)
        if member.is_timed_out():
            await member.timeout(until, reason=reason_string)
            await ctx.send(f'user [{member.mention}] has had their timeout lifted because: {reason_string}')
        else:
            await ctx.send(f'{member.name} is not timed out')

    @commands.command(name='ban')
    @is_admin
    async def ban_user(self, ctx, member : discord.Member, *reason : str):
        reason_string = ' '.join(reason)
        await ctx.send(f'user [{member.mention}] has been banned because: {reason_string}')
        member.ban(0, 0, reason_string)

    @commands.command(name='unban')
    @is_admin
    async def unban_user(self, ctx, member : discord.Member, *reason : str):
        reason_string = ' '.join(reason)
        await ctx.send(f'user [{member.mention}] has been unbanned because: {reason_string}')
        await member.unban(reason_string)

    @commands.command(name='kick')
    @is_admin
    async def kick_user(self, ctx, member : discord.Member, *reason : str):
        reason_string = ' '.join(reason)
        await ctx.send(f'user [{member.mention}] has been kicked because: {reason_string}')
        await member.kick(reason_string)

    @commands.command(name='add-role', aliases=['addrole'])
    @is_admin
    async def add_role(self, ctx, member : discord.Member, role : str):
        
        if role in member.guild.fetch_roles:
            await member.add_roles([role])
            await ctx.send(f'role [{role}] added to [{member.mention}]')
        else:
            await ctx.send(f'no such role [{role}] exists')
    
    @commands.command(name='remove-role', aliases=['rmrole'])
    @is_admin
    async def remove_role(self, ctx, member : discord.Member, role : str):
        if role in member.roles:
            await member.remove_roles([role])
            await ctx.send(f'role [{role}] removed from [{member.mention}]')
        else:
            await ctx.send(f'user [{member.mention}] does not have role [{role}]')
    
    @commands.command(name='change-nickname', aliases=['chnick'])
    @is_admin
    async def change_nickname(self, ctx, member : discord.Member, *new_nick : str):
        new_nick_string = ' '.join(new_nick)

        if new_nick_string == member.nick:
            await ctx.send('user already has that nick')
            return 
        
        if new_nick_string == 'RESTORE':
            await member.edit(nick='')
            await ctx.send(f'user has had their nick restored: {member.mention}')
        else:
            await member.edit(nick=new_nick_string)
            await ctx.send(f'user nick name has been updated: {member.mention}')
    
    @commands.command(name='user-info')
    async def user_info(self, ctx, member : discord.Member):
        info_embed = discord.Embed(title=f'User Info For:', description=f'{member.mention}')
        info_embed.add_field(name='username:', value=f'{member.name}', inline=True)

        if member.global_name != member.display_name:
            info_embed.add_field(name='nickname:', value=f'{member.display_name}', inline=True)
        else:
            info_embed.add_field(name='display name:', value=f'{member.global_name}', inline=True)

        role_list = ''
        for role in member.roles:
            role_list += ('∎ ' + str(role) + '\n')

        info_embed.add_field(name='roles:', value=f'{role_list}', inline=True)
        info_embed.add_field(name='server join date', value=f'{self.make_datetime_readable_full(member.joined_at)}', inline=True)
        info_embed.add_field(name='user creation date', value=f'{self.make_datetime_readable_full(member.created_at)}', inline=True)

        if member.is_timed_out:
            if not member.timed_out_until:
                pass
            else:
                info_embed.add_field(name='current timeout:', value=f'{member.mention} is timed out until {self.make_datetime_readable_relative(member.timed_out_until)}', inline=True)

        info_embed.set_thumbnail(url=member.avatar)

        await ctx.send(content=None, embed=info_embed)