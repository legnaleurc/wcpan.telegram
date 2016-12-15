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

    async def get_updates(self, offset: int = None, limit: int = None,
                          timeout: int = None, allowed_updates: List[str] = None
                          ) -> Awaitable[List[types.Update]]:
        args = {}
        if offset is not None:
            args['offset'] = offset
        if limit is not None:
            args['limit'] = limit
        if timeout is not None:
            args['timeout'] = timeout
        if allowed_updates is not None:
            args['allowed_updates'] = allowed_updates

        data = await self._get('getUpdates', args)
        return [types.Update(u) for u in data]

    async def set_webhook(self, url: str, certificate: types.InputFile = None,
                          max_connections: int = None,
                          allowed_updates: List[str] = None) -> Awaitable[bool]:
        args = {
            'url': '' if not url else str(url),
        }
        if certificate is not None:
            args['certificate'] = certificate
        if max_connections is not None:
            args['max_connections'] = max_connections
        if allowed_updates is not None:
            args['allowed_updates'] = allowed_updates

        if isinstance(certificate, types.InputFile):
            data = await self._post('setWebhook', args)
        else:
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
            args['reply_markup'] = reply_markup

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
            args['reply_markup'] = reply_markup

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
            args['reply_markup'] = reply_markup

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
            args['reply_markup'] = reply_markup

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
            args['reply_markup'] = reply_markup

        if isinstance(sticker, str):
            data = await self._get('sendSticker', args)
        else:
            data = await self._post('sendSticker', args)

        return types.Message(data)

    async def send_video(self, chat_id: Union[int, str],
                         video: Union[types.InputFile, str],
                         duration: int = None, width: int = None,
                         height: int = None, caption: str = None,
                         disable_notification: bool = None,
                         reply_to_message_id: int = None,
                         reply_markup: ReplyMarkup = None
                         ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'video': video,
        }
        if duration is not None:
            args['duration'] = duration
        if width is not None:
            args['width'] = width
        if height is not None:
            args['height'] = height
        if caption is not None:
            args['caption'] = caption
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        if isinstance(video, str):
            data = await self._get('sendVideo', args)
        else:
            data = await self._post('sendVideo', args)

        return types.Message(data)

    async def send_voice(self, chat_id: Union[int, str],
                         voice: Union[types.InputFile, str],
                         caption: str = None, duration: int = None,
                         disable_notification: bool = None,
                         reply_to_message_id: int = None,
                         reply_markup: ReplyMarkup = None
                         ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'voice': voice,
        }
        if caption is not None:
            args['caption'] = caption
        if duration is not None:
            args['duration'] = duration
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        if isinstance(audio, str):
            data = await self._get('sendVoice', args)
        else:
            data = await self._post('sendVoice', args)

        return types.Message(data)

    async def send_location(self, chat_id: Union[int, str], latitude: float,
                            longitude: float, disable_notification: bool = None,
                            reply_to_message_id: int = None,
                            reply_markup: ReplyMarkup = None
                            ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
        }
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('sendLocation', args)
        return types.Message(data)

    async def send_venue(self, chat_id: Union[int, str], latitude: float,
                         longitude: float, title: str, address: str,
                         foursquare_id: str = None,
                         disable_notification: bool = None,
                         reply_to_message_id: int = None,
                         reply_markup: ReplyMarkup = None
                         ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
        }
        if foursquare_id is not None:
            args['foursquare_id'] = foursquare_id
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('sendVenue', args)
        return types.Message(data)

    async def send_contact(self, chat_id: Union[int, str], phone_number: str,
                           first_name: str, last_name: str = None,
                           disable_notification: bool = None,
                           reply_to_message_id: int = None,
                           reply_markup: ReplyMarkup = None
                           ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'phone_number': phone_number,
            'first_name': first_name,
        }
        if last_name is not None:
            args['last_name'] = last_name
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('sendContact', args)
        return types.Message(data)

    async def send_chat_action(self, chat_id: Union[int, str],
                               action: str) -> Awaitable[bool]:
        args = {
            'chat_id': chat_id,
            'action': action,
        }

        data = await self._get('sendChatAction', args)
        return data

    async def get_user_profile_photos(self, user_id: int, offset: int = None,
                                      limit: int = None
                                      ) -> Awaitable[types.UserProfilePhotos]:
        args = {
            'user_id': user_id,
        }
        if offset is not None:
            args['offset'] = offset
        if limit is not None:
            args['limit'] = limit

        data = await self._get('getUserProfilePhotos', args)
        return types.UserProfilePhotos(data)

    async def get_file(self, file_id: str) -> Awaitable[types.File]:
        args = {
            'file_id': file_id,
        }

        data = await self._get('getFile', args)
        return types.File(data)

    async def kick_chat_member(self, chat_id: Union[int, str],
                               user_id: int) -> Awaitable[bool]:
        args = {
            'chat_id': chat_id,
            'user_id': user_id,
        }

        data = await self._get('kickChatMember', args)
        return data

    async def leave_chat(self, chat_id: Union[int, str]) -> Awaitable[bool]:
        args = {
            'chat_id': chat_id,
        }

        data = await self._get('leaveChat', args)
        return data

    async def unban_chat_member(self, chat_id: Union[int, str],
                                user_id: int) -> Awaitable[bool]:
        args = {
            'chat_id': chat_id,
            'user_id': user_id,
        }

        data = await self._get('unbanChatMember', args)
        return data

    async def get_chat(self, chat_id: Union[int, str]) -> Awaitable[types.Chat]:
        args = {
            'chat_id': chat_id,
        }

        data = await self._get('getChat', args)
        return types.Chat(data)

    async def get_chat_administrators(self, chat_id: Union[int, str]
                                      ) -> Awaitable[List[types.ChatMember]]:
        args = {
            'chat_id': chat_id,
        }

        data = await self._get('getChatAdministrators', args)
        return [types.ChatMember(_) for _ in data]

    async def get_chat_members_count(self, chat_id: Union[int, str]) -> Awaitable[int]:
        args = {
            'chat_id': chat_id,
        }

        data = await self._get('getChatMembersCount', args)
        return data

    async def get_chat_member(self, chat_id: Union[int, str],
                              user_id: int) -> Awaitable[types.ChatMember]:
        args = {
            'chat_id': chat_id,
            'user_id': user_id,
        }

        data = await self._get('getChatMember', args)
        return types.ChatMember(data)

    async def answer_callback_query(self, callback_query_id: str,
                                    text: str = None, show_alert: bool = None,
                                    url: str = None, cache_time: int = None
                                    ) -> Awaitable[bool]:
        args = {
            'callback_query_id': callback_query_id,
        }
        if text is not None:
            args['text'] = text
        if show_alert is not None:
            args['show_alert'] = show_alert
        if url is not None:
            args['url'] = url
        if cache_time is not None:
            args['cache_time'] = cache_time

        data = await self._get('answerCallbackQuery', args)
        return data

    async def edit_message_text(self, text: str,
                                chat_id: Union[int, str] = None,
                                message_id: int = None,
                                inline_message_id: str = None,
                                parse_mode: str = None,
                                disable_web_page_preview: bool = None,
                                reply_markup: types.InlineKeyboardMarkup = None
                                ) -> Awaitable[Union[types.Message, bool]]:
        args = {
            'text': text,
        }
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id
        if parse_mode is not None:
            args['parse_mode'] = parse_mode
        if disable_web_page_preview is not None:
            args['disable_web_page_preview'] = disable_web_page_preview
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('editMessageText', args)
        if isinstance(data, bool):
            return data
        return types.Message(data)

    async def edit_message_caption(self, chat_id: Union[int, str] = None,
                                   message_id: int = None,
                                   inline_message_id: str = None,
                                   caption: str = None,
                                   reply_markup:
                                       types.InlineKeyboardMarkup = None
                                   ) -> Awaitable[Union[types.Message, bool]]:
        args = {}
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id
        if caption is not None:
            args['caption'] = caption
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('editMessageCaption', args)
        if isinstance(data, bool):
            return data
        return types.Message(data)

    async def edit_message_reply_markup(self, chat_id: Union[int, str] = None,
                                        message_id: int = None,
                                        inline_message_id: str = None,
                                        reply_markup:
                                            types.InlineKeyboardMarkup = None
                                        ) -> Awaitable[
                                            Union[types.Message, bool]]:
        args = {}
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('editMessageReplyMarkup', args)
        if isinstance(data, bool):
            return data
        return types.Message(data)

    async def answer_inline_query(self, inline_query_id: str,
                                  results: List[types.InlineQueryResult],
                                  cache_time: int = None,
                                  is_personal: bool = None,
                                  next_offset: str = None,
                                  switch_pm_text: str = None,
                                  switch_pm_parameter: str = None
                                  ) -> Awaitable[bool]:
        args = {
            'inline_query_id': inline_query_id,
            'results': results,
        }
        if cache_time is not None:
            args['cache_time'] = cache_time
        if is_personal is not None:
            args['is_personal'] = is_personal
        if next_offset is not None:
            args['next_offset'] = next_offset
        if switch_pm_text is not None:
            args['switch_pm_text'] = switch_pm_text
        if switch_pm_parameter is not None:
            args['switch_pm_parameter'] = switch_pm_parameter

        data = await self._get('answerInlineQuery', args)
        return data

    async def send_game(self, chat_id: int, game_short_name: str,
                        disable_notification: bool = None,
                        reply_to_message_id: int = None,
                        reply_markup: types.InlineKeyboardMarkup = None,
                        ) -> Awaitable[types.Message]:
        args = {
            'chat_id': chat_id,
            'game_short_name': game_short_name,
        }
        if disable_notification is not None:
            args['disable_notification'] = disable_notification
        if reply_to_message_id is not None:
            args['reply_to_message_id'] = reply_to_message_id
        if reply_markup is not None:
            args['reply_markup'] = reply_markup

        data = await self._get('sendGame', args)
        return types.Message(data)

    async def set_game_score(self, user_id: int, score: int, force: bool = None,
                             disable_edit_message: bool = None,
                             chat_id: int = None, message_id: int = None,
                             inline_message_id: str = None
                             ) -> Awaitable[Union[types.Message, bool]]:
        args = {
            'user_id': user_id,
            'score': score,
        }
        if force is not None:
            args['force'] = force
        if disable_edit_message is not None:
            args['disable_edit_message'] = disable_edit_message
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id

        data = await self._get('setGameScore', args)
        if isinstance(data, bool):
            return data
        return types.Message(data)

    async def get_game_high_scores(self, user_id: int, chat_id: int = None,
                             message_id: int = None,
                             inline_message_id: str = None
                             ) -> Awaitable[List[types.GameHighScore]]:
        args = {
            'user_id': user_id,
        }
        if chat_id is not None:
            args['chat_id'] = chat_id
        if message_id is not None:
            args['message_id'] = message_id
        if inline_message_id is not None:
            args['inline_message_id'] = inline_message_id

        data = await self._get('getGameHighScores', args)
        return [types.GameHighScore(_) for _ in data]

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
            args = util.normalize_args(args)
            url = thu.url_concat(url, args)

        link = thc.AsyncHTTPClient()
        request = thc.HTTPRequest(url)
        response = await link.fetch(request)

        return self._parse_response(response)

    async def _post(self, api_method, args):
        url = self._get_api_url(api_method)
        args = util.normalize_args(args)
        content_type, stream = util.generate_multipart_formdata(args.items())

        link = thc.AsyncHTTPClient()
        request = thc.HTTPRequest(url, method='POST', headers={
            'Content-Type': content_type,
        }, body_producer=stream, request_timeout=0.0)
        response = await link.fetch(request)

        return self._parse_response(response)


class _DispatcherMixin(object):

    def __init__(self, *args, **kwargs) -> None:
        super(_DispatcherMixin, self).__init__()

    async def on_text(self, message: types.Message) -> None:
        pass

    async def on_audio(self, message: types.Message) -> None:
        pass

    async def on_document(self, message: types.Message) -> None:
        pass

    async def on_game(self, message: types.Message) -> None:
        pass

    async def on_photo(self, message: types.Message) -> None:
        pass

    async def on_sticker(self, message: types.Message) -> None:
        pass

    async def on_video(self, message: types.Message) -> None:
        pass

    async def on_voice(self, message: types.Message) -> None:
        pass

    async def on_caption(self, message: types.Message) -> None:
        pass

    async def on_contact(self, message: types.Message) -> None:
        pass

    async def on_location(self, message: types.Message) -> None:
        pass

    async def on_venue(self, message: types.Message) -> None:
        pass

    async def on_new_chat_member(self, message: types.Message) -> None:
        pass

    async def on_left_chat_member(self, message: types.Message) -> None:
        pass

    async def on_new_chat_title(self, message: types.Message) -> None:
        pass

    async def on_new_chat_photo(self, message: types.Message) -> None:
        pass

    async def on_delete_chat_photo(self, message: types.Message) -> None:
        pass

    async def on_group_chat_created(self, message: types.Message) -> None:
        pass

    async def on_supergroup_chat_created(self, message: types.Message) -> None:
        pass

    async def on_channel_chat_created(self, message: types.Message) -> None:
        pass

    async def on_pinned_message(self, message: types.Message) -> None:
        pass

    async def _receive_message(self, message: types.Message) -> None:
        if message.text is not None:
            await self.on_text(message)
        elif message.audio is not None:
            await self.on_audio(message)
        elif message.document is not None:
            await self.on_document(message)
        elif message.game is not None:
            await self.on_game(message)
        elif message.photo is not None:
            await self.on_photo(message)
        elif message.sticker is not None:
            await self.on_sticker(message)
        elif message.video is not None:
            await self.on_video(message)
        elif message.voice is not None:
            await self.on_voice(message)
        elif message.caption is not None:
            await self.on_caption(message)
        elif message.contact is not None:
            await self.on_contact(message)
        elif message.location is not None:
            await self.on_location(message)
        elif message.venue is not None:
            await self.on_venue(message)
        elif message.new_chat_member is not None:
            await self.on_new_chat_member(message)
        elif message.left_chat_member is not None:
            await self.on_left_chat_member(message)
        elif message.new_chat_title is not None:
            await self.on_new_chat_title(message)
        elif message.new_chat_photo is not None:
            await self.on_new_chat_photo(message)
        elif message.delete_chat_photo is not None:
            await self.on_delete_chat_photo(message)
        elif message.group_chat_created is not None:
            await self.on_group_chat_created(message)
        elif message.supergroup_chat_created is not None:
            await self.on_supergroup_chat_created(message)
        elif message.channel_chat_created is not None:
            await self.on_channel_chat_created(message)
        elif message.pinned_message is not None:
            await self.on_pinned_message(message)
        else:
            raise BotError('unknown message type')


class BotAgent(_DispatcherMixin):

    def __init__(self, api_token: str) -> None:
        self._api = BotClient(api_token)

    @property
    def client(self) -> BotClient:
        return self._api

    async def get_updates(self,
                          timeout: int = 0) -> Awaitable[List[types.Update]]:
        offset = 0
        updates = []
        while True:
            us = await self._api.get_updates(offset, timeout=timeout)
            updates.extend(us)
            if not us:
                break
            offset = us[-1].update_id + 1
        return updates

    async def get_user_profile_photos(self, user_id: int
                                      ) -> Awaitable[types.UserProfilePhotos]:
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

    async def poll(self, timeout: int) -> Awaitable[None]:
        # remove previous webhook first
        ok = False
        while not ok:
            ok = await self._api.delete_webhook()
        # forever
        while True:
            try:
                updates = await self.get_updates(timeout)
                for u in updates:
                    await self._receive_message(u.message)
            except thc.HTTPError as e:
                if e.code != 599:
                    raise

    async def listen(self, hook_url: str) -> Awaitable[None]:
        await self._api.set_webhook(url=hook_url)

    async def close(self):
        await self._api.delete_webhook()


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
