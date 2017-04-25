# coding=utf-8

import os
import asyncio
import logging
import threading

from aiohttp import web

log = logging.getLogger(__name__)


class Server:
    def __init__(self, port, root_dir):
        self._port = port
        self._root_dir = os.path.abspath(root_dir)
        self._loop = asyncio.new_event_loop()

    def run(self):
        def _run():
            asyncio.set_event_loop(self._loop)
            try:
                self._loop.run_forever()
            except Exception:
                log.error("Unexpected error occurred when run loop", exc_info=True)
                raise
            finally:
                self._loop.close()

        log.info("Run web server, port={0}, root directory={1}".format(self._port, self._root_dir))
        app = web.Application(logger=log, loop=self._loop)
        app.router.add_static("/", path=self._root_dir, name="static")
        self._loop.run_until_complete(self._loop.create_server(app.make_handler(access_log=None, loop=self._loop),
                                                               "0.0.0.0",
                                                               self._port))
        t = threading.Thread(target=_run)
        t.start()
