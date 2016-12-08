wcpan.telegram
==============

Telegram Bot API with Tornado.

High Level API Example
----------------------

``BotAgent`` is a high level undead, you can demand it to send requests:

.. code:: python

    from tornado import gen, ioloop
    from wcpan.telegram import api, types


    async def main():
        API_TOKEN = 'your_token'
        lich = api.BotAgent(API_TOKEN)
        talk_to = 42

        # getMe
        user = await lich.get_me()
        print(user)

        # getUpdates
        updates = await lich.get_updates()
        print(updates)

        # sendMessage
        message = await lich.send_message(talk_to, 'hello')
        print(message)

        # sendPhoto
        photo = types.InputFile('path_to_your_phoho.png')
        message = await lich.send_photo(talk_to, photo)
        print(message)

        # sendAudio
        audio = types.InputFile('path_to_your_audio.ogg')
        message = await lich.send_audio(talk_to, audio)
        print(message)

        # sendVideo
        video = types.InputFile('path_to_your_video.mp4')
        message = await lich.send_video(talk_to, video)
        print(message)

        # sendDocument
        document = types.InputFile('path_to_your_file.zip')
        message = await lich.send_document(talk_to, document)
        print(message)


    main_loop = ioloop.IOLoop.instance()
    main_loop.run_sync(main)

And let it handles updates:

.. code:: python

    from tornado import gen, ioloop
    from wcpan.telegram import api


    class KelThuzad(api.BotAgent):

        def __init__(self, api_token):
            super(KelThuzad, self).__init__(api_token)

        async def on_text(self, message):
            id_ = message.message_id
            chat = message.chat
            text = message.text
            # echo same text
            await self.send_message(chat.id_, text, reply_to_message_id=id_)

        async def on_video(self, message):
            chat = message.chat
            video = message.video
            # echo video without upload again
            await self.send_video(chat.id_, video.file_id, reply_to_message_id=id_)


    async def forever():
        API_TOKEN = 'your_token'
        lich = api.KelThuzad(API_TOKEN)
        await lich.poll()


    main_loop = ioloop.IOLoop.instance()
    main_loop.run_sync(forever)

Or handles updates by webhook:

.. code:: python

    from tornado import gen, ioloop, web
    from wcpan.telegram import api


    class HookHandler(api.BotHookHandler):

        async def on_text(self, message):
            lich = self.application.settings['lich']
            id_ = message.message_id
            chat = message.chat
            text = message.text
            # echo same text
            await lich.send_message(chat.id_, text, reply_to_message_id=id_)


    async def create_lich():
        API_TOKEN = 'your_token'
        lich = api.BotAgent(API_TOKEN)
        await lich.listen('https://your.host/hook')
        return lich


    main_loop = ioloop.IOLoop.instance()

    lich = main_loop.run_sync(create_lich)
    application = web.Application([
        (r"/hook", HookHandler),
    ], lich=lich)
    # please configure your own SSL proxy
    application.listen(8000)

    main_loop.start()

Low Level API Example
---------------------

``BotClient`` is also there, which provides simple and direct API mapping:

.. code:: python

    from tornado import gen, ioloop
    from wcpan.telegram import api, types


    async def main():
        API_TOKEN = 'your_token'
        ghoul = api.BotClient(API_TOKEN)
        talk_to = 42

        # getMe
        user = await ghoul.get_me()
        print(user)

        # getUpdates
        offset = 0
        updates = []
        while True:
            us = await ghoul.get_updates(offset)
            updates.extend(us)
            if not us:
                break
            offset = us[-1].update_id + 1
        print(updates)

        # sendMessage
        message = await ghoul.send_message(talk_to, 'hello')
        print(message)

        # sendDocument
        document = types.InputFile('path_to_your_file.zip')
        message = await lich.send_document(talk_to, document)
        print(message)


    main_loop = ioloop.IOLoop.instance()
    main_loop.run_sync(main)
