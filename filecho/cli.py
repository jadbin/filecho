# coding=utf-8

import sys
import argparse
import logging.config

from filecho.server import Server


class Command:
    @property
    def description(self):
        return "Run a web server for serving static files"

    def add_arguments(self, parser):
        parser.add_argument("-d", "--dir", dest="dir", metavar="DIR",
                            help="the root directory of static files")
        parser.add_argument("-p", "--port", dest="port", metavar="PORT", type=int, default=80,
                            help="serving port")

    def run(self, args):
        logger = {
            "version": 1,
            "loggers": {
                "filecho": {
                    "level": "INFO",
                    "handlers": ["console"]
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default"
                }
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(name)s: [%(levelname)s] %(message)s",
                    "datefmt": "%b/%d/%Y %H:%M:%S"
                }
            }
        }
        logging.config.dictConfig(logger)
        root_dir = args.dir
        if not root_dir:
            raise UsageError()
        port = args.port
        server = Server(port, root_dir)
        server.run()


class UsageError(Exception):
    """
    Usage error
    """


def main(argv=None):
    if argv is None:
        argv = sys.argv
    command = Command()
    parser = argparse.ArgumentParser()
    parser.prog = "filecho"
    parser.description = command.description
    command.add_arguments(parser)
    args = parser.parse_args(args=argv[1:])
    try:
        command.run(args)
    except UsageError as e:
        parser.print_help()
        if str(e):
            print("")
            print("{0}: error: {1}".format(parser.prog, e))
        sys.exit(2)
