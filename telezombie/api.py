import urllib.parse as up
import json

from tornado import gen, httpclient
import yaml

from . import settings, types, util


_API_TEMPLATE = 'https://api.telegram.org/bot{api_token}/{api_method}'


class TeleZombie(object):

    def __init__(self, api_token=None):
        if not api_token:
            api_token = self._get_api_token(settings.DEFAULT_TOKEN_PATH)

        self._api_token = api_token

    @gen.coroutine
    def get_updates(self, offset=0, limit=100, timeout=0):
        args = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout,
        }
        data = yield self._get('getUpdates', args)
        return [types.Update(u) for u in data]

    @gen.coroutine
    def set_webhook(self, url=None):
        if url is None:
            args = None
        else:
            args = {
                'url': url
            }

        # TODO undocumented return type
        data = yield self._get('setWebhook', args)
        return None

    @gen.coroutine
    def get_me(self):
        data = yield self._get('getMe')
        return types.User(data)

    @gen.coroutine
    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
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

        data = yield self._get('sendMessage', args)
        return types.Message(data)

    @gen.coroutine
    def forward_message(self, chat_id, from_chat_id, message_id):
        args = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id,
        }

        data = yield self._get('forwardMessage', args)
        return types.Message(data)

    @gen.coroutine
    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
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
            data = yield self._get('sendPhoto', args)
        else:
            data = yield self._post('sendPhoto', args)

        return types.Message(data)

    @gen.coroutine
    def send_audio(self, chat_id, audio, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'audio': audio,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(audio, str):
            data = yield self._get('sendAudio', args)
        else:
            data = yield self._post('sendAudio', args)

        return types.Message(data)

    @gen.coroutine
    def send_document(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'document': document,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(document, str):
            data = yield self._get('sendDocument', args)
        else:
            data = yield self._post('sendDocument', args)

        return types.Message(data)

    @gen.coroutine
    def send_sticker(self, chat_id, sticker, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'sticker': sticker,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(sticker, str):
            data = yield self._get('sendSticker', args)
        else:
            data = yield self._post('sendSticker', args)

        return types.Message(data)

    @gen.coroutine
    def send_video(self, chat_id, video, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'video': video,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        if isinstance(video, str):
            data = yield self._get('sendVideo', args)
        else:
            data = yield self._post('sendVideo', args)

        return types.Message(data)

    @gen.coroutine
    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        args = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
        }
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = str(reply_markup)

        data = yield self._get('sendLocation', args)
        return types.Message(data)

    @gen.coroutine
    def send_chat_action(self, chat_id, action):
        args = {
            'chat_id': chat_id,
            'action': action,
        }

        # TODO undocumented return type
        data = yield self._get('sendChatAction', args)
        return None

    @gen.coroutine
    def get_user_profile_photos(self, user_id, offset=0, limit=100):
        args = {
            'user_id': user_id,
            'offset': offset,
            'limit': limit,
        }

        data = yield self._get('getUserProfilePhotos', args)
        return types.UserProfilePhotos(data)

    def _get_api_token(self, path):
        with open(path, 'r') as fin:
            data = yaml.safe_load(fin)
            return data['api_token']

    def _get_api_url(self, api_method):
        return _API_TEMPLATE.format(api_token=self._api_token, api_method=api_method)

    def _parse_response(self, response):
        if response.code != 200:
            return None
        data = response.body.decode('utf-8')
        data = json.loads(data)
        if not data['ok']:
            print(data['description'])
            return None
        return data['result']

    @gen.coroutine
    def _get(self, api_method, args=None):
        url = self._get_api_url(api_method)
        if args is not None:
            query = up.urlencode(args)
            url += '?' + query

        link = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url)
        response = yield link.fetch(request, raise_error=False)

        return self._parse_response(response)

    @gen.coroutine
    def _post(self, api_method, args):
        url = self._get_api_url(api_method)
        content_type, stream = util.generate_multipart_formdata(args.items())

        link = httpclient.AsyncHTTPClient()
        request = httpclient.HTTPRequest(url, method='POST', headers={
            'Content-Type': content_type,
        }, body_producer=stream, request_timeout=0.0)
        response = yield link.fetch(request, raise_error=False)

        return self._parse_response(response)


class TeleLich(object):

    def __init__(self, api_token=None):
        self._api = TeleZombie(api_token)

    @property
    def zombie(self):
        return self._api

    @gen.coroutine
    def get_updates(self, timeout=0):
        offset = 0
        updates = []
        while True:
            us = yield self._api.get_updates(offset, timeout=timeout)
            updates.extend(us)
            if not us:
                break
            offset = us[-1].update_id + 1
        return updates

    @gen.coroutine
    def get_me(self):
        return (yield self._api.get_me())

    @gen.coroutine
    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_message(chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup))

    @gen.coroutine
    def forward_message(self, chat_id, from_chat_id, message_id):
        return (yield self._api.forward_message(chat_id, from_chat_id, message_id))

    @gen.coroutine
    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_photo(chat_id, photo, caption, reply_to_message_id, reply_markup))

    @gen.coroutine
    def send_audio(self, chat_id, audio, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_audio(chat_id, audio, reply_to_message_id, reply_markup))

    @gen.coroutine
    def send_document(self, chat_id, document, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_document(chat_id, document, reply_to_message_id, reply_markup))

    @gen.coroutine
    def send_sticker(self, chat_id, sticker, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_sticker(chat_id, sticker, reply_to_message_id, reply_markup))

    @gen.coroutine
    def send_video(self, chat_id, video, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_video(chat_id, video, reply_to_message_id, reply_markup))

    @gen.coroutine
    def send_location(self, chat_id, latitude, longitude, reply_to_message_id=None, reply_markup=None):
        return (yield self._api.send_location(chat_id, latitude, longitude, reply_to_message_id, reply_markup))

    @gen.coroutine
    def send_chat_action(self, chat_id, action):
        return (yield self._api.send_chat_action(chat_id, action))

    @gen.coroutine
    def get_user_profile_photos(self, user_id):
        offset = 0
        photos = []
        total = 0
        while True:
            ps = yield self._api.get_user_profile_photos(user_id, offset)
            total = ps.total_count
            photos.extend(ps.photos)
            if not ps:
                break
            offset = ps[-1][-1].file_id + 1

        return types.UserProfilePhotos({
            'total_count': total,
            'photos': photos,
        })

    @gen.coroutine
    def poll(self, timeout=3):
        # remove previous webhook first
        yield self._api.set_webhook()
        # forever
        while True:
            updates = yield self.get_updates(timeout)
            for u in updates:
                self._receive_message(u.message)

    @gen.coroutine
    def listen(self, hook_url):
        yield self._api.set_webhook(url=hook_url)

    def on_text(self, message):
        pass

    def on_audio(self, message):
        pass

    def on_document(self, message):
        pass

    def on_photo(self, message):
        pass

    def on_sticker(self, message):
        pass

    def on_video(self, message):
        pass

    def on_contact(self, message):
        pass

    def on_location(self, message):
        pass

    def _receive_message(self, message):
        if message.text is not None:
            self.on_text(message)
        elif message.audio is not None:
            self.on_audio(message)
        elif message.document is not None:
            self.on_document(message)
        elif message.photo is not None:
            self.on_photo(message)
        elif message.sticker is not None:
            self.on_sticker(message)
        elif message.video is not None:
            self.on_video(message)
        elif message.contact is not None:
            self.on_contact(message)
        elif message.location is not None:
            self.on_location(message)
        else:
            print('unknown', message)
