import web
from handlers import *
from sqlalchemy.orm import scoped_session, sessionmaker
from models import engine
import admin

# 404 & 500
def notfound():
    return web.notfound(
            "Sorry, the page you were looking for was not found.")
def internalerror():
    return web.internalerror("Bad, bad server. No donut for you.")

# url settings
urls = (
    '/?', 'Index',
    '/admin', admin.app,
    '/advantage', 'Advantage',
    '/unlock', 'Unlock',
    '/check', 'Check',
    '/faq', 'Faq',
    '/order', 'Order',
    '/ticket', 'Ticket',
    '/dbtobesetup', 'DBtobesetup',
#    '/.+', 'Redirect',
)

#sqlsession
def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # if the above alone doesn't work, uncomment the following line:
        # web.ctx.orm.expunge_all()
        web.ctx.orm.close()


app = web.application(urls, globals())
app.add_processor(load_sqla)
app.notfound = notfound
app.internalerror = internalerror
application = app.wsgifunc()
