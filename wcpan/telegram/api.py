import json
from typing import List, Awaitable, Union

from tornado import httpclient as thc, web as tw, httputil as thu

from . import types, util


_API_TEMPLATE = 'https://api.telegram.org/bot{api_token}/{api_method}'


ReplyMarkup = Union[
    types.InlineKeyboardMarkup,
    types.ReplyKeyboardMarkup,
    types.ReplyKeyboardRemove,
    types.ForceReply,
]


class BotClient(object):

    def __init__(self, api_token: str) -> None:
        self._api_token = api_token
        if not self._api_token:
            raise BotError('invalid API token')

    async def get_updates(self, offset: int = 0, limit: int = 100,
                          timeout: int = 0, allowed_updates: List[str] = None
                          ) -> Awaitable[List[types.Update]]:
        args = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
        }
        data = await self._get('getUpdates', args)
        return [types.Update(u) for u in data]

    async def set_webhook(self, url: str, certificate: types.InputFile = None,
                          max_connections: int = 40,
                          allowed_updates: List[str] = None) -> Awaitable[bool]:
        args = {
            'url': '' if not url else str(url),
            'max_connections': max_connections,
        }
        if certificate is not None:
            args['certificate'] = str(certificate)
        args['allowed_updates'] = ([] if allowed_updates is None
                                   else str(allowed_updates))

        data = await self._get('setWebhook', args)
        return data

    async def delete_webhook(self) -> Awaitable[bool]:
        data = await self._get('deleteWebhook')
        return data

    async def get_webhook_info(self) -> Awaitable[types.WebhookInfo]:
        data = await self._get('getWebhookInfo')
        return types.WebhookInfo(data)

    async def get_me(self) -> Awaitable[types.User]:
        data = await self._get('getMe')
        return types.User(data)

    async def send_message(self, chat_id: Union[int, str], text: str,
                           parse_mode: str = None,
                           disable_web_page_preview: bool = None,
                           disable_notification: bool = None,
                           reply_to_message_id: int = None,
                           reply_markup: ReplyMarkup = None
                           ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'text': text,
        }
        if parse_mode is not None:
            args['parse_mode'] = parse_mode
        if disable_web_page_preview is not None:
            args['disable_web_page_preview'] = disable_web_page_preview
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        data = await self._get('sendMessage', args)
        return types.Message(data)

    async def forward_message(self, chat_id: Union[int, str],
                              from_chat_id: Union[int, str], message_id: int,
                              disable_notification: bool = None,
                              ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
        }
        if disable_notification is not None:
            args['disable_notification'] = disable_notification

        data = await self._get('forwardMessage', args)
        return types.Message(data)

    async def send_photo(self, chat_id: Union[int, str],
                         photo: Union[types.InputFile, str],
                         caption: str = None, disable_notification: bool = None,
                         reply_to_message_id: int = None,
                         reply_markup: ReplyMarkup = None
                         ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'photo': photo,
        }
        if caption is not None:
            args['caption'] = caption
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(photo, str):
            data = await self._get('sendPhoto', args)
        else:
            data = await self._post('sendPhoto', args)

        return types.Message(data)

    async def send_audio(self, chat_id: Union[int, str],
                         audio: Union[types.InputFile, str],
                         caption: str = None, duration: int = None,
                         performer: str = None, title: str = None,
                         disable_notification: bool = None,
                         reply_to_message_id: int = None,
                         reply_markup: ReplyMarkup = None
                         ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'audio': audio,
        }
        if caption is not None:
            args['caption'] = caption
        if duration is not None:
            args['duration'] = duration
        if performer is not None:
            args['performer'] = performer
        if title is not None:
            args['title'] = title
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(audio, str):
            data = await self._get('sendAudio', args)
        else:
            data = await self._post('sendAudio', args)

        return types.Message(data)

    async def send_document(self, chat_id: Union[int, str],
                            document: Union[types.InputFile, str],
                            caption: str = None,
                            disable_notification: bool = None,
                            reply_to_message_id: int = None,
                            reply_markup: ReplyMarkup = None
                            ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'document': document,
        }
        if caption is not None:
            args['caption'] = caption
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(document, str):
            data = await self._get('sendDocument', args)
        else:
            data = await self._post('sendDocument', args)

        return types.Message(data)

    async def send_sticker(self, chat_id: Union[int, str],
                           sticker: Union[types.InputFile, str],
                           disable_notification: bool = None,
                           reply_to_message_id: int = None,
                           reply_markup: ReplyMarkup = None
                           ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'sticker': sticker,
        }
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(sticker, str):
            data = await self._get('sendSticker', args)
        else:
            data = await self._post('sendSticker', args)

        return types.Message(data)

    async def send_video(self, chat_id, video, reply_to_message_id=None,
                         reply_markup=None):
        args = {
            'chat_id': chat_id,
            'video': video,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(video, str):
            data = await self._get('sendVideo', args)
        else:
            data = await self._post('sendVideo', args)

        return types.Message(data)

    async def send_location(self, chat_id, latitude, longitude,
                            reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        data = await self._get('sendLocation', args)
        return types.Message(data)

    async def send_chat_action(self, chat_id, action):
        args = {
            'chat_id': chat_id,
            'action': action,
        }

        # TODO undocumented return type
        data = await self._get('sendChatAction', args)

    async def get_user_profile_photos(self, user_id, offset=0, limit=100):
        args = {
            'user_id': user_id,
            'offset': offset,
            'limit': limit,
        }

        data = await self._get('getUserProfilePhotos', args)
        return types.UserProfilePhotos(data)

    def _get_api_url(self, api_method):
        return _API_TEMPLATE.format(api_token=self._api_token,
                                    api_method=api_method)

    def _parse_response(self, response):
        data = response.body.decode('utf-8')
        data = json.loads(data)
        if not data['ok']:
            raise BotError(data['description'])
        return data['result']

    async def _get(self, api_method, args=None):
        url = self._get_api_url(api_method)
        if args is not None:
            url = thu.url_concat(url, args)

        link = thc.AsyncHTTPClient()
        request = thc.HTTPRequest(url)
        response = await link.fetch(request)

        return self._parse_response(response)

    async def _post(self, api_method, args):
        url = self._get_api_url(api_method)
        content_type, stream = util.generate_multipart_formdata(args.items())

        link = thc.AsyncHTTPClient()
        request = thc.HTTPRequest(url, method='POST', headers={
            'Content-Type': content_type,
        }, body_producer=stream, request_timeout=0.0)
        response = await link.fetch(request)

        return self._parse_response(response)


class _DispatcherMixin(object):

    def __init__(self, *args, **kwargs):
        super(_DispatcherMixin, self).__init__()

    async def on_text(self, message):
        pass

    async def on_audio(self, message):
        pass

    async def on_document(self, message):
        pass

    async def on_photo(self, message):
        pass

    async def on_sticker(self, message):
        pass

    async def on_video(self, message):
        pass

    async def on_contact(self, message):
        pass

    async def on_location(self, message):
        pass

    async def on_new_chat_participant(self, message):
        pass

    async def on_left_chat_participant(self, message):
        pass

    async def on_new_chat_title(self, message):
        pass

    async def on_new_chat_photo(self, message):
        pass

    async def on_delete_chat_photo(self, message):
        pass

    async def on_group_chat_created(self, message):
        pass

    async def _receive_message(self, message):
        if message.text is not None:
            await self.on_text(message)
        elif message.audio is not None:
            await self.on_audio(message)
        elif message.document is not None:
            await self.on_document(message)
        elif message.photo is not None:
            await self.on_photo(message)
        elif message.sticker is not None:
            await self.on_sticker(message)
        elif message.video is not None:
            await self.on_video(message)
        elif message.contact is not None:
            await self.on_contact(message)
        elif message.location is not None:
            await self.on_location(message)
        elif message.new_chat_participant is not None:
            await self.on_new_chat_participant(message)
        elif message.left_chat_participant is not None:
            await self.on_left_chat_participant(message)
        elif message.new_chat_title is not None:
            await self.on_new_chat_title(message)
        elif message.new_chat_photo is not None:
            await self.on_new_chat_photo(message)
        elif message.delete_chat_photo is not None:
            await self.on_delete_chat_photo(message)
        elif message.group_chat_created is not None:
            await self.on_group_chat_created(message)
        elif message.voice is not None:
            pass
        else:
            raise BotError('unknown message type')


class BotAgent(_DispatcherMixin):

    def __init__(self, api_token):
        self._api = BotClient(api_token)

    @property
    def client(self):
        return self._api

    async def get_updates(self, timeout=0):
        offset = 0
        updates = []
        while True:
            us = await self._api.get_updates(offset, timeout=timeout)
            updates.extend(us)
            if not us:
                break
            offset = us[-1].update_id + 1
        return updates

    async def get_me(self):
        return await self._api.get_me()

    async def send_message(self, chat_id, text, disable_web_page_preview=None,
                           reply_to_message_id=None, reply_markup=None):
        return await self._api.send_message(chat_id, text,
                                            disable_web_page_preview,
                                            reply_to_message_id, reply_markup)

    async def forward_message(self, chat_id, from_chat_id, message_id):
        return await self._api.forward_message(chat_id, from_chat_id,
                                               message_id)

    async def send_photo(self, chat_id, photo, caption=None,
                         reply_to_message_id=None, reply_markup=None):
        return await self._api.send_photo(chat_id, photo, caption,
                                          reply_to_message_id, reply_markup)

    async def send_audio(self, chat_id, audio, reply_to_message_id=None,
                         reply_markup=None):
        return await self._api.send_audio(chat_id, audio, reply_to_message_id,
                                          reply_markup)

    async def send_document(self, chat_id, document, reply_to_message_id=None,
                            reply_markup=None):
        return await self._api.send_document(chat_id, document,
                                             reply_to_message_id, reply_markup)

    async def send_sticker(self, chat_id, sticker, reply_to_message_id=None,
                           reply_markup=None):
        return await self._api.send_sticker(chat_id, sticker,
                                            reply_to_message_id, reply_markup)

    async def send_video(self, chat_id, video, reply_to_message_id=None,
                         reply_markup=None):
        return await self._api.send_video(chat_id, video, reply_to_message_id,
                                          reply_markup)

    async def send_location(self, chat_id, latitude, longitude,
                            reply_to_message_id=None, reply_markup=None):
        return await self._api.send_location(chat_id, latitude, longitude,
                                             reply_to_message_id, reply_markup)

    async def send_chat_action(self, chat_id, action):
        return await self._api.send_chat_action(chat_id, action)

    async def get_user_profile_photos(self, user_id):
        offset = 0
        photos = []
        total = 0
        while True:
            ps = await self._api.get_user_profile_photos(user_id, offset)
            total = ps.total_count
            photos.extend(ps.photos)
            if not ps:
                break
            offset = ps[-1][-1].file_id + 1

        return types.UserProfilePhotos({
            'total_count': total,
            'photos': photos,
        })

    async def poll(self, timeout=1):
        # remove previous webhook first
        await self._api.set_webhook()
        # forever
        while True:
            try:
                updates = await self.get_updates(timeout)
                for u in updates:
                    await self._receive_message(u.message)
            except thc.HTTPError as e:
                if e.code != 599:
                    raise

    async def listen(self, hook_url):
        await self._api.set_webhook(url=hook_url)

    async def close(self):
        # remove webhook
        await self._api.set_webhook()


class BotHookHandler(tw.RequestHandler, _DispatcherMixin):

    async def post(self):
        data = self.request.body
        data = data.decode('utf-8')
        data = json.loads(data)
        if 'message' not in data:
            return
        update = types.Update(data)
        await self._receive_message(update.message)


class BotError(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
