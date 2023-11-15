import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re

class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self, msg):
        regex = r'https://(x\.com|twitter\.com)(/.*)?'
        if msg.author.bot or not re.search(regex, msg.content): return
        
        if type(msg.channel) != discord.Thread or msg.channel.type == discord.ChannelType.stage_voice or msg.channel.parent.type != discord.ChannelType.forum:
            await msg.delete()
            
        def fixup(m):
            r = 'fixupx' if m.group(1) == 'x.com' else 'fxtwitter'
            return f'https://{r}.com{m.group(2)}'
            
        content = re.sub(regex, fixup, msg.content)

        if type(msg.channel) == discord.Thread: channel = msg.channel.parent
        else: channel = msg.channel

        webhooks = await channel.webhooks()

        webhook = None        
        for wh in webhooks:
            if wh.name == 'AutoFx': webhook = wh

        if not webhook:
            webhook = await channel.create_webhook(name='AutoFx')

        view = discord.ui.View()
        if msg.reference:
            refmsg = await channel.fetch_message(msg.reference.message_id)
            view = view.add_item(discord.ui.Button(label=f'In reply to {refmsg.author.display_name}', style=discord.ButtonStyle.link, url=refmsg.jump_url))

        links = re.findall(r'https?://(?:twitter|x)\.com+/[^\s]*', msg.content)[:3]
        for i, link in enumerate(links):
            view = view.add_item(discord.ui.Button(label=f'Original tweet {i+1}', style=discord.ButtonStyle.link, url=link.replace('x.com', 'twitter.com')))
            
        if type(msg.channel) == discord.Thread:
            await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.display_avatar.url, view=view, thread=msg.channel)
        else:
            await webhook.send(content=content, username=msg.author.display_name, avatar_url=msg.author.display_avatar.url, view=view)


    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        await thread.join()


async def setup(bot):
	await bot.add_cog(Event(bot))