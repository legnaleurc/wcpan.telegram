import json
import os.path as op
from typing import Optional


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

    def __init__(self, data):
        self._data = data
        self._from = User(data['from'])
        chat = data['chat']
        if 'first_name' in chat:
            self._chat = User(chat)
        else:
            self._chat = GroupChat(chat)
        if 'forward_from' in data:
            self._forward_from = User(data['forward_from'])
        else:
            self._forward_from = None
        if 'reply_to_message' in data:
            self._reply_to_message = Message(data['reply_to_message'])
        else:
            self._reply_to_message = None
        if 'audio' in data:
            self._audio = Audio(data['audio'])
        else:
            self._audio = None
        if 'document' in data:
            self._document = Document(data['document'])
        else:
            self._document = None
        if 'photo' in data:
            self._photo = [PhotoSize(ps) for ps in data['photo']]
        else:
            self._photo = None
        if 'sticker' in data:
            self._sticker = Sticker(data['sticker'])
        else:
            self._sticker = None
        if 'video' in data:
            self._video = Video(data['video'])
        else:
            self._video = None
        if 'contact' in data:
            self._contact = Contact(data['contact'])
        else:
            self._contact = None
        if 'location' in data:
            self._location = Location(data['location'])
        else:
            self._location = None
        if 'new_chat_participant' in data:
            self._new_chat_participant = User(data['new_chat_participant'])
        else:
            self._new_chat_participant = None
        if 'left_chat_participant' in data:
            self._left_chat_participant = User(data['left_chat_participant'])
        else:
            self._left_chat_participant = None
        if 'new_chat_photo' in data:
            self._new_chat_photo = [PhotoSize(ps) for ps in data['new_chat_photo']]
        else:
            self._new_chat_photo = None
        if 'voice' in data:
            self._voice = {}

    def __str__(self):
        return json.dumps(self._data)

    @property
    def message_id(self):
        return self._data['message_id']

    @property
    def from_(self):
        return self._from

    @property
    def date(self):
        return self._data['date']

    @property
    def chat(self):
        return self._chat

    @property
    def forward_from(self):
        return self._forward_from

    @property
    def forward_date(self):
        return self._data.get('forward_date', None)

    @property
    def reply_to_message(self):
        return self._reply_to_message

    @property
    def text(self):
        return self._data.get('text', None)

    @property
    def audio(self):
        return self._audio

    @property
    def document(self):
        return self._document

    @property
    def photo(self):
        return self._photo

    @property
    def sticker(self):
        return self._sticker

    @property
    def video(self):
        return self._video

    @property
    def contact(self):
        return self._contact

    @property
    def location(self):
        return self._location

    @property
    def new_chat_participant(self):
        return self._new_chat_participant

    @property
    def left_chat_participant(self):
        return self._left_chat_participant

    @property
    def new_chat_title(self):
        return self._data.get('new_chat_title', None)

    @property
    def new_chat_photo(self):
        return self._new_chat_photo

    @property
    def delete_chat_photo(self):
        return self._data.get('delete_chat_photo', None)

    @property
    def group_chat_created(self):
        return self._data.get('group_chat_created', None)

    @property
    def voice(self):
        return 'dummy'


class PhotoSize(object):

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return json.dumps(self._data)

    @property
    def file_id(self):
        return self._data['file_id']

    @property
    def width(self):
        return self._data['width']

    @property
    def height(self):
        return self._data['height']

    @property
    def file_size(self):
        return self._data.get('file_size', None)


class Audio(object):

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return json.dumps(self._data)

    @property
    def file_id(self):
        return self._data['file_id']

    @property
    def duration(self):
        return self._data['duration']

    @property
    def mime_type(self):
        return self._data.get('mime_type', None)

    @property
    def file_size(self):
        return self._data.get('file_size', None)


class Document(object):

    def __init__(self, data):
        self._data = data
        self._thumb = PhotoSize(data['thumb']) if 'thumb' in data else None

    def __str__(self):
        return json.dumps(self._data)

    @property
    def file_id(self):
        return self._data['file_id']

    @property
    def thumb(self):
        return self._thumb

    @property
    def file_name(self):
        return self._data.get('file_name', None)

    @property
    def mime_type(self):
        return self._data.get('mime_type', None)

    @property
    def file_size(self):
        return self._data.get('file_size', None)


class Sticker(object):

    def __init__(self, data):
        self._data = data
        self._thumb = PhotoSize(data['thumb'])

    def __str__(self):
        return json.dumps(self._data)

    @property
    def file_id(self):
        return self._data['file_id']

    @property
    def width(self):
        return self._data['width']

    @property
    def height(self):
        return self._data['height']

    @property
    def thumb(self):
        return self._thumb

    @property
    def file_size(self):
        return self._data.get('file_size', None)


class Video(object):

    def __init__(self, data):
        self._data = data
        self._thumb = PhotoSize(data['thumb'])

    def __str__(self):
        return json.dumps(self._data)

    @property
    def file_id(self):
        return self._data['file_id']

    @property
    def width(self):
        return self._data['width']

    @property
    def height(self):
        return self._data['height']

    @property
    def duration(self):
        return self._data['duration']

    @property
    def thumb(self):
        return self._thumb

    @property
    def mime_type(self):
        return self._data.get('mime_type', None)

    @property
    def file_size(self):
        return self._data.get('file_size', None)

    @property
    def caption(self):
        return self._data.get('caption', None)


class Contact(object):

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return json.dumps(self._data)

    @property
    def phone_number(self):
        return self._data['phone_number']

    @property
    def first_name(self):
        return self._data['first_name']

    @property
    def last_name(self):
        return self._data.get('last_name', None)

    @property
    def user_id(self):
        return self._data.get('user_id', None)


class Location(object):

    def __init__(self, data):
        self._data = data

    def __str__(self):
        return json.dumps(self._data)

    @property
    def longitude(self):
        return self._data['phone_number']

    @property
    def latitude(self):
        return self._data['first_name']


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


class UserProfilePhotos(object):

    def __init__(self, data):
        self._data = data
        self._photos = [[PhotoSize(ps) for ps in pss] for pss in data['photos']]

    def __str__(self):
        return json.dumps(self._data)

    @property
    def total_count(self):
        return self._data['total_count']

    @property
    def photos(self):
        return self._photos


class ReplyKeyboardMarkup(object):

    def __init__(self, keyboard, resize_keyboard=None, one_time_keyboard=None, selective=None):
        data = {
            'hide_keyboard': hide_keyboard,
        }
        if resize_keyboard is not None:
            data['resize_keyboard'] = resize_keyboard
        if one_time_keyboard is not None:
            data['one_time_keyboard'] = one_time_keyboard
        if selective is not None:
            data['selective'] = selective
        self._data = data

    def __str__(self):
        return json.dumps(self._data)


class ReplyKeyboardHide(object):

    def __init__(self, hide_keyboard, selective=None):
        data = {
            'hide_keyboard': hide_keyboard,
        }
        if selective is not None:
            data['selective'] = selective
        self._data = data

    def __str__(self):
        return json.dumps(self._data)


class ForceReply(object):

    def __init__(self, force_reply, selective=None):
        data = {
            'force_reply': force_reply,
        }
        if selective is not None:
            data['selective'] = selective
        self._data = data

    def __str__(self):
        return json.dumps(self._data)


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


def _wrap_data(data, key, type_=None):
    if key not in data:
        return None
    if type_ is None:
        return data[key]
    return type_(data[key])
