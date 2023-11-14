import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re

class Event(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        regex = r'https:\/\/(x\.com|twitter\.com)(\/.*)?'
        if msg.author.bot or not re.search(regex, msg.content): return
        
        await msg.delete()
        content = msg.content
        while True:
            match = re.search(regex, content)
            if match:
                group = match.group(1)
                if group == 'x.com': content = content.replace('x.com', 'fixupx.com')
                elif group == 'twitter.com': content = content.replace('twitter.com', 'fxtwitter.com')
            else:
                break

        if type(msg.channel) == discord.Thread: channel = msg.channel.parent
        else: channel = msg.channel
        
        webhooks = await channel.webhooks()

        webhook = None        
        for wh in webhooks:
            if wh.name == 'AutoFx': webhook = wh
            
        if not webhook:
            webhook = await channel.create_webhook(name='AutoFx')
        
        if msg.reference:
            refmsg = await channel.fetch_message(msg.reference.message_id)
            view = discord.ui.View().add_item(discord.ui.Button(label=f'In reply to {refmsg.author.display_name}', style=discord.ButtonStyle.link, url=refmsg.jump_url))
            await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.display_avatar.url, view=view)
        elif type(msg.channel) == discord.Thread:
            await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.display_avatar.url, thread=msg.channel)
        else:
            await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.display_avatar.url)

        
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        await thread.join()
            

async def setup(bot):
	await bot.add_cog(Event(bot))