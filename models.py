# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:wuchujiemysql@localhost:3306/unlockdb?charset=utf8', echo=True, pool_recycle=20)

Base = declarative_base()

class Type(Base):
    __tablename__ = 'types'

    id          = Column(Integer, primary_key=True)
    band        = Column(String(50), nullable=False)
    phone_type  = Column(String(100), nullable=False)
    support_device= Column(String(100), nullable=False)
    time_cost   = Column(String(50), nullable=False)
    price       = Column(String(12), nullable=False)
    pic_name    = Column(String(50))

    def __init__(self, band, phone_type, sd, tc, pr, pn):
        self.band = band
        self.phone_type = phone_type
        self.support_device = sd
        self.time_cost = tc
        self.price = pr
        self.pic_name = pn

class Ordertick(Base):
    __tablename__ = 'orders'

    id          = Column(Integer, primary_key=True)
    create_time = Column(DateTime, nullable=False)
    band        = Column(String(50), nullable=False)
    phone_type  = Column(String(100), nullable=False)
    support_device= Column(String(100), nullable=False)
    time_cost   = Column(String(50), nullable=False)
    price       = Column(String(12), nullable=False)
    pic_name    = Column(String(50))
    imei        = Column(String(512), nullable=False)
    email       = Column(String(512), nullable=False)

    def __init__(self, band, phone_type, sd, tc, price, pn, imei, email, crt):
        self.band = band
        self.phone_type = phone_type
        self.support_device = sd
        self.time_cost = tc
        self.price = price
        self.pic_name = pn
        self.imei = imei
        self.email = email
        self.create_time = crt

#Base.metadata.create_all(engine)

