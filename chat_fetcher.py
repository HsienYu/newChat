import asyncio

import aiohttp
from aiohttp import ClientConnectorError
from pytchat import LiveChatAsync


class ChatFetcher:
    def __init__(self, video_id, server_url=None):
        self.video_id = video_id
        self.server_url = server_url

    async def run(self):
        live_chat = LiveChatAsync(self.video_id, callback=self.on_message)
        while live_chat.is_alive():
            await asyncio.sleep(3)

    async def on_message(self, chat_data):
        for c in chat_data.items:
            msg = {
                'datetime': c.datetime,
                'author': c.author.name,
                'message': c.message
            }
            print(f'{self.video_id}::{msg}')
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(self.server_url, json={'void_id': self.video_id, 'msg': msg}):
                        pass
            except ClientConnectorError:
                print(f'ClientConnectorError: Can not connect to {self.server_url}')
            await chat_data.tick_async()
