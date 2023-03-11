from flask import Response

class end_point_action(object):
    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        if self.action:
            self.action()
        return self.response