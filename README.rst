wcpan.telegram
==============

Telegram Bot API with Tornado.

Implemented Functions
---------------------

- Getting Updates
    - [x] Update
    - [x] getUpdates
    - [x] setWebhook
    - [x] deleteWebhook
    - [x] getWebhookInfo
    - [x] WebhookInfo
- Available Types
    - [x] User
    - [x] Chat
    - [x] Message
    - [x] MessageEntity
    - [x] PhotoSize
    - [x] Audio
    - [x] Document
    - [x] Video
    - [x] Voice
    - [x] VideoNote
    - [x] Contact
    - [x] Location
    - [x] Venue
    - [x] UserProfilePhotos
    - [x] ReplyKeyboardMarkup
    - [x] KeyboardButton
    - [x] ReplyKeyboardRemove
    - [x] InlineKeyboardMarkup
    - [x] InlineKeyboardButton
    - [x] CallbackQuery
    - [x] ForceReply
    - [ ] ChatPhoto
    - [x] ChatMember
    - [x] ResponseParameters
    - [x] InputFile
- Available Methods
    - [x] getMe
    - [x] sendMessage
    - [x] forwardMessage
    - [x] sendPhoto
    - [x] sendAudio
    - [x] sendDocument
    - [x] sendVideo
    - [x] sendVoice
    - [x] sendVoiceNote
    - [x] sendLocation
    - [x] sendVenue
    - [x] sendContact
    - [x] sendChatAction
    - [x] getUserProfilePhotos
    - [x] getFile
    - [x] kickChatMember
    - [x] unbanChatMember
    - [ ] restrictChatMember
    - [ ] promoteChatMember
    - [ ] exportChatInviteLink
    - [ ] setChatPhoto
    - [ ] deleteChatPhoto
    - [ ] setChatTitle
    - [ ] setChatDescription
    - [ ] pinChatMessage
    - [ ] unpinChatMessage
    - [x] leaveChat
    - [x] getChat
    - [x] getChatAdministrators
    - [x] getChatMembersCount
    - [x] getChatMember
    - [x] answerCallbackQuery
- Updating Messages
    - [x] editMessageText
    - [x] editMessageCaption
    - [x] editMessageReplyMarkup
    - [x] deleteMessage
- Stickers
    - [x] Sticker
    - [x] StickerSet
    - [x] MaskPosition
    - [x] sendSticker
    - [x] getStickerSet
    - [x] uploadStickerSet
    - [x] createNewStickerSet
    - [x] addStickerToSet
    - [x] setStickerPositionInSet
    - [x] deleteStickerFromSet
- Inline Mode
    - [x] InlineQuery
    - [x] answerInlineQuery
    - [x] InlineQueryResult
    - [x] InlineQueryResultArticle
    - [x] InlineQueryResultPhoto
    - [x] InlineQueryResultGif
    - [x] InlineQueryResultMpeg4Gif
    - [x] InlineQueryResultVideo
    - [x] InlineQueryResultAudio
    - [x] InlineQueryResultVoice
    - [x] InlineQueryResultDocument
    - [x] InlineQueryResultLocation
    - [x] InlineQueryResultVenue
    - [x] InlineQueryResultContact
    - [x] InlineQueryResultGame
    - [x] InlineQueryResultCachedPhoto
    - [x] InlineQueryResultCachedGif
    - [x] InlineQueryResultCachedMpeg4Gif
    - [x] InlineQueryResultCachedSticker
    - [x] InlineQueryResultCachedDocument
    - [x] InlineQueryResultCachedVideo
    - [x] InlineQueryResultCachedVoice
    - [x] InlineQueryResultCachedAudio
    - [x] InputMessageContent
    - [x] InputTextMessageContent
    - [x] InputLocationMessageContent
    - [x] InputVenueMessageContent
    - [x] InputContactMessageContent
    - [x] ChosenInlineResult
- Payments
    - [ ] sendInvoice
    - [ ] answerShippingQuery
    - [ ] answerPreCheckoutQuery
    - [ ] LabeledPrice
    - [ ] Invoice
    - [ ] ShippingAddress
    - [ ] OrderInfo
    - [ ] ShippingOption
    - [ ] SuccessfulPayment
    - [ ] ShippingQuery
    - [ ] PreCheckoutQuery
- Games
    - [x] sendGame
    - [x] Game
    - [x] Animation
    - [x] CallbackGame
    - [x] setGameScore
    - [x] getGameHighScores
    - [x] GameHighScore

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
