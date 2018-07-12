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
        try:
            self._loop = asyncio.get_event_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        self._app_runner = None
        self._tcp_site = None

    def run(self):
        log.info("Run web server, port={}, root directory={}, prefix={}".format(self._port,
                                                                                self._root_dir,
                                                                                self._prefix))
        app = web.Application(logger=log, loop=self._loop)
        app.router.add_static(self._prefix, path=self._root_dir, name="static")
        self._app_runner = web.AppRunner(app, access_log=None)
        self._loop.run_until_complete(self._app_runner.setup())
        self._tcp_site = web.TCPSite(self._app_runner, host='0.0.0.0', port=self._port)
        self._loop.run_until_complete(self._tcp_site.start())
        asyncio.set_event_loop(self._loop)
        self._loop.add_signal_handler(signal.SIGINT, lambda sig=signal.SIGINT: self.shutdown(sig=sig))
        self._loop.add_signal_handler(signal.SIGTERM, lambda sig=signal.SIGTERM: self.shutdown(sig=sig))
        try:
            self._loop.run_forever()
        except Exception as e:
            log.error("Unexpected error occurred when run loop: %s", e)
            raise

    def shutdown(self, sig=None):
        if sig is not None:
            log.info('Received shutdown signal: %s', sig)
        asyncio.ensure_future(self._shutdown(), loop=self._loop)

    async def _shutdown(self):
        log.info("Shutdown now")
        await self._tcp_site.stop()
        self._tcp_site = None
        await self._app_runner.cleanup()
        self._app_runner = None
        self._loop.stop()
        self._loop.remove_signal_handler(signal.SIGINT)
        self._loop.remove_signal_handler(signal.SIGTERM)
