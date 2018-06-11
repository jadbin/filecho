# coding=utf-8

import os
import asyncio
import logging
import signal

from aiohttp import web

log = logging.getLogger(__name__)


class Server:
    def __init__(self, port, root_dir, prefix=None):
        self._port = port
        self._root_dir = os.path.abspath(root_dir)
        self._prefix = prefix or ''
        if not self._prefix.startswith('/'):
            self._prefix = '/' + self._prefix
        self._loop = asyncio.new_event_loop()

    def run(self):
        log.info("Run web server, port={}, root directory={}, prefix={}".format(self._port,
                                                                                self._root_dir,
                                                                                self._prefix))
        app = web.Application(logger=log, loop=self._loop)
        app.router.add_static(self._prefix, path=self._root_dir, name="static")
        self._loop.run_until_complete(self._loop.create_server(app.make_handler(access_log=None, loop=self._loop),
                                                               "0.0.0.0",
                                                               self._port))
        asyncio.set_event_loop(self._loop)
        self._loop.add_signal_handler(signal.SIGINT,
                                      lambda loop=self._loop: asyncio.ensure_future(self.shutdown(), loop=loop))
        self._loop.add_signal_handler(signal.SIGTERM,
                                      lambda loop=self._loop: asyncio.ensure_future(self.shutdown(), loop=loop))
        try:
            self._loop.run_forever()
        except Exception:
            log.error("Unexpected error occurred when run loop", exc_info=True)
            raise
        finally:
            self._loop.close()

    async def shutdown(self):
        log.info("Shutdown now")
        self._loop.stop()
