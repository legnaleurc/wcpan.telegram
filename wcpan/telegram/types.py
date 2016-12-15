import json
import os.path as op
from typing import Optional


class Update(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def update_id(self) -> int:
        return self._data['update_id']

    @property
    def message(self) -> Optional[Message]:
        return _wrap_data(self._data, 'message', Message)

    @property
    def edited_message(self) -> Optional[Message]:
        return _wrap_data(self._data, 'edited_message', Message)

    @property
    def channel_post(self) -> Optional[Message]:
        return _wrap_data(self._data, 'channel_post', Message)

    @property
    def edited_channel_post(self) -> Optional[Message]:
        return _wrap_data(self._data, 'edited_channel_post', Message)

    @property
    def inline_query(self) -> Optional[InlineQuery]:
        return _wrap_data(self._data, 'inline_query', InlineQuery)

    @property
    def chosen_inline_result(self) -> Optional[ChosenInlineResult]:
        return _wrap_data(self._data, 'chosen_inline_result', ChosenInlineResult)

    @property
    def callback_query(self) -> Optional[CallbackQuery]:
        return _wrap_data(self._data, 'callback_query', CallbackQuery)


class WebhookInfo(object):

    def __init__(self, data) -> None:
        self._data = data

    @property
    def url(self) -> str:
        return self._data['url']

    @property
    def has_custom_certificate(self) -> bool:
        return self._data['has_custom_certificate']

    @property
    def pending_update_count(self) -> int:
        return self._data['pending_update_count']

    @property
    def last_error_date(self) -> int:
        return _wrap_data(self._data, 'last_error_date')

    @property
    def last_error_message(self) -> str:
        return _wrap_data(self._data, 'last_error_message')

    @property
    def max_connections(self) -> int:
        return _wrap_data(self._data, 'max_connections')

    @property
    def allowed_updates(self) -> List[str]:
        return _wrap_data(self._data, 'allowed_updates')


class User(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def id_(self) -> int:
        return self._data['id']

    @property
    def first_name(self) -> str:
        return self._data['first_name']

    @property
    def last_name(self) -> Optional[str]:
        return self._data.get('last_name', None)

    @property
    def username(self) -> Optional[str]:
        return self._data.get('username', None)


class Chat(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def id_(self) -> int:
        return self._data['id']

    @property
    def type_(self) -> str:
        return self._data['type']

    @property
    def title(self) -> Optional[str]:
        return self._data.get('title', None)

    @property
    def username(self) -> Optional[str]:
        return self._data.get('username', None)

    @property
    def first_name(self) -> Optional[str]:
        return self._data.get('first_name', None)

    @property
    def last_name(self) -> Optional[str]:
        return self._data.get('last_name', None)

    @property
    def all_members_are_administrators(self) -> Optional[bool]:
        return self._data.get('all_members_are_administrators', None)


class Message(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def message_id(self) -> int:
        return self._data['message_id']

    @property
    def from_(self) -> Optional[User]:
        return _wrap_data(self._data, 'from', User)

    @property
    def date(self) -> int:
        return self._data['date']

    @property
    def chat(self) -> Chat:
        return Chat(data['chat'])

    @property
    def forward_from(self) -> Optional[User]:
        return _wrap_data(self._data, 'forward_from', User)

    @property
    def forward_from_chat(self) -> Optional[Chat]:
        return _wrap_data(self._data, 'forward_from_chat', Chat)

    @property
    def forward_from_message_id(self) -> Optional[int]:
        return _wrap_data(self._data, 'forward_from_message_id')

    @property
    def forward_date(self) -> Optional[int]:
        return self._data.get('forward_date', None)

    @property
    def reply_to_message(self) -> Optional[Message]:
        return _wrap_data(self._data, 'reply_to_message', Message)

    @property
    def edit_date(self) -> Optional[int]:
        return _wrap_data(self._data, 'edit_date')

    @property
    def text(self) -> Optional[str]:
        return self._data.get('text', None)

    @property
    def entities(self) -> Optional[List[MessageEntity]]:
        if 'entities' not in self._data:
            return None
        data = self._data['entities']
        data = [MessageEntity(_) for _ in data]
        return data

    @property
    def audio(self) -> Optional[Audio]:
        return _wrap_data(self._data, 'audio', Audio)

    @property
    def document(self) -> Optional[Document]:
        return _wrap_data(self._data, 'document', Document)

    @property
    def game(self) -> Optional[Game]:
        return _wrap_data(self._data, 'game', Game)

    @property
    def photo(self) -> Optional[List[PhotoSize]]:
        if 'photo' not in self._data:
            return None
        data = self._data['photo']
        data = [PhotoSize(_) for _ in data]
        return data

    @property
    def sticker(self) -> Optional[Sticker]:
        return _wrap_data(self._data, 'sticker', Sticker)

    @property
    def video(self) -> Optional[Video]:
        return _wrap_data(self._data, 'video', Video)

    @property
    def voice(self) -> Optional[Voice]:
        return _wrap_data(self._data, 'voice', Voice)

    @property
    def caption(self) -> Optional[str]:
        return _wrap_data(self._data, 'caption')

    @property
    def contact(self) -> Optional[Contact]:
        return _wrap_data(self._data, 'contact', Contact)

    @property
    def location(self) -> Optional[Location]:
        return _wrap_data(self._data, 'location', Location)

    @property
    def venue(self) -> Optional[Venue]:
        return _wrap_data(self._data, 'venue', Venue)

    @property
    def new_chat_member(self) -> Optional[User]:
        return _wrap_data(self._data, 'new_chat_member', User)

    @property
    def left_chat_member(self) -> Optional[User]:
        return _wrap_data(self._data, 'left_chat_member', User)

    @property
    def new_chat_title(self) -> Optional[str]:
        return self._data.get('new_chat_title', None)

    @property
    def new_chat_photo(self) -> Optional[List[PhotoSize]]:
        if 'new_chat_photo' not in self._data:
            return None
        data = self._data['new_chat_photo']
        data = [PhotoSize(_) for _ in data]
        return data

    @property
    def delete_chat_photo(self) -> Optional[bool]:
        return self._data.get('delete_chat_photo', None)

    @property
    def group_chat_created(self) -> Optional[bool]:
        return self._data.get('group_chat_created', None)

    @property
    def supergroup_chat_created(self) -> Optional[bool]:
        return _wrap_data(self._data, 'supergroup_chat_created')

    @property
    def channel_chat_created(self) -> Optional[bool]:
        return _wrap_data(self._data, 'channel_chat_created')

    @property
    def migrate_to_chat_id(self) -> Optional[int]:
        return _wrap_data(self._data, 'migrate_to_chat_id')

    @property
    def migrate_from_chat_id(self) -> Optional[int]:
        return _wrap_data(self._data, 'migrate_from_chat_id')

    @property
    def pinned_message(self) -> Optional[Message]:
        return _wrap_data(self._data, 'pinned_message', Message)


class MessageEntity(object):

    def __init__(self, data) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def type_(self) -> str:
        return self._data['type']

    @property
    def offset(self) -> int:
        return self._data['offset']

    @property
    def length(self) -> int:
        return self._data['length']

    @property
    def url(self) -> Optional[str]:
        return _wrap_data(self._data, 'url')

    @property
    def user(self) -> Optional[User]:
        return _wrap_data(self._data, 'user', User)


class PhotoSize(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def width(self) -> int:
        return self._data['width']

    @property
    def height(self) -> int:
        return self._data['height']

    @property
    def file_size(self) -> Optional[int]:
        return self._data.get('file_size', None)


class Audio(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def duration(self) -> int:
        return self._data['duration']

    @property
    def performer(self) -> Optional[str]:
        return _wrap_data(self._data, 'performer')

    @property
    def title(self) -> Optional[str]:
        return _wrap_data(self._data, 'title')

    @property
    def mime_type(self) -> Optional[str]:
        return self._data.get('mime_type', None)

    @property
    def file_size(self) -> Optional[int]:
        return self._data.get('file_size', None)


class Document(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def thumb(self) -> Optional[PhotoSize]:
        return _wrap_data(self._data, 'thumb', PhotoSize)

    @property
    def file_name(self) -> Optional[str]:
        return self._data.get('file_name', None)

    @property
    def mime_type(self) -> Optional[str]:
        return self._data.get('mime_type', None)

    @property
    def file_size(self) -> Optional[int]:
        return self._data.get('file_size', None)


class Sticker(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def width(self) -> int:
        return self._data['width']

    @property
    def height(self) -> int:
        return self._data['height']

    @property
    def thumb(self) -> Optional[PhotoSize]:
        return _wrap_data(self._data, 'thumb', PhotoSize)

    @property
    def emoji(self) -> Optional[str]:
        return _wrap_data(self._data, 'emoji')

    @property
    def file_size(self) -> Optional[int]:
        return self._data.get('file_size', None)


class Video(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def width(self) -> int:
        return self._data['width']

    @property
    def height(self) -> int:
        return self._data['height']

    @property
    def duration(self) -> int:
        return self._data['duration']

    @property
    def thumb(self) -> Optional[PhotoSize]:
        return _wrap_data(self._data, 'thumb', PhotoSize)

    @property
    def mime_type(self) -> Optional[str]:
        return self._data.get('mime_type', None)

    @property
    def file_size(self) -> Optional[int]:
        return self._data.get('file_size', None)


class Voice(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def duration(self) -> int:
        return self._data['duration']

    @property
    def mime_type(self) -> Optional[str]:
        return _wrap_data(self._data, 'mime_type')

    @property
    def file_size(self) -> Optional[int]:
        return _wrap_data(self._data, 'file_size')


class Contact(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def phone_number(self) -> str:
        return self._data['phone_number']

    @property
    def first_name(self) -> str:
        return self._data['first_name']

    @property
    def last_name(self) -> Optional[str]:
        return self._data.get('last_name', None)

    @property
    def user_id(self) -> Optional[int]:
        return self._data.get('user_id', None)


class Location(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def longitude(self) -> float:
        return self._data['phone_number']

    @property
    def latitude(self) -> float:
        return self._data['first_name']


class Venue(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def location(self) -> Location:
        return self._data['location']

    @property
    def title(self) -> str:
        return self._data['title']

    @property
    def address(self) -> str:
        return self._data['address']

    @property
    def foursquare_id(self) -> Optional[str]:
        return _wrap_data(self._data, 'foursquare_id')


class UserProfilePhotos(object):

    def __init__(self, data: dict) -> None:
        self._data = data
        self._photos = [[PhotoSize(ps) for ps in pss] for pss in data['photos']]

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def total_count(self) -> int:
        return self._data['total_count']

    @property
    def photos(self) -> List[List[PhotoSize]]:
        return self._photos


class File(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def file_size(self) -> Optional[int]:
        return _wrap_data(self._data, 'file_size')

    @property
    def file_path(self) -> Optional[str]:
        return _wrap_data(self._data, 'file_path')


class ReplyKeyboardMarkup(object):

    def __init__(self, keyboard: List[List['KeyboardButton']],
                 resize_keyboard: bool = None, one_time_keyboard: bool = None,
                 selective: bool = None) -> None:
        data = {
            'keyboard': keyboard,
        }
        if resize_keyboard is not None:
            data['resize_keyboard'] = resize_keyboard
        if one_time_keyboard is not None:
            data['one_time_keyboard'] = one_time_keyboard
        if selective is not None:
            data['selective'] = selective
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)


class KeyboardButton(object):

    def __init__(self, text: str,
                 request_contact: bool = None, request_location: bool = None
                 ) -> None:
        data = {
            'text': text,
        }
        if request_contact is not None:
            data['request_contact'] = request_contact
        if request_location is not None:
            data['request_location'] = request_location
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)


class ReplyKeyboardRemove(object):

    def __init__(self, remove_keyboard: bool, selective: bool = None) -> None:
        data = {
            'remove_keyboard': remove_keyboard,
        }
        if selective is not None:
            data['selective'] = selective
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)


class InlineKeyboardMarkup(object):

    def __init__(self, inline_keyboard: List[List['InlineKeyboardButton']]
                 ) -> None:
        data = {
            'inline_keyboard': inline_keyboard,
        }
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)


class InlineKeyboardButton(object):

    def __init__(self, text: str, url: str = None, callback_data: str = None,
                 switch_inline_query: str = None,
                 switch_inline_query_current_chat: str = None,
                 callback_game: 'CallbackGame' = None) -> None:
        data = {
            'text': text,
        }
        if url is not None:
            data['url'] = url
        if callback_data is not None:
            data['callback_data'] = callback_data
        if switch_inline_query is not None:
            data['switch_inline_query'] = switch_inline_query
        if switch_inline_query_current_chat is not None:
            data['switch_inline_query_current_chat'] = switch_inline_query_current_chat
        if callback_game is not None:
            data['callback_game'] = callback_game
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)


class CallbackQuery(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def id_(self) -> str:
        return self._data['id']

    @property
    def from_(self) -> User:
        return User(self._data['from'])

    @property
    def message(self) -> Optional[Message]:
        return _wrap_data(self._data, 'message', Message)

    @property
    def inline_message_id(self) -> Optional[str]:
        return _wrap_data(self._data, 'inline_message_id')

    @property
    def chat_instance(self) -> str:
        return self._data['chat_instance']

    @property
    def data(self) -> Optional[str]:
        return _wrap_data(self._data, 'data')

    @property
    def game_short_name(self) -> Optional[str]:
        return _wrap_data(self._data, 'game_short_name')


class ForceReply(object):

    def __init__(self, force_reply: bool, selective: bool = None) -> None:
        data = {
            'force_reply': force_reply,
        }
        if selective is not None:
            data['selective'] = selective
        self._data = data

    def __str__(self) -> None:
        return json.dumps(self._data)


class ChatMember(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def user(self) -> User:
        return User(self._data['user'])

    @property
    def status(self) -> str:
        return self._data['status']


class ResponseParameters(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def migrate_to_chat_id(self) -> int:
        return _wrap_data(self._data, 'migrate_to_chat_id')

    @property
    def retry_after(self) -> int:
        return _wrap_data(self._data, 'retry_after')


class InputFile(object):

    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def name(self):
        import os.path as op
        return op.basename(self._file_path)

    @property
    def content_type(self):
        import mimetypes
        return mimetypes.guess_type(self._file_path)[0]

    @property
    def content(self):
        with open(self._file_path, 'rb') as fin:
            return fin.read()

    @property
    def size(self):
        return op.getsize(self._file_path)

    def stream(self, chunk_size=524288):
        with open(self._file_path, 'rb') as fin:
            while True:
                chunk = fin.read(chunk_size)
                if not chunk:
                    break
                yield chunk


class InlineQuery(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def id_(self) -> str:
        return self._data['id']

    @property
    def from_(self) -> User:
        return User(self._data['from'])

    @property
    def location(self) -> Optinal[Location]:
        return _wrap_data(self._data, 'location', Location)

    @property
    def query(self) -> str:
        return self._data['query']

    @property
    def offset(self) -> str:
        return self._data['offset']


class InlineQueryResult(object):

    def __init__(self, type_: str, id_: int) -> None:
        self._data = {
            'type': type_,
            'id': id_,
        }

    def __str__(self) -> None:
        return json.dumps(self._data)


class InlineQueryResultArticle(InlineQueryResult):

    def __init__(self, id_: int, title: str,
                 input_message_content: InputMessageContent,
                 reply_markup: InlineKeyboardMarkup = None,
                 url: str = None, hide_url: bool = None,
                 description: str = None, thumb_url: str = None,
                 thumb_width: int = None, thumb_height: int = None) -> None:
        super(InlineQueryResultArticle, self).__init__('article', id_)

        self._data.update({
            'input_message_content': input_message_content,
        })

        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if url is not None:
            self._data['url'] = url
        if hide_url is not None:
            self._data['hide_url'] = hide_url
        if description is not None:
            self._data['description'] = description
        if thumb_url is not None:
            self._data['thumb_url'] = thumb_url
        if thumb_width is not None:
            self._data['thumb_width'] = thumb_width
        if thumb_height is not None:
            self._data['thumb_height'] = thumb_height


class InlineQueryResultPhoto(InlineQueryResult):

    def __init__(self, id_: int, photo_url: str, thumb_url: str,
                 photo_width: int = None, photo_height: int = None,
                 title: str = None, description: str = None,
                 caption: str = None, reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultPhoto, self).__init__('photo', id_)

        self._data.update({
            'photo_url': photo_url,
            'thumb_url': thumb_url,
        })

        if photo_width is not None:
            self._data['photo_width'] = photo_width
        if photo_height is not None:
            self._data['photo_height'] = photo_height
        if title is not None:
            self._data['title'] = title
        if description is not None:
            self._data['description'] = description
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultGif(InlineQueryResult):

    def __init__(self, id_: int, gif_url: str, thumb_url: str,
                 gif_width: int = None, gif_height: int = None,
                 title: str = None, caption: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultGif, self).__init__('gif', id_)

        self._data.update({
            'gif_url': gif_url,
            'thumb_url': thumb_url,
        })

        if gif_width is not None:
            self._data['gif_width'] = gif_width
        if gif_height is not None:
            self._data['gif_height'] = gif_height
        if title is not None:
            self._data['title'] = title
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultMpeg4Gif(InlineQueryResult):

    def __init__(self, id_: int, mpeg4_url: str, thumb_url: str,
                 mpeg4_width: int = None, mpeg4_height: int = None,
                 title: str = None, caption: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultMpeg4Gif, self).__init__('mpeg4_gif', id_)

        self._data.update({
            'mpeg4_url': mpeg4_url,
            'thumb_url': thumb_url,
        })

        if mpeg4_width is not None:
            self._data['mpeg4_width'] = mpeg4_width
        if mpeg4_height is not None:
            self._data['mpeg4_height'] = mpeg4_height
        if title is not None:
            self._data['title'] = title
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultVideo(InlineQueryResult):

    def __init__(self, id_: int, video_url: str, mime_type: str, thumb_url: str,
                 title: str, caption: str = None, video_width: int = None,
                 video_height: int = None, video_duration: int = None,
                 description: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultVideo, self).__init__('video', id_)

        self._data.update({
            'video_url': video_url,
            'mime_type': mime_type,
            'thumb_url': thumb_url,
            'title': title,
        })

        if caption is not None:
            self._data['caption'] = caption
        if video_width is not None:
            self._data['video_width'] = video_width
        if video_height is not None:
            self._data['video_height'] = video_height
        if video_duration is not None:
            self._data['video_duration'] = video_duration
        if description is not None:
            self._data['description'] = description
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultAudio(InlineQueryResult):

    def __init__(self, id_: int, audio_url: str, title: str,
                 caption: str = None, performer: str = None,
                 audio_duration: int = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultAudio, self).__init__('audio', id_)

        self._data.update({
            'audio_url': audio_url,
            'title': title,
        })

        if caption is not None:
            self._data['caption'] = caption
        if performer is not None:
            self._data['performer'] = performer
        if audio_duration is not None:
            self._data['audio_duration'] = audio_duration
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultVoice(InlineQueryResult):

    def __init__(self, id_: int, voice_url: str, title: str,
                 caption: str = None, voice_duration: int = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultVoice, self).__init__('voice', id_)

        self._data.update({
            'voice_url': voice_url,
            'title': title,
        })

        if caption is not None:
            self._data['caption'] = caption
        if voice_duration is not None:
            self._data['voice_duration'] = voice_duration
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultDocument(InlineQueryResult):

    def __init__(self, id_: int, title: str, document_url: str, mime_type: str,
                 caption: str = None, description: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None, thumb_width: int = None,
                 thumb_height: int = None) -> None:
        super(InlineQueryResultDocument, self).__init__('document', id_)

        self._data.update({
            'title': title,
            'document_url': document_url,
            'mime_type': mime_type,
        })

        if caption is not None:
            self._data['caption'] = caption
        if description is not None:
            self._data['description'] = description
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content
        if thumb_url is not None:
            self._data['thumb_url'] = thumb_url
        if thumb_width is not None:
            self._data['thumb_width'] = thumb_width
        if thumb_height is not None:
            self._data['thumb_height'] = thumb_height


class InlineQueryResultLocation(InlineQueryResult):

    def __init__(self, id_: int, latitude: float, longitude: float, title: str,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None, thumb_width: int = None,
                 thumb_height: int = None) -> None:
        super(InlineQueryResultLocation, self).__init__('location', id_)

        self._data.update({
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
        })

        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content
        if thumb_url is not None:
            self._data['thumb_url'] = thumb_url
        if thumb_width is not None:
            self._data['thumb_width'] = thumb_width
        if thumb_height is not None:
            self._data['thumb_height'] = thumb_height


class InlineQueryResultVenue(InlineQueryResult):

    def __init__(self, id_: int, latitude: float, longitude: float, title: str,
                 address: str, foursquare_id: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None, thumb_width: int = None,
                 thumb_height: int = None) -> None:
        super(InlineQueryResultVenue, self).__init__('venue', id_)

        self._data.update({
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
        })

        if foursquare_id is not None:
            self._data['foursquare_id'] = foursquare_id
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content
        if thumb_url is not None:
            self._data['thumb_url'] = thumb_url
        if thumb_width is not None:
            self._data['thumb_width'] = thumb_width
        if thumb_height is not None:
            self._data['thumb_height'] = thumb_height


class InlineQueryResultContact(InlineQueryResult):

    def __init__(self, id_: int, phone_number: str, first_name: str,
                 last_name: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None,
                 thumb_url: str = None, thumb_width: int = None,
                 thumb_height: int = None) -> None:
        super(InlineQueryResultContact, self).__init__('contact', id_)

        self._data.update({
            'phone_number': phone_number,
            'first_name': first_name,
        })

        if last_name is not None:
            self._data['last_name'] = last_name
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content
        if thumb_url is not None:
            self._data['thumb_url'] = thumb_url
        if thumb_width is not None:
            self._data['thumb_width'] = thumb_width
        if thumb_height is not None:
            self._data['thumb_height'] = thumb_height


class InlineQueryResultGame(InlineQueryResult):

    def __init__(self, id_: int, game_short_name: str,
                 reply_markup: InlineKeyboardMarkup = None) -> None:
        super(InlineQueryResultGame, self).__init__('game', id_)

        self._data.update({
            'game_short_name': game_short_name,
        })

        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup


class InlineQueryResultCachedPhoto(InlineQueryResult):

    def __init__(self, id_: int, photo_file_id: str, title: str = None,
                 description: str = None, caption: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedPhoto, self).__init__('photo', id_)

        self._data.update({
            'photo_file_id': photo_file_id,
        })

        if title is not None:
            self._data['title'] = title
        if description is not None:
            self._data['description'] = description
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedGif(InlineQueryResult):

    def __init__(self, id_: int, gif_file_id: str, title: str = None,
                 caption: str = None, reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedGif, self).__init__('gif', id_)

        self._data.update({
            'gif_file_id': gif_file_id,
        })

        if title is not None:
            self._data['title'] = title
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedMpeg4Gif(InlineQueryResult):

    def __init__(self, id_: int, mpeg4_file_id: str, title: str = None,
                 caption: str = None, reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedMpeg4Gif, self).__init__('mpeg4_gif', id_)

        self._data.update({
            'mpeg4_file_id': mpeg4_file_id,
        })

        if title is not None:
            self._data['title'] = title
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedSticker(InlineQueryResult):

    def __init__(self, id_: int, sticker_file_id: str,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedSticker, self).__init__('sticker', id_)

        self._data.update({
            'sticker_file_id': sticker_file_id,
        })

        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedDocument(InlineQueryResult):

    def __init__(self, id_: int, title: str, document_file_id: str,
                 description: str = None, caption: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedDocument, self).__init__('document', id_)

        self._data.update({
            'title': title,
            'document_file_id': document_file_id,
        })

        if description is not None:
            self._data['description'] = description
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedVideo(InlineQueryResult):

    def __init__(self, id_: int, video_file_id: str, title: str,
                 description: str = None, caption: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedVideo, self).__init__('video', id_)

        self._data.update({
            'video_file_id': video_file_id,
            'title': title,
        })

        if description is not None:
            self._data['description'] = description
        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedVoice(InlineQueryResult):

    def __init__(self, id_: int, voice_file_id: str, title: str,
                 caption: str = None, reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedVoice, self).__init__('voice', id_)

        self._data.update({
            'voice_file_id': voice_file_id,
            'title': title,
        })

        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InlineQueryResultCachedAudio(InlineQueryResult):

    def __init__(self, id_: int, audio_file_id: str, caption: str = None,
                 reply_markup: InlineKeyboardMarkup = None,
                 input_message_content: InputMessageContent = None) -> None:
        super(InlineQueryResultCachedAudio, self).__init__('audio', id_)

        self._data.update({
            'audio_file_id': audio_file_id,
        })

        if caption is not None:
            self._data['caption'] = caption
        if reply_markup is not None:
            self._data['reply_markup'] = reply_markup
        if input_message_content is not None:
            self._data['input_message_content'] = input_message_content


class InputMessageContent(object):

    def __init__(self) -> None:
        self._data = {}

    def __str__(self) -> None:
        return json.dumps(self._data)


class InputTextMessageContent(InputMessageContent):

    def __init__(self, message_text: str, parse_mode: str = None,
                 disable_web_page_preview: bool = None) -> None:
        super(InputTextMessageContent, self).__init__()

        self._data.update({
            'message_text': message_text,
        })

        if parse_mode is not None:
            self._data['parse_mode'] = parse_mode
        if disable_web_page_preview is not None:
            self._data['disable_web_page_preview'] = disable_web_page_preview


class InputLocationMessageContent(InputMessageContent):

    def __init__(self, latitude: float, longitude: float) -> None:
        super(InputLocationMessageContent, self).__init__()

        self._data.update({
            'latitude': latitude,
            'longitude': longitude,
        })


class InputVenueMessageContent(InputMessageContent):

    def __init__(self, latitude: float, longitude: float, title: str,
                 address: str, foursquare_id: str = None) -> None:
        super(InputVenueMessageContent, self).__init__()

        self._data.update({
            'latitude': latitude,
            'longitude': longitude,
            'title': title,
            'address': address,
        })

        if foursquare_id is not None:
            self._data['foursquare_id'] = foursquare_id


class InputContactMessageContent(InputMessageContent):

    def __init__(self, phone_number: str, first_name: str,
                 last_name: str = None) -> None:
        super(InputContactMessageContent, self).__init__()

        self._data.update({
            'phone_number': phone_number,
            'first_name': first_name,
        })

        if last_name is not None:
            self._data['last_name'] = last_name


class ChosenInlineResult(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> None:
        return json.dumps(self._data)

    @property
    def result_id(self) -> str:
        return self._data['result_id']

    @property
    def from_(self) -> User:
        return self._data['from']

    @property
    def location(self) -> Optional[Location]:
        return _wrap_data(self._data, 'location', Location)

    @property
    def inline_message_id(self) -> Optional[str]:
        return _wrap_data(self._data, 'inline_message_id')

    @property
    def query(self) -> str:
        return self._data['query']


class Game(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def title(self) -> str:
        return self._data['title']

    @property
    def description(self) -> str:
        return self._data['description']

    @property
    def photo(self) -> List[PhotoSize]:
        data = self._data['photo']
        data = [PhotoSize(_) for _ in data]

    @property
    def text(self) -> Optional[str]:
        return _wrap_data(self._data, 'text')

    @property
    def text_entities(self) -> Optional[List[MessageEntity]]:
        if 'text_entities' not in self._data:
            return None
        data = self._data['text_entities']
        data = [MessageEntity(_) for _ in data]
        return data

    @property
    def animation(self) -> Optional[Animation]:
        return _wrap_data(self._data, 'animation', Animation)


class Animation(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def file_id(self) -> str:
        return self._data['file_id']

    @property
    def thumb(self) -> Optional[PhotoSize]:
        return _wrap_data(self._data, 'thumb', PhotoSize)

    @property
    def file_name(self) -> Optional[str]:
        return _wrap_data(self._data, 'file_name')

    @property
    def mime_type(self) -> Optional[str]:
        return _wrap_data(self._data, 'mime_type')

    @property
    def file_size(self) -> Optional[int]:
        return _wrap_data(self._data, 'file_size')


class CallbackGame(object):

    pass


class GameHighScore(object):

    def __init__(self, data: dict) -> None:
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data)

    @property
    def position(self) -> int:
        return self._data['position']

    @property
    def user(self) -> User:
        return User(self._data['user'])

    @property
    def score(self) -> int:
        return self._data['score']


def _wrap_data(data, key, type_=None):
    if key not in data:
        return None
    if type_ is None:
        return data[key]
    return type_(data[key])
