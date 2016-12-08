import json

from tornado import gen, httpclient, web, httputil

from . import settings, types, util


_API_TEMPLATE = 'https://api.telegram.org/bot{api_token}/{api_method}'


class TeleZombie(object):

    def __init__(self, api_token):
        self._api_token = api_token
        if not self._api_token:
            raise TeleError('invalid API token')

    async def get_updates(self, offset=0, limit=100, timeout=0):
        args = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
        }
        data = await self._get('getUpdates', args)
        return [types.Update(u) for u in data]

    async def set_webhook(self, url=None):
        if url is None:
            args = None
        else:
            args = {
                'url': url
            }

        # TODO undocumented return type
        data = await self._get('setWebhook', args)

    async def get_me(self):
        data = await self._get('getMe')
        return types.User(data)

    async def send_message(self, chat_id, text, disable_web_page_preview=None,
                           reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'text': text,
        }
        if disable_web_page_preview is not None:
            args['disable_web_page_preview'] = disable_web_page_preview
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        data = await self._get('sendMessage', args)
        return types.Message(data)

    async def forward_message(self, chat_id, from_chat_id, message_id):
        args = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
        }

        data = await self._get('forwardMessage', args)
        return types.Message(data)

    async def send_photo(self, chat_id, photo, caption=None,
                         reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'photo': photo,
        }
        if caption is not None:
            args['caption'] = caption
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(photo, str):
            data = await self._get('sendPhoto', args)
        else:
            data = await self._post('sendPhoto', args)

        return types.Message(data)

    async def send_audio(self, chat_id, audio, reply_to_message_id=None,
                         reply_markup=None):
        args = {
            'chat_id': chat_id,
            'audio': audio,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(audio, str):
            data = await self._get('sendAudio', args)
        else:
            data = await self._post('sendAudio', args)

        return types.Message(data)

    async def send_document(self, chat_id, document, reply_to_message_id=None,
                            reply_markup=None):
        args = {
            'chat_id': chat_id,
            'document': document,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(document, str):
            data = await self._get('sendDocument', args)
        else:
            data = await self._post('sendDocument', args)

        return types.Message(data)

    async def send_sticker(self, chat_id, sticker, reply_to_message_id=None,
                           reply_markup=None):
        args = {
            'chat_id': chat_id,
            'sticker': sticker,
        }
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
            raise TeleError(data['description'])
        return data['result']

    async def _get(self, api_method, args=None):
        url = self._get_api_url(api_method)
        if args is not None:
            url = httputil.url_concat(url, args)

        link = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url)
        response = await link.fetch(request)

        return self._parse_response(response)

    async def _post(self, api_method, args):
        url = self._get_api_url(api_method)
        content_type, stream = util.generate_multipart_formdata(args.items())

        link = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url, method='POST', headers={
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
            raise TeleError('unknown message type')


class TeleLich(_DispatcherMixin):

    def __init__(self, api_token):
        self._api = TeleZombie(api_token)

    @property
    def zombie(self):
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
            except httpclient.HTTPError as e:
                if e.code != 599:
                    raise

    async def listen(self, hook_url):
        await self._api.set_webhook(url=hook_url)

    async def close(self):
        # remove webhook
        await self._api.set_webhook()


class TeleHookHandler(web.RequestHandler, _DispatcherMixin):

    async def post(self):
        data = self.request.body
        data = data.decode('utf-8')
        data = json.loads(data)
        if 'message' not in data:
            return
        update = types.Update(data)
        await self._receive_message(update.message)


class TeleError(Exception):

    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description
