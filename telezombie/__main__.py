import sys

from tornado import ioloop, gen

from . import api, types


@gen.coroutine
def get_updates(bot):
    offset = 0
    limit = 100
    updates = []
    while True:
        us = yield bot.get_updates(offset, limit)
        updates.extend(us)
        if not us:
            break
        offset = us[-1].update_id + 1
    return updates


@gen.coroutine
def forever():
    bot = api.TeleZombie()
    user = yield bot.get_me()
    print(user)

    while True:
        updates = yield get_updates(bot)
        for u in updates:
            msg = u.message
            chat = msg.chat
            text = msg.text
            bot.send_message(chat.id_, text)


def main(args=None):
    if args is None:
        args = sys.argv

    main_loop = ioloop.IOLoop.instance()

    main_loop.run_sync(forever)

    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
