#!/usr/bin/python
# -*- coding: utf-8 -*-

import web
from hashlib import sha512 as sha
from time import time as tt
from models import Ordertick as OD
from models import Type
from jinja2 import Environment, FileSystemLoader
from sqlalchemy import func
import utils

env = Environment(loader = FileSystemLoader('templates/admin'))

# url settings
urls = (
    '/?', 'Index',
    '/login', 'Login',
    '/orders', 'Orders',
    '/sub/(.*)', 'Suborders',
    '/imei/(.*)', 'IMEIcheck',
    '/item/(.*)', 'Itemcheck',
    '/ajax/orderdata', 'Orderdata',
    '/ajax/update', 'Orderupdate',
    '/.+', 'Redirect',
)

def logged(func):
    def wrap(*args):
        pas = 'acer' + sha('lenovo').hexdigest() + str(tt())[:6]
        if web.cookies().get('pas') != sha(pas).hexdigest():
            raise web.seeother("/login")
        else:
            return func(*args)
    return wrap

class Index:
    @logged
    def GET(self):
        items = web.ctx.orm.query(Type.phone_type).all()
        items = set([ str(i.phone_type) for i in items])
        return env.get_template('index.htm').render(items=items)
class Orders:
    @logged
    def GET(self):
        return env.get_template('orders.htm').render()
class Suborders:
    @logged
    def GET(self, sub):
        return env.get_template('suborders.htm').render(sub=sub)
class IMEIcheck:
    @logged
    def GET(self, imei):
        odt = web.ctx.orm.query(OD).filter(OD.imei.like('%'+imei+'%')).all()
        size = web.ctx.orm.query(func.count(OD.id)).\
                filter(OD.imei == imei).one()[0]
        data = utils.jsonify(OD, odt, OD.id, OD.create_time, OD.pic_name,
                OD.imei, OD.email, OD.phone_type, OD.price)
        datastr = '{"Rows":' + data +',"Total":' + str(size) + '}'
        return env.get_template('imei.htm').render(datastr=datastr)
class Itemcheck:
    @logged
    def GET(self, item):
        odt = web.ctx.orm.query(OD).filter(OD.phone_type == item).all()
        size = web.ctx.orm.query(func.count(OD.id)).\
                filter(OD.phone_type == item).one()[0]
        data = utils.jsonify(OD, odt, OD.id, OD.create_time, OD.pic_name,
                OD.imei, OD.email, OD.phone_type, OD.price)
        datastr = '{"Rows":' + data +',"Total":' + str(size) + '}'
        return env.get_template('imei.htm').render(datastr=datastr)
class Orderupdate:
    @logged
    def POST(self):
        try:
            oid = int(web.input(id=None).id)
            status = web.input(status=None).status

            if oid < 0 or status not in [u'未付款',u'已付款',u'已提交',u'成功',u'失敗']:
                return 'no'
            cn_to_en = {u'未付款':'checking payment',u'已付款':'payment confirmed',
                    u'已提交':'in process',u'成功':'unlocked',u'失敗':'reject'}
            odt = web.ctx.orm.query(OD).filter(OD.id == oid).one()
            odt.pic_name = cn_to_en[status]
            web.ctx.orm.commit()
            return cn_to_en[status]
        except:
            web.ctx.orm.rollback()
            return 'no'

class Orderdata:
    @logged
    def POST(self):
        page = int(web.input(page=1).page) - 1
        pgs  = int(web.input(pagesize=20).pagesize)
        sub  =  web.input(sub=None).sub

        if not sub:
            # orgin
            odt = web.ctx.orm.query(OD).\
                    order_by(OD.id.desc())[0 + page*pgs : pgs + page*pgs]
            size = web.ctx.orm.query(func.count(OD.id)).one()[0]
        #subpages
        elif sub == 'nopay':
            odt = web.ctx.orm.query(OD).\
                    filter(OD.pic_name == 'checking payment').\
                    order_by(OD.id.desc())[0 + page*pgs : pgs + page*pgs]
            size = web.ctx.orm.query(func.count(OD.id)).\
                    filter(OD.pic_name == 'checking payment').one()[0]
        elif sub == 'paied':
            odt = web.ctx.orm.query(OD).\
                    filter(OD.pic_name == 'payment confirmed').\
                    order_by(OD.id.desc())[0 + page*pgs : pgs + page*pgs]
            size = web.ctx.orm.query(func.count(OD.id)).\
                    filter(OD.pic_name == 'payment confirmed').one()[0]
        elif sub == 'process':
            odt = web.ctx.orm.query(OD).\
                    filter(OD.pic_name == 'in process').\
                    order_by(OD.id.desc())[0 + page*pgs : pgs + page*pgs]
            size = web.ctx.orm.query(func.count(OD.id)).\
                    filter(OD.pic_name == 'in process').one()[0]
        elif sub == 'success':
            odt = web.ctx.orm.query(OD).\
                    filter(OD.pic_name == 'unlocked').\
                    order_by(OD.id.desc())[0 + page*pgs : pgs + page*pgs]
            size = web.ctx.orm.query(func.count(OD.id)).\
                    filter(OD.pic_name == 'unlocked').one()[0]
        elif sub == 'fail':
            odt = web.ctx.orm.query(OD).\
                    filter(OD.pic_name == 'reject').\
                    order_by(OD.id.desc())[0 + page*pgs : pgs + page*pgs]
            size = web.ctx.orm.query(func.count(OD.id)).\
                    filter(OD.pic_name == 'reject').one()[0]

        data = utils.jsonify(OD, odt, OD.id, OD.create_time, OD.pic_name,
                OD.imei, OD.email, OD.phone_type, OD.price)
        return '{"Rows":' + data +',"Total":' + str(size) + '}'

class Login:
    def GET(self):
        web.setcookie('pas', '' , 30000)
        return env.get_template('login.html').render()
    def POST(self):
        d = web.input()
        pas = d.username + sha(d.password).hexdigest() + str(tt())[:6]
        web.setcookie('pas', sha(pas).hexdigest() , 30000)
        web.seeother("./")

class Redirect:
    def GET(self):
        web.found('/')

app = web.application(urls, globals())

