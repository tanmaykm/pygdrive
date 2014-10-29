#!/usr/bin/python

import os
import logging

import tornado.ioloop
import tornado.web

from synchandler import SyncHandler
from authhandler import AuthHandler


def read_config():
    with open("conf/server.conf") as f:
        cfg_read = eval(f.read())
    cfg_read['home_folder'] = os.path.expanduser(cfg_read['home_folder'])
    cfg_read['token_file'] = os.path.expanduser(cfg_read['token_file'])
    return cfg_read


def run():
    logging.basicConfig(format='%(asctime)-15s %(message)s')
    logger = logging.getLogger('pygdrive')
    logger.setLevel(logging.DEBUG)

    cfg = read_config()

    SyncHandler.LOC = cfg['home_folder']

    application = tornado.web.Application([
        (r"/", SyncHandler),
        (r"/auth/", AuthHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './www/static'}),
    ])
    application.listen(cfg['port'])
    application.settings["google_oauth"] = cfg["google_oauth"]
    application.settings['token_file'] = cfg['token_file']

    logger.info("Server listening on " + str(cfg['port']))
    logger.info("Open http://localhost:" + str(cfg['port']) + " in your browser.")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    run()