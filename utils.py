# -*- coding: utf-8 -*-

try:
    import json
except:
    import simplejson as json

import datetime
import web # for browser_cache function, webpy
from weakref import WeakValueDictionary as WVD


def jsonify( cl, obj, *args):
    """Jsonify function for sqlalchemy model. v0.1 2012-12-28
Usage: 1: jsonify( User, user, User.name, User.address, ...) => {name:"zagfai",address:"Canton"}
       2: jsonify( User, users, User.name, ...) => [{name:"zagfai"},{name:"reatlk"}]
       3: jsonify( User, user) => {......all......}
"""
    def jsonifyone( obj, args):
        if args == ():
            args = dir(obj)
        else:
            args = [ str(attr).split('.')[1] for attr in args]
        return { a:getattr(obj, a) for a in args}

    class encoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, WVD):
                return None
            else:
                return json.JSONEncoder.default(self, obj)

    #start
    if isinstance( obj, list):
        lt = [ jsonifyone(i, args) for i in obj if isinstance(i,cl)]
        return json.dumps( lt, cls=encoder, ensure_ascii=False)
    else:
        return json.dumps(jsonifyone( obj, args), cls=encoder, ensure_ascii=False)

def browser_cache(seconds):
    """Decorator for browser. @browser_cache( seconds ) before GET/POST function."""
    def wrap(f):
        def wrapped_f(*args):
            last_time_str = web.ctx.env.get('HTTP_IF_MODIFIED_SINCE', '')
            last_time = web.net.parsehttpdate(last_time_str)
            now = datetime.datetime.now()
            if last_time and last_time + datetime.timedelta(seconds = seconds) > now:
                web.notmodified()
            else:
                web.lastmodified(now)
                web.header('Cache-Control', 'max-age='+str(seconds))
            yield f(*args)
        return wrapped_f
    return wrap
