import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re
import asyncio
import aiohttp

class QueueRateLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.queue = asyncio.Queue()
        self.last_check = 0
        self.lock = asyncio.Lock()

    async def add_to_queue(self, coro):
        await self.queue.put(coro)

    async def process_queue(self):
        while True:
            coro = await self.queue.get()
            await self.wait_for_rate_limit()
            try: await coro
            except Exception as e: print(f"Error processing queue item: {e}")
            self.queue.task_done()

    async def wait_for_rate_limit(self):
        async with self.lock:
            current_time = asyncio.get_event_loop().time()
            if current_time - self.last_check < 1 / self.rate_limit:
                wait_time = 1 / self.rate_limit - (current_time - self.last_check)
                await asyncio.sleep(wait_time)
                self.rate_limit = max(1, self.rate_limit * 0.9)  # Gradually reduce rate limit
            else:
                self.rate_limit = min(5, self.rate_limit * 1.1)  # Gradually increase rate limit
            self.last_check = asyncio.get_event_loop().time()

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rate_limiter = QueueRateLimiter(3)
        self.bot.loop.create_task(self.rate_limiter.process_queue())

    @commands.Cog.listener()
    async def on_message(self, msg):
        regex = r'https://(x\.com|twitter\.com)(/.*)?'
        if msg.author.bot or not re.search(regex, msg.content): return
        
        if type(msg.channel) != discord.Thread or msg.channel.type == discord.ChannelType.stage_voice or msg.channel.parent.type != discord.ChannelType.forum:
            await self.rate_limiter.add_to_queue(msg.delete())
        
        await self.rate_limiter.add_to_queue(self.process_message(msg))
        
    async def process_message(self, msg):
        content = re.sub(r'https://(x\.com|twitter\.com)(/.*)?', self.fixup, msg.content)
        channel = msg.channel.parent if isinstance(msg.channel, discord.Thread) else msg.channel

        webhook = await self.get_or_create_webhook(channel)
        view = await self.create_view(msg, channel)

        await self.send_webhook_message(webhook, msg, content, view)
        
    async def get_or_create_webhook(self, channel):
        webhooks = await channel.webhooks()
        webhook = discord.utils.get(webhooks, name='AutoFx')
        if not webhook:
            webhook = await channel.create_webhook(name='AutoFx')
        return webhook
    
    async def create_view(self, msg, channel):
        view = discord.ui.View()
        if msg.reference:
            refmsg = await channel.fetch_message(msg.reference.message_id)
            view.add_item(discord.ui.Button(label=f'In reply to {refmsg.author.display_name}', style=discord.ButtonStyle.link, url=refmsg.jump_url))

        links = re.findall(r'https?://(?:twitter|x)\.com+/[^\s]*', msg.content)[:3]
        for i, link in enumerate(links):
            view.add_item(discord.ui.Button(label=f'Original tweet {i+1}', style=discord.ButtonStyle.link, url=link.replace('x.com', 'twitter.com')))
        
        return view
    
    async def send_webhook_message(self, webhook, msg, content, view):
        kwargs = {
            'content': content,
            'username': msg.author.display_name,
            'avatar_url': msg.author.display_avatar.url,
            'view': view
        }
        if isinstance(msg.channel, discord.Thread):
            kwargs['thread'] = msg.channel

        await webhook.send(**kwargs)
        
    def fixup(self, match):
        domain = match.group(1)
        path = match.group(2) or ''
        return f'https://{"fixupx" if domain == "x.com" else "fxtwitter"}.com{path}'


async def setup(bot):
	await bot.add_cog(Event(bot))