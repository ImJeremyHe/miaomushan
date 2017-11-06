import tornado.web
import json


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        if self.application.user_info:
            return self.application.user_info
        key = self.get_cookie("mms")
        if key:
            value = self.application.rd.get(key)
            if value:
                self.application.user_info = json.loads(value)
                return self.application.user_info
        return
