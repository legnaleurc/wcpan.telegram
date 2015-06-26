import sys

from tornado import ioloop, gen

from . import api


@gen.coroutine
def forever():
    bot = api.TeleZombie()
    user = yield bot.get_me()
    print(user)
    offset = 0
    limit = 100
    updates = []
    while True:
        us = yield bot.get_updates(offset, limit)
        updates.extend(us)
        if len(us) < limit:
            break
        offset += limit
    for u in updates:
        print(u)


def main(args=None):
    if args is None:
        args = sys.argv

    main_loop = ioloop.IOLoop.instance()

    main_loop.run_sync(forever)

    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
