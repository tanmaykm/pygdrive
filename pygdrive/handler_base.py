import logging

from tornado.web import RequestHandler


class HandlerBase(RequestHandler):
    _config = None
    logger = logging.getLogger('pygdrive')

    def rendertpl(self, tpl, **kwargs):
        self.render("../www/" + tpl, **kwargs)

    @classmethod
    def configure(cls, cfg):
        cls._config = cfg

    @classmethod
    def config(cls, key=None, default=None):
        if key is None:
            return cls._config
        if key in cls._config:
            return cls._config[key]
        else:
            return default
