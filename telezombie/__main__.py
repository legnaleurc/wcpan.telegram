import sys

from tornado import ioloop, gen, options

from . import api, types, settings


class KelThuzad(api.TeleLich):

    def __init__(self, api_token):
        super(KelThuzad, self).__init__(api_token)

    @gen.coroutine
    def on_text(self, message):
        id_ = message.message_id
        chat = message.chat
        text = message.text
        yield self.send_message(chat.id_, text, reply_to_message_id=id_)

    @gen.coroutine
    def on_audio(self, message):
        chat = message.chat
        audio = message.audio
        yield self.send_audio(chat.id_, audio.file_id, reply_to_message_id=id_)

    @gen.coroutine
    def on_document(self, message):
        chat = message.chat
        document = message.document
        yield self.send_document(chat.id_, document.file_id, reply_to_message_id=id_)

    @gen.coroutine
    def on_photo(self, message):
        chat = message.chat
        photo = message.photo
        for p in photo:
            yield self.send_photo(chat.id_, p.file_id, reply_to_message_id=id_)

    @gen.coroutine
    def on_sticker(self, message):
        chat = message.chat
        sticker = message.sticker
        yield self.send_sticker(chat.id_, sticker.file_id, reply_to_message_id=id_)

    @gen.coroutine
    def on_video(self, message):
        chat = message.chat
        video = message.video
        yield self.send_video(chat.id_, video.file_id, reply_to_message_id=id_)

    @gen.coroutine
    def on_contact(self, message):
        chat = message.chat
        contact = message.contact
        yield self.send_video(chat.id_, contact.phone_number, reply_to_message_id=id_)

    @gen.coroutine
    def on_location(self, message):
        chat = message.chat
        location = message.location
        yield self.send_video(chat.id_, location.longitude, location.latitude, reply_to_message_id=id_)


@gen.coroutine
def forever():
    api_token = options.options.api_token

    kel_thuzad = KelThuzad(api_token)

    yield kel_thuzad.poll()


def parse_config(path):
    data = settings.load(path)
    options.options.api_token = data['api_token']


def main(args=None):
    if args is None:
        args = sys.argv

    options.define('config', default=None, type=str, help='config file path', metavar='telezombie.yaml', callback=parse_config)
    options.define('api_token', default=None, type=str, help='API token', metavar='<token>')
    remains = options.parse_command_line(args)

    main_loop = ioloop.IOLoop.instance()

    main_loop.run_sync(forever)

    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
