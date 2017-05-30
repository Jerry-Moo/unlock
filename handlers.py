#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
from jinja2 import Environment, FileSystemLoader
#from sqlalchemy.exc import SQLAlchemyError
from models import Base, engine, Type, Ordertick
from datetime import datetime as dt

env = Environment(loader = FileSystemLoader('templates'))

class Redirect:
    def GET(self):
        web.found( '/' )

class Index:
    def GET(self):
        return env.get_template('index.html').render()
    def POST(self):
        return self.GET()
class Advantage:
    def GET(self):
        return env.get_template('advantage.html').render()
class Unlock:
    def GET(self):
        pics = set([ i[0] for i in web.ctx.orm.query(Type.pic_name).all() ])
        return env.get_template('unlock.html').render(pics=pics)
class Check:
    def GET(self):
        return env.get_template('check.html').render()
    def POST(self):
        data = web.input()
        tp = web.ctx.orm.query(Ordertick).\
                filter(Ordertick.imei == data.imei).\
                filter(Ordertick.email == data.email).\
                filter(Ordertick.id == data.oid).all()
        if not tp:
            return env.get_template('check.html').render(no=True)
        else:
            return env.get_template('checkdata.html').render(rec=tp[0])
class Faq:
    def GET(self):
        return env.get_template('faq.html').render()
class Order:
    def GET(self):
        picname = web.input().get('id')
        tp = web.ctx.orm.query(Type).filter(Type.pic_name == picname).all()
        print tp
        if tp:
            return env.get_template('order.html').render(tp = tp)
        else:
            web.seeother('/unlock')
class Ticket:
    def GET(self):
        web.seeother('/unlock')
    def POST(self):
        data = web.input()
        tp = web.ctx.orm.query(Type).\
            filter(Type.pic_name == data.picname).\
            filter(Type.phone_type == data.mmtype)
        print data
        try:
            tp = tp.one()
            if data.imei and data.email:
                ticket = Ordertick(tp.band, tp.phone_type, tp.support_device,
                        tp.time_cost, tp.price, "checking payment",
                        data.imei, data.email, dt.now())
                web.ctx.orm.add( ticket )
                web.ctx.orm.commit()
                return env.get_template('ticket.html').render(data=ticket)
            else:
                return ['Please input correct email and imei']
        except:
            web.ctx.orm.rollback()
            return ['Dont hack me please']

#env.get_template('index.html').render( uid = data['uid'], oauth_token = data['oauth_token'])

class DBtobesetup:
    def GET(self):
        Base.metadata.create_all(engine)
        return 'Success!'
